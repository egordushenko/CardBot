from __future__ import annotations

import base64
from typing import Any

import httpx

from prompts import PRODUCT_PRESERVATION_SUFFIX


OPENROUTER_CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"


class ImageGenerationError(RuntimeError):
    pass


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


def _extract_image_url(payload: dict[str, Any]) -> str:
    try:
        return payload["choices"][0]["message"]["images"][0]["image_url"]["url"]
    except (KeyError, IndexError, TypeError):
        pass

    try:
        return payload["data"][0]["url"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ImageGenerationError("OpenRouter response does not contain images") from exc


async def generate_single_image(
    prompt: str,
    reference_photo_bytes: bytes,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> bytes:
    photo_b64 = base64.b64encode(reference_photo_bytes).decode("ascii")
    safe_prompt = build_safe_image_prompt(prompt)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{photo_b64}",
                        },
                    },
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

    return extract_openrouter_image_bytes(result)


async def generate_marketplace_image(
    prompt: str,
    reference_photo_file_id: str,
    bot: Any,
    api_key: str,
    model: str,
    site_url: str = "https://alterega.ru",
) -> bytes:
    telegram_file = await bot.get_file(reference_photo_file_id)
    photo_bytes = await telegram_file.download_as_bytearray()
    return await generate_single_image(
        prompt=prompt,
        reference_photo_bytes=bytes(photo_bytes),
        api_key=api_key,
        model=model,
        site_url=site_url,
    )


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
