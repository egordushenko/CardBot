from __future__ import annotations

import re
from typing import Any

from llm import CardGeneration
from marketplace_rules import sanitize_description, sanitize_title


WB_FORBIDDEN_TITLE_WORDS = (
    "акция",
    "акци",
    "скидка",
    "скидк",
    "распродажа",
    "распродаж",
    "хит продаж",
    "лучший",
    "премиум",
    "идеальный",
)

WB_FORBIDDEN_DESCRIPTION_PHRASES = (
    "Представляем вашему вниманию",
    "Идеальный выбор для каждого",
    "Незаменимый помощник",
    "Высокое качество",
    "Премиальное качество",
    "Лучший подарок",
    "Хит продаж",
    "Успейте купить",
)


def parse_characteristics_text(value: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in value.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, field_value = line.split(":", 1)
        key = key.strip()
        field_value = field_value.strip()
        if key and field_value:
            result[key] = field_value
    return result


def _format_characteristics(fields: dict[str, str]) -> str:
    return "\n".join(f"{key}: {value}" for key, value in fields.items()).strip()


def _field_placeholder(field: str) -> str:
    return f"[укажите {field.casefold()}]"


def _remove_forbidden_title_words(title: str) -> str:
    cleaned = title
    for phrase in WB_FORBIDDEN_TITLE_WORDS:
        cleaned = re.sub(rf"(?iu)(?<!\w){re.escape(phrase)}\w*(?!\w)", "", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip(" ,.;:-")


def _remove_forbidden_description_phrases(description: str) -> str:
    cleaned = description
    for phrase in WB_FORBIDDEN_DESCRIPTION_PHRASES:
        cleaned = re.sub(re.escape(phrase), "", cleaned, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", cleaned).strip()


def _profile_fields(profile: dict[str, Any] | None, key: str) -> list[str]:
    if not profile:
        return []
    value = profile.get(key)
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def validate_wb_generation(
    card: CardGeneration,
    category_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    characteristics = parse_characteristics_text(card.characteristics)
    required = _profile_fields(category_profile, "required_characteristics")
    missing_required = [field for field in required if field not in characteristics]
    target_min = int((category_profile or {}).get("characteristics_target_min") or 8)
    issues: list[str] = []

    if len(card.title) > 60:
        issues.append("title_too_long")
    if card.keywords.strip():
        issues.append("wb_keywords_present")
    if missing_required:
        issues.append("missing_required_characteristics")
    if len(characteristics) < target_min:
        issues.append("too_few_characteristics")

    lowered_title = card.title.casefold()
    if any(phrase in lowered_title for phrase in WB_FORBIDDEN_TITLE_WORDS):
        issues.append("forbidden_title_words")

    return {
        "issues": issues,
        "characteristics_count": len(characteristics),
        "characteristics_target_min": target_min,
        "missing_required_characteristics": missing_required,
    }


def apply_wb_generation_quality(
    card: CardGeneration,
    category_profile: dict[str, Any] | None = None,
) -> CardGeneration:
    if card.marketplace != "wb":
        return card

    characteristics = parse_characteristics_text(card.characteristics)
    required = _profile_fields(category_profile, "required_characteristics")
    recommended = _profile_fields(category_profile, "recommended_characteristics")
    target_min = int((category_profile or {}).get("characteristics_target_min") or 8)

    for field in required:
        characteristics.setdefault(field, _field_placeholder(field))
    for field in recommended:
        if len(characteristics) >= target_min:
            break
        characteristics.setdefault(field, _field_placeholder(field))

    title = sanitize_title(_remove_forbidden_title_words(card.title), "wb")
    description = sanitize_description(
        _remove_forbidden_description_phrases(card.description),
        "wb",
    )

    return CardGeneration(
        title=title,
        description=description,
        keywords="",
        characteristics=_format_characteristics(characteristics),
        tokens_used=card.tokens_used,
        marketplace=card.marketplace,
    )
