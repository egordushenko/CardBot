from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from marketplace_rules import sanitize_description, sanitize_ozon_hashtags, sanitize_title
from prompts import DIRECTOR_SYSTEM_PROMPT, OZON_SYSTEM_PROMPT, WB_SYSTEM_PROMPT


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_FREE_SUFFIX = ":free"


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


def _format_profile_value(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if str(item).strip())
    return str(value or "").strip()


def build_openrouter_model_fallbacks(model: str) -> list[str]:
    primary = model.strip()
    if not primary:
        return []

    candidates = [primary]
    if primary.endswith(OPENROUTER_FREE_SUFFIX):
        candidates.append(primary[: -len(OPENROUTER_FREE_SUFFIX)])

    result: list[str] = []
    for candidate in candidates:
        if candidate and candidate not in result:
            result.append(candidate)
    return result


def build_category_profile_prompt_block(
    category_profile: dict[str, Any] | None,
    marketplace: str = "ozon",
) -> str:
    if not category_profile:
        return ""

    category = str(category_profile.get("category") or "").strip()
    if not category:
        return ""

    normalized_marketplace = normalize_marketplace(marketplace)
    if normalized_marketplace == "wb":
        return (
            "\n\nКатегорийный профиль WB:\n"
            f"Категория товара: {category}\n"
            f"Формула названия: {category_profile.get('title_formula')}\n"
            f"Длина названия: {category_profile.get('title_target_min')}-{category_profile.get('title_target_max')} символов\n"
            f"Длина описания: {category_profile.get('description_target_min')}-{category_profile.get('description_target_max')} символов\n"
            f"Целевое количество характеристик: {category_profile.get('characteristics_target_min')}-{category_profile.get('characteristics_target_max')}\n"
            f"Обязательные характеристики: {_format_profile_value(category_profile.get('required_characteristics'))}\n"
            f"Желательные характеристики: {_format_profile_value(category_profile.get('recommended_characteristics'))}\n"
            f"Типичные слова в названии: {_format_profile_value(category_profile.get('top_title_words'))}\n"
            "Если поле не следует из входа пользователя и не имеет разрешенного дефолта, не выводи его."
        )

    return (
        "\n\nКатегорийный профиль Ozon:\n"
        f"Категория товара: {category}\n"
        f"Длина названия: стремись к {category_profile.get('title_target_chars')} символам\n"
        f"Длина описания: {category_profile.get('desc_target_chars')} символов\n"
        f"Приоритетные характеристики: {_format_profile_value(category_profile.get('top_characteristics'))}\n"
        f"Примеры релевантных хэштегов для категории: {_format_profile_value(category_profile.get('top_hashtags'))}\n"
        f"Типичные SEO-слова для названий в этой категории: {_format_profile_value(category_profile.get('top_title_words'))}"
    )


def select_system_prompt(
    marketplace: str,
    category_profile: dict[str, Any] | None = None,
) -> str:
    normalized = normalize_marketplace(marketplace)
    if normalized == "ozon":
        return OZON_SYSTEM_PROMPT + build_category_profile_prompt_block(category_profile, "ozon")
    return WB_SYSTEM_PROMPT + build_category_profile_prompt_block(category_profile, "wb")


def build_resolved_fields_prompt_block(resolved_fields: dict[str, Any] | None) -> str:
    if not resolved_fields:
        return ""

    field_lines: list[str] = []
    instructions: list[str] = []
    for key, value in resolved_fields.items():
        if key == "__prompt_instructions__":
            if isinstance(value, list):
                instructions.extend(str(item).strip() for item in value if str(item).strip())
            elif str(value).strip():
                instructions.append(str(value).strip())
            continue
        if str(value).strip():
            field_lines.append(f"- {key}: {str(value).strip()}")

    blocks: list[str] = []
    if field_lines:
        blocks.append("Обогащенные поля для карточки:\n" + "\n".join(field_lines))
    if instructions:
        blocks.append("Дополнительные инструкции:\n" + "\n".join(f"- {item}" for item in instructions))
    if not blocks:
        return ""
    return "\n\n" + "\n\n".join(blocks)


def build_user_prompt(
    marketplace: str,
    user_input: str,
    resolved_fields: dict[str, Any] | None = None,
) -> str:
    normalized = normalize_marketplace(marketplace)
    name = MARKETPLACE_NAMES[normalized]
    return (
        f"Маркетплейс: {name}\n"
        f"Товар: {user_input.strip()}"
        f"{build_resolved_fields_prompt_block(resolved_fields)}"
    )


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
        if field_value.casefold().startswith("[укажите"):
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

    required = ("title", "description", "characteristics")
    for field in required:
        if not str(data.get(field, "")).strip():
            raise LLMResponseError(f"LLM response is missing required field: {field}")
    if normalized_marketplace == "ozon" and not str(data.get(search_field, "")).strip():
        raise LLMResponseError(f"LLM response is missing required field: {search_field}")

    return CardGeneration(
        title=sanitize_title(str(data["title"]), normalized_marketplace),
        description=sanitize_description(str(data["description"]), normalized_marketplace),
        keywords=(
            sanitize_ozon_hashtags(str(data[search_field]))
            if normalized_marketplace == "ozon"
            else str(data.get(search_field, "")).strip()
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
    category_profile: dict[str, Any] | None = None,
    resolved_fields: dict[str, Any] | None = None,
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

    messages = [
        {
            "role": "system",
            "content": select_system_prompt(marketplace, category_profile),
        },
        {
            "role": "user",
            "content": build_user_prompt(marketplace, user_input, resolved_fields),
        },
    ]
    model_candidates = build_openrouter_model_fallbacks(model)
    response = None
    last_error: Exception | None = None
    for candidate in model_candidates:
        try:
            response = await client.chat.completions.create(
                model=candidate,
                messages=messages,
                max_tokens=2200,
                temperature=0.7,
                response_format={"type": "json_object"},
            )
            break
        except Exception as exc:
            last_error = exc
            status_code = getattr(exc, "status_code", None)
            if status_code != 429 or candidate == model_candidates[-1]:
                raise

    if response is None:
        raise LLMResponseError("LLM request failed") from last_error

    content = response.choices[0].message.content
    if not content:
        raise LLMResponseError("LLM returned empty response")

    usage: Any = getattr(response, "usage", None)
    tokens_used = int(getattr(usage, "total_tokens", 0) or 0)
    card = parse_generation_payload(content, tokens_used=tokens_used, marketplace=marketplace)
    if normalize_marketplace(marketplace) == "wb":
        from wb_generation_quality import apply_wb_generation_quality

        return apply_wb_generation_quality(card, category_profile, user_input=user_input)
    return card


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
