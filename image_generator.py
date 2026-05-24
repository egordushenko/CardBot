from __future__ import annotations

import base64
import logging
import re
from dataclasses import dataclass
from io import BytesIO
from typing import Any

import httpx
from PIL import Image, ImageOps


OPENROUTER_CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"
MIN_BATCH_IMAGE_TIMEOUT_SECONDS = 420.0
BATCH_IMAGE_TIMEOUT_SECONDS_PER_IMAGE = 180.0
REFERENCE_COLLAGE_SIZE = (1536, 1536)
REFERENCE_COLLAGE_BACKGROUND = (246, 246, 244)
REFERENCE_COLLAGE_GAP = 16
REFERENCE_COLLAGE_LAYOUTS = {
    1: (1,),
    2: (2,),
    3: (1, 2),
    4: (2, 2),
    5: (2, 3),
    6: (3, 3),
    7: (3, 4),
}


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


def _resample_filter() -> Any:
    return getattr(Image, "Resampling", Image).LANCZOS


def build_reference_photo_collage(
    reference_photo_bytes: list[bytes],
    *,
    canvas_size: tuple[int, int] = REFERENCE_COLLAGE_SIZE,
    gap: int = REFERENCE_COLLAGE_GAP,
) -> bytes:
    if not reference_photo_bytes:
        raise ImageGenerationError("Reference collage requires at least one photo")
    if len(reference_photo_bytes) > 7:
        raise ImageGenerationError("Reference collage supports up to 7 photos")

    decoded_images: list[Image.Image] = []
    for photo_bytes in reference_photo_bytes:
        try:
            image = Image.open(BytesIO(photo_bytes))
            image = ImageOps.exif_transpose(image).convert("RGB")
        except Exception as exc:
            raise ImageGenerationError("Reference photo could not be decoded") from exc
        decoded_images.append(image)

    row_layout = REFERENCE_COLLAGE_LAYOUTS[len(decoded_images)]
    canvas_width, canvas_height = canvas_size
    canvas = Image.new("RGB", canvas_size, REFERENCE_COLLAGE_BACKGROUND)
    row_height = (canvas_height - gap * (len(row_layout) + 1)) // len(row_layout)

    index = 0
    for row, columns in enumerate(row_layout):
        cell_width = (canvas_width - gap * (columns + 1)) // columns
        row_y = gap + row * (row_height + gap)
        for column in range(columns):
            image = decoded_images[index]
            fitted = ImageOps.contain(image, (cell_width, row_height), _resample_filter())
            x = gap + column * (cell_width + gap) + (cell_width - fitted.width) // 2
            y = row_y + (row_height - fitted.height) // 2
            canvas.paste(fitted, (x, y))
            index += 1
            if index >= len(decoded_images):
                break

    output = BytesIO()
    canvas.save(output, format="JPEG", quality=92, optimize=True)
    return output.getvalue()


def _build_single_image_prompt(
    concept: ImageBatchConcept,
    *,
    total_count: int,
) -> str:
    validate_prompt_text(str(concept.prompt))
    shot_goal = str(concept.purpose).strip() or "marketplace product-card image"
    return (
        "Draw one photorealistic 3:4 marketplace product-card image.\n\n"
        "Reference:\n"
        "The attached image is a reference collage showing the same product from multiple angles. "
        "Use it only to understand the real product identity, shape, proportions, materials, "
        "colors, markings, and construction. Do not reproduce the collage layout.\n\n"
        "Product facts:\n"
        f"{str(concept.prompt).strip()}\n\n"
        "Shot goal:\n"
        f"{shot_goal}\n\n"
        "Composition:\n"
        "Return exactly one image only. "
        "Create a polished commercial marketplace image for Ozon/Wildberries. "
        "Show one clear product scene only. Keep the product large, centered, sharp, "
        "and easy to inspect.\n\n"
        "Preserve:\n"
        "Preserve the product's exact shape, proportions, colors, materials, visible markings, "
        "and functional details from the reference collage.\n\n"
        "Avoid:\n"
        "No collage, no grid, no split-screen, no multiple product variants, no extra products, "
        "no watermark, no unreadable overlay text, no invented labels."
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

    for concept in concepts:
        validate_prompt_text(str(concept.prompt))

    collage_bytes = build_reference_photo_collage(reference_photo_bytes)
    generated_images: list[GeneratedImage] = []

    async with httpx.AsyncClient(timeout=batch_image_timeout_seconds(len(concepts))) as client:
        for concept in concepts:
            content: list[dict[str, Any]] = [
                _image_content_item(collage_bytes),
                {"type": "text", "text": "Input reference collage"},
                {
                    "type": "text",
                    "text": _build_single_image_prompt(concept, total_count=len(concepts)),
                },
            ]
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
                raise ImageGenerationError("OpenRouter returned no images")
            if len(image_bytes_list) > 1:
                logging.warning(
                    "OpenRouter returned multiple images for single-image request: got=%s",
                    len(image_bytes_list),
                )

            usage = extract_openrouter_image_usage(result, fallback_model=model)
            generated_images.append(
                GeneratedImage(
                    image_bytes=image_bytes_list[0],
                    usage=ImageGenerationUsage(model=usage.model, cost_usd=usage.cost_usd),
                )
            )

    if len(generated_images) != len(concepts):
        raise ImageGenerationError(
            f"OpenRouter returned {len(generated_images)} images: expected {len(concepts)} images"
        )
    return generated_images


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
