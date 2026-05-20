from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from marketplace_rules import sanitize_description, sanitize_ozon_hashtags, sanitize_title
from prompts import DIRECTOR_SYSTEM_PROMPT, OZON_SYSTEM_PROMPT, WB_SYSTEM_PROMPT


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class LLMResponseError(RuntimeError):
    pass


@dataclass(frozen=True)
class CardGeneration:
    title: str
    description: str
    keywords: str
    characteristics: str
    tokens_used: int = 0
    marketplace: str = "wb"


@dataclass(frozen=True)
class ImageConcept:
    image_index: int
    purpose: str
    photo_index: int
    prompt: str


MARKETPLACE_NAMES = {
    "wb": "Wildberries",
    "wildberries": "Wildberries",
    "ozon": "Ozon",
}


def normalize_marketplace(marketplace: str) -> str:
    normalized = marketplace.strip().lower()
    if normalized == "wildberries":
        return "wb"
    if normalized in {"wb", "ozon"}:
        return normalized
    raise LLMResponseError(f"Unsupported marketplace: {marketplace}")


def select_system_prompt(marketplace: str) -> str:
    normalized = normalize_marketplace(marketplace)
    if normalized == "ozon":
        return OZON_SYSTEM_PROMPT
    return WB_SYSTEM_PROMPT


def build_user_prompt(marketplace: str, user_input: str) -> str:
    normalized = normalize_marketplace(marketplace)
    name = MARKETPLACE_NAMES[normalized]
    return f"Маркетплейс: {name}\nТовар: {user_input.strip()}"


def build_image_director_user_prompt(
    product_description: str,
    marketplace: str,
    photos_count: int,
    images_count: int,
) -> str:
    normalized = normalize_marketplace(marketplace)
    name = MARKETPLACE_NAMES[normalized]
    last_index = max(photos_count - 1, 0)
    return (
        f"Товар: {product_description.strip()}\n"
        f"Маркетплейс: {name}\n"
        f"Загружено фото: {photos_count} (индексы от 0 до {last_index})\n"
        f"Нужно сгенерировать изображений: {images_count}\n\n"
        f"Создай {images_count} уникальных концепций изображений для карточки товара. "
        f"Распредели {photos_count} фото по изображениям адаптивно."
    )


def _strip_markdown_fence(payload: str) -> str:
    text = payload.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


_SERVICE_MARKERS_RE = re.compile(r"(?i)(\\r|\\n|\bsummary\b|\bdepth\b|\btfo\b)")
_CJK_RE = re.compile(r"[\u3400-\u9fff]")


def sanitize_characteristics(value: str) -> str:
    lines: list[str] = []
    for raw_line in value.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if _SERVICE_MARKERS_RE.search(line) or _CJK_RE.search(line):
            break
        if ":" not in line:
            continue
        key, field_value = line.split(":", 1)
        key = key.strip()
        field_value = field_value.strip()
        if not key or not field_value:
            continue
        lines.append(f"{key}: {field_value}")
    return "\n".join(lines).strip()


def parse_generation_payload(
    payload: str,
    tokens_used: int = 0,
    marketplace: str = "wb",
) -> CardGeneration:
    try:
        data = json.loads(_strip_markdown_fence(payload))
    except json.JSONDecodeError as exc:
        raise LLMResponseError("LLM returned invalid JSON") from exc

    normalized_marketplace = normalize_marketplace(marketplace)
    search_field = "hashtags" if normalized_marketplace == "ozon" else "keywords"

    if "characteristics" in data:
        data["characteristics"] = sanitize_characteristics(str(data["characteristics"]))

    required = ("title", "description", search_field, "characteristics")
    for field in required:
        if not str(data.get(field, "")).strip():
            raise LLMResponseError(f"LLM response is missing required field: {field}")

    return CardGeneration(
        title=sanitize_title(str(data["title"]), normalized_marketplace),
        description=sanitize_description(str(data["description"]), normalized_marketplace),
        keywords=(
            sanitize_ozon_hashtags(str(data[search_field]))
            if normalized_marketplace == "ozon"
            else str(data[search_field]).strip()
        ),
        characteristics=str(data["characteristics"]).strip(),
        tokens_used=tokens_used,
        marketplace=normalized_marketplace,
    )


def parse_image_concepts_payload(
    payload: str,
    photos_count: int,
    images_count: int,
) -> list[ImageConcept]:
    try:
        data = json.loads(_strip_markdown_fence(payload))
    except json.JSONDecodeError as exc:
        raise LLMResponseError("LLM returned invalid image concepts JSON") from exc

    raw_concepts = data.get("concepts")
    if not isinstance(raw_concepts, list) or not raw_concepts:
        raise LLMResponseError("LLM response is missing required field: concepts")

    concepts: list[ImageConcept] = []
    max_photo_index = max(photos_count - 1, 0)
    for index, item in enumerate(raw_concepts[:images_count], start=1):
        if not isinstance(item, dict):
            raise LLMResponseError("LLM image concept must be an object")
        prompt = str(item.get("prompt", "")).strip()
        if not prompt:
            raise LLMResponseError("LLM image concept is missing prompt")
        image_index = int(item.get("image_index") or index)
        photo_index = int(item.get("photo_index") or 0)
        photo_index = min(max(photo_index, 0), max_photo_index)
        concepts.append(
            ImageConcept(
                image_index=image_index,
                purpose=str(item.get("purpose", "")).strip() or f"image {image_index}",
                photo_index=photo_index,
                prompt=prompt,
            )
        )

    if len(concepts) != images_count:
        raise LLMResponseError("LLM returned fewer image concepts than requested")
    return concepts


async def generate_card(
    user_input: str,
    api_key: str,
    model: str = "deepseek/deepseek-v4-flash",
    site_url: str = "https://alterega.ru",
    marketplace: str = "wb",
) -> CardGeneration:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
        timeout=30.0,
        max_retries=1,
        default_headers={
            "HTTP-Referer": site_url,
            "X-Title": "CardBot",
        },
    )

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": select_system_prompt(marketplace)},
            {"role": "user", "content": build_user_prompt(marketplace, user_input)},
        ],
        max_tokens=1500,
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise LLMResponseError("LLM returned empty response")

    usage: Any = getattr(response, "usage", None)
    tokens_used = int(getattr(usage, "total_tokens", 0) or 0)
    return parse_generation_payload(content, tokens_used=tokens_used, marketplace=marketplace)


async def generate_image_prompts(
    product_description: str,
    marketplace: str,
    photos_count: int,
    images_count: int,
    api_key: str,
    model: str = "deepseek/deepseek-v4-flash",
    site_url: str = "https://alterega.ru",
) -> list[ImageConcept]:
    from openai import AsyncOpenAI

    if photos_count < 1 or photos_count > 5:
        raise LLMResponseError("photos_count must be between 1 and 5")
    if images_count < 1 or images_count > 9:
        raise LLMResponseError("images_count must be between 1 and 9")

    client = AsyncOpenAI(
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
        timeout=45.0,
        max_retries=1,
        default_headers={
            "HTTP-Referer": site_url,
            "X-Title": "CardBot",
        },
    )

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": DIRECTOR_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_image_director_user_prompt(
                    product_description=product_description,
                    marketplace=marketplace,
                    photos_count=photos_count,
                    images_count=images_count,
                ),
            },
        ],
        max_tokens=2000,
        temperature=0.8,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise LLMResponseError("LLM returned empty image concepts response")
    return parse_image_concepts_payload(
        content,
        photos_count=photos_count,
        images_count=images_count,
    )
