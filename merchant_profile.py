from __future__ import annotations

import re
from typing import Any


MERCHANT_PROFILE_FIELDS: tuple[dict[str, str], ...] = (
    {
        "key": "visual_style_default",
        "label": "Стиль бренда",
        "prompt": "Опишите визуальный стиль бренда: минимализм, премиум, спорт, eco, яркий маркетплейс.",
    },
    {
        "key": "text_tone",
        "label": "Тон текста",
        "prompt": "Опишите тон текста: экспертный, дружелюбный, премиальный, спокойный, дерзкий.",
    },
    {
        "key": "preferred_card_formats",
        "label": "Формат карточек",
        "prompt": "Опишите предпочитаемый формат карточек: коротко по выгодам, bullet points, storytelling, инфографика.",
    },
    {
        "key": "banned_words",
        "label": "Запрещённые слова",
        "prompt": "Укажите слова и формулировки, которых нужно избегать. Если ограничений нет, напишите '-'.",
    },
    {
        "key": "typical_product_segment",
        "label": "Типичный сегмент товаров",
        "prompt": "Опишите типичный сегмент товаров: женская одежда, спорт, детские товары, косметика, аксессуары.",
    },
)
MERCHANT_PROFILE_FIELD_BY_KEY = {field["key"]: field for field in MERCHANT_PROFILE_FIELDS}
MERCHANT_PROFILE_SKIP_VALUES = {"-", "—", "–", "нет", "не", "skip", "пропустить"}
EMPTY_VALUE = "—"
MERCHANT_PROFILE_IMAGE_VISUAL_RULES = (
    "Visual rules for image generation: strict grid layout, technical infographic, "
    "minimal decoration, one clear CTA."
)


def normalize_profile_value(value: Any | None, *, limit: int = 500) -> str:
    if value is None:
        return ""
    normalized = re.sub(r"\s+", " ", str(value)).strip()
    if normalized.casefold() in MERCHANT_PROFILE_SKIP_VALUES:
        return ""
    return normalized[:limit]


def normalize_merchant_profile(profile: dict[str, Any] | None) -> dict[str, str]:
    source = profile or {}
    return {
        field["key"]: normalize_profile_value(source.get(field["key"]))
        for field in MERCHANT_PROFILE_FIELDS
    }


def is_merchant_profile_empty(profile: dict[str, Any] | None) -> bool:
    return not any(normalize_merchant_profile(profile).values())


def _filled_profile_lines(profile: dict[str, Any] | None) -> list[str]:
    normalized = normalize_merchant_profile(profile)
    lines: list[str] = []
    for field in MERCHANT_PROFILE_FIELDS:
        value = normalized[field["key"]]
        if value:
            lines.append(f"- {field['label']}: {value}")
    return lines


def format_merchant_profile_message(profile: dict[str, Any] | None) -> str:
    lines = ["🏪 Профиль магазина"]
    normalized = normalize_merchant_profile(profile)
    if not any(normalized.values()):
        lines.append("")
        lines.append("Профиль пока не заполнен.")
    else:
        lines.append("")
        for field in MERCHANT_PROFILE_FIELDS:
            value = normalized[field["key"]] or EMPTY_VALUE
            lines.append(f"{field['label']}: {value}")
    return "\n".join(lines)


def build_merchant_profile_prompt_block(profile: dict[str, Any] | None) -> str:
    lines = _filled_profile_lines(profile)
    if not lines:
        return ""
    return (
        "\n\nПрофиль магазина пользователя:\n"
        "Учитывай профиль ниже как устойчивые предпочтения; прямые пожелания текущей генерации имеют приоритет.\n"
        + "\n".join(lines)
    )


def build_merchant_profile_image_guidance(profile: dict[str, Any] | None) -> str:
    lines = _filled_profile_lines(profile)
    if not lines:
        return ""
    return (
        "Профиль магазина: учитывай как устойчивые визуальные и текстовые предпочтения; "
        "явные пожелания текущей генерации имеют приоритет.\n"
        f"{MERCHANT_PROFILE_IMAGE_VISUAL_RULES}\n"
        + "\n".join(lines)
    )


def merge_merchant_profile_image_guidance(
    image_guidance: str | None,
    profile: dict[str, Any] | None,
) -> str:
    explicit_guidance = normalize_profile_value(image_guidance, limit=1200)
    profile_guidance = build_merchant_profile_image_guidance(profile)
    return "\n\n".join(part for part in (explicit_guidance, profile_guidance) if part)
