from __future__ import annotations

from collections import Counter
from typing import Any

from llm import CardGeneration, normalize_marketplace
from ozon_generation_quality import _requires_grounding as _ozon_requires_grounding
from ozon_generation_quality import _user_mentions_field as _ozon_user_mentions_field
from ozon_generation_quality import _value_is_grounded as _ozon_value_is_grounded
from wb_generation_quality import _is_clothing_context
from wb_generation_quality import _requires_grounded_value as _wb_requires_grounded_value
from wb_generation_quality import _user_mentions_field as _wb_user_mentions_field
from wb_generation_quality import _value_is_grounded as _wb_value_is_grounded
from wb_generation_quality import infer_wb_clothing_composition, parse_characteristics_text


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
    "Длина предмета",
    "Глубина предмета",
}

FORBIDDEN_FIELD_MARKERS = (
    "упаков",
    "вес с упаков",
    "вес товара без упаков",
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


def _profile_fields(profile: dict[str, Any] | None, key: str) -> list[str]:
    value = (profile or {}).get(key)
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _characteristic_exists(characteristics: dict[str, str], field_marker: str) -> bool:
    marker = field_marker.casefold()
    return any(marker in field.casefold() for field in characteristics)


def _is_safe_default_value(
    field: str,
    value: str,
    *,
    marketplace: str,
    user_input: str,
    category_profile: dict[str, Any] | None,
    title: str,
) -> bool:
    field_lower = field.casefold()
    value_lower = value.casefold()
    if marketplace == "ozon" and field == "Страна-изготовитель" and value_lower == "китай":
        return True
    if marketplace == "wb" and field == "Страна производства" and value_lower == "китай":
        return True
    if marketplace == "wb" and field == "Состав":
        return value == infer_wb_clothing_composition(user_input, title, category_profile)
    if "комплектац" in field_lower:
        input_words = {
            word.strip(" ,.;:-").casefold()
            for word in user_input.split()
            if len(word.strip(" ,.;:-")) >= 4
        }
        value_words = {
            word.strip(" ,.;:-").casefold()
            for word in value.split()
            if len(word.strip(" ,.;:-")) >= 4
        }
        return bool(input_words & value_words)
    return False


def _is_hallucinated_fact(
    field: str,
    value: str,
    *,
    marketplace: str,
    user_input: str,
    category_profile: dict[str, Any] | None,
    title: str,
) -> bool:
    if marketplace == "ozon":
        requires_grounding = _ozon_requires_grounding(field)
        user_mentions = _ozon_user_mentions_field(user_input, field)
        value_is_grounded = _ozon_value_is_grounded(user_input, field, value)
    else:
        requires_grounding = _wb_requires_grounded_value(field)
        user_mentions = _wb_user_mentions_field(user_input, field)
        value_is_grounded = _wb_value_is_grounded(user_input, field, value)
    return (
        requires_grounding
        and (not user_mentions or not value_is_grounded)
        and not _is_safe_default_value(
            field,
            value,
            marketplace=marketplace,
            user_input=user_input,
            category_profile=category_profile,
            title=title,
        )
    )


def _target_min_characteristics(
    marketplace: str,
    category_profile: dict[str, Any] | None,
) -> int:
    target = MIN_CHARACTERISTICS[marketplace]
    if marketplace != "wb":
        return target
    try:
        profile_target = int((category_profile or {}).get("characteristics_target_min") or 0)
    except (TypeError, ValueError):
        profile_target = 0
    return max(target, profile_target)


def _add_missing_explicit_ozon_electronics_issues(
    issues: list[str],
    characteristics: dict[str, str],
    user_input: str,
    category_profile: dict[str, Any] | None,
) -> None:
    context = f"{user_input} {(category_profile or {}).get('category') or ''}".casefold()
    if not any(marker in context for marker in ("электроник", "наушник", "гарнитур")):
        return
    checks = (
        ("микрофон", "микрофон", "Наличие микрофона"),
        ("bluetooth", "беспроводной связи", "Тип беспроводной связи"),
        ("блютуз", "беспроводной связи", "Тип беспроводной связи"),
        ("шумоподав", "шумоподав", "Шумоподавление"),
        ("внутриканаль", "конструкция", "Конструкция наушников"),
        ("время работы", "время работы", "Время работы"),
    )
    for input_marker, field_marker, field_name in checks:
        if input_marker in context and not _characteristic_exists(characteristics, field_marker):
            issues.append(f"missing_explicit_characteristic:{field_name}")


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

    target_min = _target_min_characteristics(marketplace, category_profile)
    if len(characteristics) < target_min:
        issues.append("too_few_characteristics")
    if not _has_country(characteristics, marketplace):
        issues.append("missing_country")

    grounded_characteristics_count = 0
    for field, value in characteristics.items():
        field_is_forbidden = _is_forbidden_field(field)
        value_is_placeholder = _is_placeholder(value)
        value_is_hallucinated = _is_hallucinated_fact(
            field,
            value,
            marketplace=marketplace,
            user_input=user_input,
            category_profile=category_profile,
            title=card.title,
        )
        if field_is_forbidden:
            issues.append(f"forbidden_characteristic_field:{field}")
        if value_is_placeholder:
            issues.append(f"placeholder_characteristic_value:{field}")
        if value_is_hallucinated:
            issues.append(f"hallucinated_characteristic_value:{field}")
        if not field_is_forbidden and not value_is_placeholder and not value_is_hallucinated:
            grounded_characteristics_count += 1

    if marketplace == "wb" and grounded_characteristics_count < target_min:
        issues.append("too_few_grounded_characteristics")

    required = _profile_fields(category_profile, "required_generation_characteristics")
    if marketplace == "wb" and _is_clothing_context(user_input, card.title, category_profile):
        if "Состав" not in characteristics and (
            "Состав" in required or not required
        ):
            issues.append("missing_required_user_data:Состав")

    if marketplace == "wb" and card.keywords.strip():
        issues.append("wb_keywords_present")
    if marketplace == "ozon":
        hashtags = [item for item in card.keywords.split() if item.startswith("#")]
        if len(hashtags) < OZON_MIN_HASHTAGS:
            issues.append("ozon_too_few_hashtags")
        _add_missing_explicit_ozon_electronics_issues(
            issues,
            characteristics,
            user_input,
            category_profile,
        )

    return {
        "marketplace": marketplace,
        "title_length": len(card.title),
        "description_length": len(description),
        "characteristics_count": len(characteristics),
        "grounded_characteristics_count": grounded_characteristics_count,
        "characteristics_target_min": target_min,
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
