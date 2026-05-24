from __future__ import annotations

import base64
import logging
import re
from dataclasses import dataclass
from typing import Any

import httpx


OPENROUTER_CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"
MIN_BATCH_IMAGE_TIMEOUT_SECONDS = 420.0
BATCH_IMAGE_TIMEOUT_SECONDS_PER_IMAGE = 180.0


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


def batch_image_timeout_seconds(concept_count: int) -> float:
    return max(
        MIN_BATCH_IMAGE_TIMEOUT_SECONDS,
        float(max(1, concept_count)) * BATCH_IMAGE_TIMEOUT_SECONDS_PER_IMAGE,
    )


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
    product_description = str(concepts[0].prompt).strip()
    return (
        f"Сгенерируй {len(concepts)} отдельных изображения данного товара. "
        "Изображения необходимы для карточек товара маркетплейсов Ozon/WB, "
        "нужно сделать в лучшем продающем виде для карточки товара.\n"
        f"Немного информации о товаре: {product_description}\n\n"
        "Установить соотношение сторон 3:4."
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

    async with httpx.AsyncClient(timeout=batch_image_timeout_seconds(len(concepts))) as client:
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
    if not image_bytes_list:
        raise ImageGenerationError(
            f"OpenRouter returned no images: expected {len(concepts)} images"
        )
    if len(image_bytes_list) != len(concepts):
        logging.warning(
            "OpenRouter returned unexpected image count: expected=%s got=%s",
            len(concepts),
            len(image_bytes_list),
        )
    image_bytes_list = image_bytes_list[: len(concepts)]

    usage = extract_openrouter_image_usage(result, fallback_model=model)
    cost_per_image = usage.cost_usd / len(image_bytes_list) if image_bytes_list else 0.0
    return [
        GeneratedImage(
            image_bytes=image_bytes,
            usage=ImageGenerationUsage(model=usage.model, cost_usd=cost_per_image),
        )
        for image_bytes in image_bytes_list
    ]


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
