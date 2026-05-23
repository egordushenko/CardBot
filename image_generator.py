from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any

import httpx

from prompts import PRODUCT_PRESERVATION_SUFFIX
from visual_pipeline import (
    ImageQualityReport,
    PhotoAnalysis,
    build_image_quality_prompt,
    build_photo_analysis_prompt,
    fallback_photo_analysis,
    parse_image_quality_payload,
    parse_photo_analysis_payload,
)


OPENROUTER_CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"


class ImageGenerationError(RuntimeError):
    pass


@dataclass(frozen=True)
class ImageGenerationUsage:
    model: str
    cost_usd: float


@dataclass(frozen=True)
class GeneratedImage:
    image_bytes: bytes
    usage: ImageGenerationUsage


def build_safe_image_prompt(prompt: str) -> str:
    return f"{prompt}{PRODUCT_PRESERVATION_SUFFIX}"


def extract_openrouter_image_bytes(payload: dict[str, Any]) -> bytes:
    image_url = _extract_image_url(payload)

    if not isinstance(image_url, str) or not image_url.strip():
        raise ImageGenerationError("OpenRouter image URL is empty")

    if image_url.startswith("data:"):
        try:
            _, encoded = image_url.split(",", 1)
            return base64.b64decode(encoded)
        except (ValueError, base64.binascii.Error) as exc:
            raise ImageGenerationError("OpenRouter returned invalid image data URL") from exc

    raise ImageGenerationError("OpenRouter returned external image URL")


def extract_openrouter_image_usage(
    payload: dict[str, Any],
    fallback_model: str,
) -> ImageGenerationUsage:
    model = str(payload.get("model") or fallback_model).strip() or fallback_model
    raw_cost = payload.get("usage")
    try:
        cost_usd = float(raw_cost or 0)
    except (TypeError, ValueError):
        cost_usd = 0.0
    return ImageGenerationUsage(model=model, cost_usd=cost_usd)


def _extract_image_url(payload: dict[str, Any]) -> str:
    try:
        return payload["choices"][0]["message"]["images"][0]["image_url"]["url"]
    except (KeyError, IndexError, TypeError):
        pass

    try:
        return payload["data"][0]["url"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ImageGenerationError("OpenRouter response does not contain images") from exc


def _extract_openrouter_text(payload: dict[str, Any]) -> str:
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ImageGenerationError("OpenRouter response does not contain text") from exc
    if isinstance(content, list):
        text_parts = [
            str(item.get("text") or "")
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        ]
        return "\n".join(part for part in text_parts if part).strip()
    return str(content or "").strip()


def _image_content_item(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict[str, Any]:
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:{mime_type};base64,{encoded}",
        },
    }


async def _request_openrouter_text(
    *,
    content: list[dict[str, Any]],
    api_key: str,
    model: str,
    site_url: str,
    timeout: float = 45.0,
) -> str:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": content,
            }
        ],
        "response_format": {"type": "json_object"},
        "max_tokens": 900,
        "temperature": 0.1,
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            OPENROUTER_CHAT_COMPLETIONS_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": site_url,
                "X-Title": "CardBot",
            },
            json=payload,
        )
        response.raise_for_status()
        result = response.json()
    return _extract_openrouter_text(result)


async def analyze_reference_photo(
    *,
    product_description: str,
    marketplace: str,
    photo_index: int,
    reference_photo_bytes: bytes,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> PhotoAnalysis:
    content = [
        _image_content_item(reference_photo_bytes),
        {
            "type": "text",
            "text": build_photo_analysis_prompt(
                product_description=product_description,
                marketplace=marketplace,
                photo_index=photo_index,
            ),
        },
    ]
    text = await _request_openrouter_text(
        content=content,
        api_key=api_key,
        model=model,
        site_url=site_url,
    )
    parsed = parse_photo_analysis_payload(text, photos_count=photo_index + 1)
    if not parsed:
        raise ImageGenerationError("vision analysis returned empty result")
    return parsed[0]


async def analyze_marketplace_reference_photos(
    *,
    product_description: str,
    marketplace: str,
    photo_file_ids: list[str],
    bot: Any,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> list[PhotoAnalysis]:
    analyses: list[PhotoAnalysis] = []
    photos_count = len(photo_file_ids)
    for photo_index, file_id in enumerate(photo_file_ids):
        try:
            telegram_file = await bot.get_file(file_id)
            photo_bytes = bytes(await telegram_file.download_as_bytearray())
            analyses.append(
                await analyze_reference_photo(
                    product_description=product_description,
                    marketplace=marketplace,
                    photo_index=photo_index,
                    reference_photo_bytes=photo_bytes,
                    api_key=api_key,
                    model=model,
                    site_url=site_url,
                )
            )
        except Exception:
            analyses.append(
                fallback_photo_analysis(
                    photo_index,
                    product_description=product_description,
                    photos_count=photos_count,
                )
            )
    return analyses


async def evaluate_generated_image_quality(
    *,
    concept_prompt: str,
    reference_photo_bytes: bytes,
    generated_image_bytes: bytes,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
    expected_visible_text: tuple[str, ...] = (),
) -> ImageQualityReport:
    content = [
        _image_content_item(reference_photo_bytes),
        _image_content_item(generated_image_bytes, mime_type="image/png"),
        {
            "type": "text",
            "text": build_image_quality_prompt(
                concept_prompt=concept_prompt,
                expected_visible_text=expected_visible_text,
            ),
        },
    ]
    text = await _request_openrouter_text(
        content=content,
        api_key=api_key,
        model=model,
        site_url=site_url,
        timeout=60.0,
    )
    return parse_image_quality_payload(text)


async def generate_single_image_result(
    prompt: str,
    reference_photo_bytes: bytes,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> GeneratedImage:
    safe_prompt = build_safe_image_prompt(prompt)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    _image_content_item(reference_photo_bytes),
                    {
                        "type": "text",
                        "text": safe_prompt,
                    },
                ],
            }
        ],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": "3:4",
            "image_size": "1K",
        },
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            OPENROUTER_CHAT_COMPLETIONS_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": site_url,
                "X-Title": "CardBot",
            },
            json=payload,
        )
        response.raise_for_status()
        result = response.json()

    return GeneratedImage(
        image_bytes=extract_openrouter_image_bytes(result),
        usage=extract_openrouter_image_usage(result, fallback_model=model),
    )


async def generate_single_image(
    prompt: str,
    reference_photo_bytes: bytes,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> bytes:
    result = await generate_single_image_result(
        prompt=prompt,
        reference_photo_bytes=reference_photo_bytes,
        api_key=api_key,
        model=model,
        site_url=site_url,
    )
    return result.image_bytes


async def generate_marketplace_image_result(
    prompt: str,
    reference_photo_file_id: str,
    bot: Any,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
    quality_model: str | None = None,
    quality_enabled: bool = False,
    expected_visible_text: tuple[str, ...] = (),
) -> GeneratedImage:
    telegram_file = await bot.get_file(reference_photo_file_id)
    photo_bytes = await telegram_file.download_as_bytearray()
    result = await generate_single_image_result(
        prompt=prompt,
        reference_photo_bytes=bytes(photo_bytes),
        api_key=api_key,
        model=model,
        site_url=site_url,
    )
    if quality_enabled and quality_model:
        report = await evaluate_generated_image_quality(
            concept_prompt=prompt,
            reference_photo_bytes=bytes(photo_bytes),
            generated_image_bytes=result.image_bytes,
            api_key=api_key,
            model=quality_model,
            site_url=site_url,
            expected_visible_text=expected_visible_text,
        )
        if not report.passed:
            issues = ", ".join(report.issues) or "unknown"
            raise ImageGenerationError(f"image QA failed: {issues}; {report.summary}")
    return result


async def generate_marketplace_image(
    prompt: str,
    reference_photo_file_id: str,
    bot: Any,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> bytes:
    result = await generate_marketplace_image_result(
        prompt=prompt,
        reference_photo_file_id=reference_photo_file_id,
        bot=bot,
        api_key=api_key,
        model=model,
        site_url=site_url,
    )
    return result.image_bytes


async def generate_all_images(
    concepts: list[Any],
    photo_file_ids: list[str],
    bot: Any,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> list[tuple[int, bytes]]:
    import asyncio

    async def process_one(concept: Any) -> tuple[int, bytes]:
        photo_index = min(int(concept.photo_index), len(photo_file_ids) - 1)
        image_bytes = await generate_marketplace_image(
            prompt=concept.prompt,
            reference_photo_file_id=photo_file_ids[photo_index],
            bot=bot,
            api_key=api_key,
            model=model,
            site_url=site_url,
        )
        return int(concept.image_index), image_bytes

    results = await asyncio.gather(
        *(process_one(concept) for concept in concepts),
        return_exceptions=True,
    )
    return [result for result in results if not isinstance(result, Exception)]
