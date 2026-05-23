from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from typing import Any

import httpx


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


@dataclass(frozen=True)
class ImageBatchConcept:
    image_index: int
    purpose: str
    prompt: str


_QUESTION_MARK_RUN_RE = re.compile(r"\?{4,}")
_MOJIBAKE_MARKERS = (
    "\u0420\u045f",
    "\u0420\u2019",
    "\u0420\u00b0",
    "\u0420\u00b5",
    "\u0420\u0451",
    "\u0420\u0405",
    "\u0421\u201a",
    "\u0421\u0453",
    "\u0421\u0402",
    "\u0421\u040a",
    "\u00d0",
    "\u00d1",
    "\u00e2",
)


def validate_prompt_text(prompt: str) -> None:
    text = str(prompt or "")
    if _QUESTION_MARK_RUN_RE.search(text):
        raise ImageGenerationError("Prompt text contains replacement question marks")
    marker_hits = sum(1 for marker in _MOJIBAKE_MARKERS if marker in text)
    if marker_hits >= 4:
        raise ImageGenerationError("Prompt text looks mojibake-corrupted")


def extract_openrouter_image_bytes(payload: dict[str, Any]) -> bytes:
    image_url = _extract_image_url(payload)
    return _decode_openrouter_image_url(image_url)


def extract_openrouter_image_bytes_list(payload: dict[str, Any]) -> list[bytes]:
    image_urls = _extract_image_urls(payload)
    return [_decode_openrouter_image_url(image_url) for image_url in image_urls]


def _decode_openrouter_image_url(image_url: str) -> bytes:
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
    raw_usage = payload.get("usage")
    raw_cost = raw_usage.get("cost") if isinstance(raw_usage, dict) else raw_usage
    try:
        cost_usd = float(raw_cost or 0)
    except (TypeError, ValueError):
        cost_usd = 0.0
    return ImageGenerationUsage(model=model, cost_usd=cost_usd)


def _extract_image_url(payload: dict[str, Any]) -> str:
    return _extract_image_urls(payload)[0]


def _extract_image_urls(payload: dict[str, Any]) -> list[str]:
    try:
        images = payload["choices"][0]["message"]["images"]
        urls = [item["image_url"]["url"] for item in images]
        if urls:
            return urls
    except (KeyError, IndexError, TypeError):
        pass

    try:
        urls = [item["url"] for item in payload["data"]]
        if urls:
            return urls
    except (KeyError, IndexError, TypeError) as exc:
        raise ImageGenerationError("OpenRouter response does not contain images") from exc

    raise ImageGenerationError("OpenRouter response does not contain images")


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


def _build_batch_image_prompt(concepts: list[ImageBatchConcept]) -> str:
    for concept in concepts:
        validate_prompt_text(str(concept.prompt))
    lines = [
        f"Generate exactly {len(concepts)} separate marketplace-ready output images.",
        "Return each result as a separate image output in message.images, not a collage and not a grid.",
        "Use the input photos as references of the same product.",
        "Preserve product identity, shape, color, material, visible text, and distinctive details from the references.",
        "Use aspect ratio 3:4 for every output image.",
        "",
        "Required outputs:",
    ]
    for concept in concepts:
        lines.append(f"Image {concept.image_index} ({concept.purpose}): {concept.prompt}")
    return "\n".join(lines)


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


async def generate_single_image_result(
    prompt: str,
    reference_photo_bytes: bytes,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> GeneratedImage:
    validate_prompt_text(prompt)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    _image_content_item(reference_photo_bytes),
                    {
                        "type": "text",
                        "text": prompt,
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


async def generate_batch_image_results(
    *,
    concepts: list[ImageBatchConcept],
    reference_photo_bytes: list[bytes],
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> list[GeneratedImage]:
    if not concepts:
        return []
    if not reference_photo_bytes:
        raise ImageGenerationError("Batch image generation requires at least one reference photo")

    content: list[dict[str, Any]] = []
    for index, photo_bytes in enumerate(reference_photo_bytes, start=1):
        content.append(_image_content_item(photo_bytes))
        content.append({"type": "text", "text": f"Input reference photo {index}"})
    content.append({"type": "text", "text": _build_batch_image_prompt(concepts)})

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": content,
            }
        ],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": "3:4",
            "image_size": "1K",
        },
        "max_tokens": 4096,
    }

    async with httpx.AsyncClient(timeout=300.0) as client:
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

    image_bytes_list = extract_openrouter_image_bytes_list(result)
    if len(image_bytes_list) != len(concepts):
        raise ImageGenerationError(
            f"OpenRouter returned wrong image count: expected {len(concepts)} images, got {len(image_bytes_list)}"
        )

    usage = extract_openrouter_image_usage(result, fallback_model=model)
    cost_per_image = usage.cost_usd / len(image_bytes_list) if image_bytes_list else 0.0
    return [
        GeneratedImage(
            image_bytes=image_bytes,
            usage=ImageGenerationUsage(model=usage.model, cost_usd=cost_per_image),
        )
        for image_bytes in image_bytes_list
    ]


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
) -> GeneratedImage:
    telegram_file = await bot.get_file(reference_photo_file_id)
    photo_bytes = await telegram_file.download_as_bytearray()
    return await generate_single_image_result(
        prompt=prompt,
        reference_photo_bytes=bytes(photo_bytes),
        api_key=api_key,
        model=model,
        site_url=site_url,
    )


async def generate_marketplace_batch_image_results(
    *,
    concepts: list[ImageBatchConcept],
    reference_photo_file_ids: list[str],
    bot: Any,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> list[GeneratedImage]:
    reference_photo_bytes: list[bytes] = []
    for file_id in reference_photo_file_ids:
        telegram_file = await bot.get_file(file_id)
        photo_bytes = await telegram_file.download_as_bytearray()
        reference_photo_bytes.append(bytes(photo_bytes))

    return await generate_batch_image_results(
        concepts=concepts,
        reference_photo_bytes=reference_photo_bytes,
        api_key=api_key,
        model=model,
        site_url=site_url,
    )


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
