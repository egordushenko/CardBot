from __future__ import annotations

from collections import Counter
from typing import Any

from llm import CardGeneration, normalize_marketplace
from wb_generation_quality import parse_characteristics_text


DESCRIPTION_MIN_CHARS = {
    "wb": 300,
    "ozon": 700,
}

DESCRIPTION_MAX_CHARS = {
    "wb": 1800,
    "ozon": 2200,
}

MIN_CHARACTERISTICS = {
    "wb": 4,
    "ozon": 4,
}

OZON_MIN_HASHTAGS = 3

FORBIDDEN_CHARACTERISTIC_FIELDS = {
    "Артикул",
    "Бренд",
    "Добавить к сравнению",
    "Китай",
    "Литьевой",
    "Bluetooth",
    "IMEI",
    "Сертификат",
    "Номер СГР",
    "Состояние товара",
    "Ширина предмета",
    "Высота предмета",
}

FORBIDDEN_FIELD_MARKERS = (
    "упаков",
    "вес с упаков",
    "сертификат",
    "гарант",
    "артикул",
)

PLACEHOLDER_PREFIXES = (
    "[укажите",
    "укажите ",
)

SELLING_CUE_WORDS = (
    "подходит",
    "помогает",
    "удоб",
    "комфорт",
    "защищ",
    "сочета",
    "использ",
    "для ",
    "можно",
)


def _has_selling_cues(description: str) -> bool:
    lowered = description.casefold()
    return sum(1 for cue in SELLING_CUE_WORDS if cue in lowered) >= 2


def _is_forbidden_field(field: str) -> bool:
    lowered = field.casefold()
    if field in FORBIDDEN_CHARACTERISTIC_FIELDS:
        return True
    return any(marker in lowered for marker in FORBIDDEN_FIELD_MARKERS)


def _is_placeholder(value: str) -> bool:
    lowered = value.strip().casefold()
    return any(lowered.startswith(prefix) for prefix in PLACEHOLDER_PREFIXES)


def _has_country(characteristics: dict[str, str], marketplace: str) -> bool:
    country_field = "Страна-изготовитель" if marketplace == "ozon" else "Страна производства"
    return bool(characteristics.get(country_field, "").strip())


def evaluate_card_quality(
    card: CardGeneration,
    user_input: str = "",
    category_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    marketplace = normalize_marketplace(card.marketplace)
    characteristics = parse_characteristics_text(card.characteristics)
    issues: list[str] = []

    if not card.title.strip():
        issues.append("missing_title")
    title_limit = 200 if marketplace == "ozon" else 60
    if len(card.title) > title_limit:
        issues.append("title_too_long")

    description = card.description.strip()
    if len(description) < DESCRIPTION_MIN_CHARS[marketplace]:
        issues.append("description_too_short")
    if len(description) > DESCRIPTION_MAX_CHARS[marketplace]:
        issues.append("description_too_long")
    if description and not _has_selling_cues(description):
        issues.append("description_too_dry")

    if len(characteristics) < MIN_CHARACTERISTICS[marketplace]:
        issues.append("too_few_characteristics")
    if not _has_country(characteristics, marketplace):
        issues.append("missing_country")

    for field, value in characteristics.items():
        if _is_forbidden_field(field):
            issues.append(f"forbidden_characteristic_field:{field}")
        if _is_placeholder(value):
            issues.append(f"placeholder_characteristic_value:{field}")

    if marketplace == "wb" and card.keywords.strip():
        issues.append("wb_keywords_present")
    if marketplace == "ozon":
        hashtags = [item for item in card.keywords.split() if item.startswith("#")]
        if len(hashtags) < OZON_MIN_HASHTAGS:
            issues.append("ozon_too_few_hashtags")

    return {
        "marketplace": marketplace,
        "title_length": len(card.title),
        "description_length": len(description),
        "characteristics_count": len(characteristics),
        "score": max(0, 100 - len(set(issues)) * 10),
        "issues": sorted(set(issues)),
    }


def summarize_quality_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    issue_counts = Counter(
        issue
        for result in results
        for issue in result.get("issues", [])
    )
    failed = sum(1 for result in results if result.get("issues"))
    return {
        "total": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "issue_counts": dict(sorted(issue_counts.items())),
        "avg_score": round(
            sum(float(result.get("score", 0)) for result in results) / len(results),
            1,
        )
        if results
        else 0,
    }
