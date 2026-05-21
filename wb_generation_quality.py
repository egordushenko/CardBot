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
    "стильный",
    "качественный",
    "лучшее",
)

WB_FORBIDDEN_DESCRIPTION_PHRASES = (
    "Представляем вашему вниманию",
    "Идеальный выбор для каждого",
    "Идеальный выбор",
    "Незаменимый помощник",
    "Высокое качество",
    "Премиальное качество",
    "Качественный материал",
    "Качественного материала",
    "Лучший подарок",
    "Хит продаж",
    "Успейте купить",
    "Стильная",
    "Стильный",
    "Стильное",
    "Лаконичный дизайн",
    "Для тех, кто ценит",
    "Для тех кто ценит",
)

WB_DROP_DESCRIPTION_SENTENCE_PATTERNS = (
    r"\bидеальн\w*\s+выбор\b",
    r"\bдля\s+тех,?\s+кто\s+ценит\b",
    r"\bлучший\s+подарок\b",
    r"\bхит\s+продаж\b",
    r"\bуспейте\s+купить\b",
)


WB_DEFAULT_COUNTRY = "Китай"

WB_SECONDARY_PLACEHOLDER_FIELDS = (
    "Длина упаковки",
    "Высота упаковки",
    "Ширина упаковки",
    "Размер упаковки",
    "Вес с упаковкой",
    "Вес товара с упаковкой",
    "Вес без упаковки",
    "Вес товара без упаковки",
    "Количество упаковок",
    "Поверхность",
    "Комплектация",
    "Требуется сборка",
)

WB_UNVERIFIED_DESCRIPTION_PATTERNS = {
    "material": (
        r"\bпластик\w*\b",
        r"\bметалл\w*\b",
        r"\bсиликон\w*\b",
        r"\bдерев\w*\b",
        r"\bполиэстер\w*\b",
        r"\bхлоп\w*\b",
        r"\bматериал\w*\b",
        r"\bкорпус выполнен\w*\b",
    ),
    "country": (
        r"\bстрана производств\w*\b",
        r"\bпроизвед[её]н\w*\b",
        r"\bсделан\w*\b",
    ),
    "kit": (
        r"\bкомплект\w*\b",
        r"\bв комплект\w*\b",
        r"\bне входит в комплект\w*\b",
        r"\bадаптер\w* не входит\w*\b",
    ),
    "warranty": (
        r"\bгаранти\w*\b",
        r"\bсертификат\w*\b",
    ),
    "assembly": (
        r"\bсборк\w*\b",
        r"\bсобран\w*\b",
    ),
    "packaging": (
        r"\bупаковк\w*\b",
        r"\bкоробк\w*\b",
    ),
}


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


def _is_placeholder(value: str) -> bool:
    return value.strip().startswith("[укажите")


def _mentions_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _user_mentions_country(user_input: str) -> bool:
    return _mentions_any(
        user_input,
        (
            r"\bкитай\w*\b",
            r"\bросси\w*\b",
            r"\bузбекистан\w*\b",
            r"\bтурци\w*\b",
            r"\bинд[иия]\w*\b",
            r"\bвьетнам\w*\b",
            r"\bтайван\w*\b",
            r"\bстрана производств\w*\b",
            r"\bпроизводств[ао]\s+[а-яёa-z-]+\b",
            r"\bсделан[ао]?\s+в\s+[а-яёa-z-]+\b",
        ),
    )


def _user_mentions_field(user_input: str, field: str) -> bool:
    field_lower = field.casefold()
    if "упаков" in field_lower or "вес с упаков" in field_lower:
        return _mentions_any(user_input, (r"\bупаковк\w*\b", r"\bкоробк\w*\b"))
    if "комплектац" in field_lower:
        return _mentions_any(user_input, (r"\bкомплект\w*\b", r"\bвходит\w*\b"))
    if "сборк" in field_lower:
        return _mentions_any(user_input, (r"\bсборк\w*\b", r"\bсобран\w*\b"))
    if "поверхност" in field_lower:
        return _mentions_any(user_input, (r"\bповерхност\w*\b", r"\bматов\w*\b", r"\bглянц\w*\b"))
    if "материал" in field_lower or "состав" in field_lower:
        return _mentions_any(
            user_input,
            (
                r"\bматериал\w*\b",
                r"\bпластик\w*\b",
                r"\bметалл\w*\b",
                r"\bсиликон\w*\b",
                r"\bдерев\w*\b",
                r"\bполиэстер\w*\b",
                r"\bхлоп\w*\b",
            ),
        )
    return field_lower in user_input.casefold()


def _is_secondary_placeholder_field(field: str) -> bool:
    field_lower = field.casefold()
    return any(marker.casefold() in field_lower for marker in WB_SECONDARY_PLACEHOLDER_FIELDS)


def _remove_forbidden_title_words(title: str) -> str:
    cleaned = title
    for phrase in WB_FORBIDDEN_TITLE_WORDS:
        cleaned = re.sub(rf"(?iu)(?<!\w){re.escape(phrase)}\w*(?!\w)", "", cleaned)
    cleaned = cleaned.replace(",", " ")
    return re.sub(r"\s+", " ", cleaned).strip(" ,.;:-")


def _remove_forbidden_description_phrases(description: str) -> str:
    kept_sentences = [
        sentence
        for sentence in _split_description_sentences(description)
        if not _mentions_any(sentence, WB_DROP_DESCRIPTION_SENTENCE_PATTERNS)
    ]
    cleaned = " ".join(kept_sentences) if kept_sentences else description
    for phrase in WB_FORBIDDEN_DESCRIPTION_PHRASES:
        cleaned = re.sub(re.escape(phrase), "", cleaned, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", cleaned).strip()


def _split_description_sentences(description: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", description.strip())
    return [part.strip() for part in parts if part.strip()]


def _remove_unverified_description_claims(
    description: str,
    user_input: str,
    characteristics: dict[str, str],
) -> str:
    if not user_input.strip():
        return description

    user_lower = user_input.casefold()
    existing = {key.casefold(): value for key, value in characteristics.items()}
    field_has_known_value = {
        "material": any(
            marker in key and not _is_placeholder(value)
            for key, value in existing.items()
            for marker in ("материал", "состав")
        ),
        "country": False,
        "kit": "комплектация" in existing and not _is_placeholder(existing["комплектация"]),
        "assembly": "требуется сборка" in existing and not _is_placeholder(existing["требуется сборка"]),
    }
    user_mentions = {
        "material": _user_mentions_field(user_input, "Материал изделия"),
        "country": _user_mentions_country(user_input),
        "kit": _user_mentions_field(user_input, "Комплектация"),
        "warranty": _mentions_any(user_input, (r"\bгаранти\w*\b", r"\bсертификат\w*\b")),
        "assembly": _user_mentions_field(user_input, "Требуется сборка"),
        "packaging": _mentions_any(user_lower, (r"\bупаковк\w*\b", r"\bкоробк\w*\b")),
    }

    kept: list[str] = []
    for sentence in _split_description_sentences(description):
        sentence_lower = sentence.casefold()
        should_drop = False
        for claim_type, patterns in WB_UNVERIFIED_DESCRIPTION_PATTERNS.items():
            if not _mentions_any(sentence_lower, patterns):
                continue
            if user_mentions.get(claim_type) or field_has_known_value.get(claim_type, False):
                continue
            should_drop = True
            break
        if not should_drop:
            kept.append(sentence)
    return " ".join(kept).strip() or description


def _normalize_wb_characteristics(
    characteristics: dict[str, str],
    required: list[str],
    recommended: list[str],
    target_min: int,
    user_input: str,
) -> dict[str, str]:
    normalized: dict[str, str] = {}
    country_explicit = _user_mentions_country(user_input)

    for key, value in characteristics.items():
        clean_key = key.strip()
        clean_value = value.strip()
        if not clean_key or not clean_value:
            continue
        if clean_key == "Страна производства" and not country_explicit:
            normalized[clean_key] = WB_DEFAULT_COUNTRY
            continue
        if clean_key == "Требуется сборка" and not _user_mentions_field(user_input, clean_key):
            continue
        if _is_placeholder(clean_value) and _is_secondary_placeholder_field(clean_key):
            continue
        normalized[clean_key] = clean_value

    normalized["Страна производства"] = (
        normalized.get("Страна производства") or WB_DEFAULT_COUNTRY
    )

    for field in required:
        if field == "Страна производства":
            normalized.setdefault(field, WB_DEFAULT_COUNTRY)
            continue
        if _is_secondary_placeholder_field(field) and not _user_mentions_field(user_input, field):
            continue
        normalized.setdefault(field, _field_placeholder(field))

    for field in recommended:
        if len(normalized) >= target_min:
            break
        if field == "Страна производства":
            normalized.setdefault(field, WB_DEFAULT_COUNTRY)
            continue
        if _is_secondary_placeholder_field(field) and not _user_mentions_field(user_input, field):
            continue
        normalized.setdefault(field, _field_placeholder(field))

    return normalized


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
    user_input: str = "",
) -> CardGeneration:
    if card.marketplace != "wb":
        return card

    characteristics = parse_characteristics_text(card.characteristics)
    required = _profile_fields(category_profile, "required_characteristics")
    recommended = _profile_fields(category_profile, "recommended_characteristics")
    target_min = int((category_profile or {}).get("characteristics_target_min") or 8)

    characteristics = _normalize_wb_characteristics(
        characteristics=characteristics,
        required=required,
        recommended=recommended,
        target_min=target_min,
        user_input=user_input,
    )

    title = sanitize_title(_remove_forbidden_title_words(card.title), "wb")
    description = sanitize_description(
        _remove_unverified_description_claims(
            _remove_forbidden_description_phrases(card.description),
            user_input=user_input,
            characteristics=characteristics,
        ),
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
