from __future__ import annotations

import re
from typing import Any

from llm import CardGeneration
from wb_generation_quality import parse_characteristics_text


OZON_DEFAULT_COUNTRY = "Китай"

OZON_DROP_FIELDS = {
    "Артикул",
    "Бренд",
    "Добавить к сравнению",
    "Китай",
    "Код ТРУ",
    "Литьевой",
    "Номер СГР",
    "Сертификат",
    "Bluetooth",
    "ISBN",
    "Автор",
    "Автор на обложке",
    "IMEI",
}

OZON_UNIVERSAL_FIELDS = {
    "Тип",
    "Цвет",
    "Материал",
    "Состав",
    "Размер",
    "Размеры",
    "Пол",
    "Совместимость",
    "Комплектация",
    "Страна-изготовитель",
    "Назначение",
    "Вес товара, г",
    "Длина, м",
    "Длина, см",
    "Длина, мм",
    "Ширина, м",
    "Ширина, см",
    "Ширина, мм",
    "Высота, м",
    "Высота, см",
    "Высота, мм",
    "Объем, мл",
    "Объем, л",
    "Мощность, Вт",
    "Количество в упаковке, шт",
    "Количество, шт",
}

OZON_BLOCKED_FIELD_MARKERS = (
    "упаков",
    "вес",
    "срок годности",
    "гарант",
    "сертификат",
    "номер сгр",
    "код тру",
    "артикул",
    "бренд",
)

OZON_GROUNDED_FIELD_MARKERS = (
    "материал",
    "состав",
    "размер",
    "длина",
    "ширина",
    "высота",
    "глубина",
    "вес",
    "объем",
    "объём",
    "мощность",
    "количество",
    "совместимость",
)

OZON_VALUE_LIKE_FIELD_RE = re.compile(
    r"^\d+(?:[.,]\d+)?(?:\s*(?:шт|г|кг|мл|л|см|мм|м|дней|месяц(?:ев|а)?|год(?:а)?))?$",
    re.IGNORECASE,
)
OZON_HASHTAGS_MIN = 12
OZON_HASHTAGS_MAX = 18


def _format_characteristics(fields: dict[str, str]) -> str:
    return "\n".join(f"{key}: {value}" for key, value in fields.items()).strip()


def _normalize_hashtag_key(tag: str) -> str:
    words = [word for word in tag.lstrip("#").casefold().split("_") if word]
    stop_words = {"для", "с", "со", "на", "в", "во", "комната", "комнаты"}
    words = [word for word in words if word not in stop_words]
    synonyms = {
        "ванны": "ванной",
        "душевой": "душа",
        "пол": "пола",
        "ворсом": "ворс",
        "впитывающий": "впитывающий",
        "влаговпитывающий": "впитывающий",
        "серый": "серый",
    }
    normalized = sorted(synonyms.get(word, word) for word in words)
    return "_".join(normalized)


def _trim_ozon_hashtags(value: str) -> str:
    tags = [tag.strip() for tag in value.split() if tag.strip().startswith("#")]
    kept: list[str] = []
    seen_tags: set[str] = set()
    seen_keys: set[str] = set()
    for tag in tags:
        lowered = tag.casefold()
        key = _normalize_hashtag_key(tag)
        if lowered in seen_tags or key in seen_keys:
            continue
        kept.append(tag)
        seen_tags.add(lowered)
        seen_keys.add(key)
        if len(kept) >= OZON_HASHTAGS_MAX:
            break
    return " ".join(kept)


def _profile_fields(profile: dict[str, Any] | None) -> set[str]:
    if not profile:
        return set()
    fields: set[str] = set()
    for key in ("prompt_characteristics", "top_characteristics"):
        value = profile.get(key)
        if isinstance(value, list):
            fields.update(str(item).strip() for item in value if str(item).strip())
    return fields


def _mentions_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _user_mentions_field(user_input: str, field: str) -> bool:
    field_lower = field.casefold()
    if "страна" in field_lower:
        return _mentions_any(user_input, (r"\bкитай\w*\b", r"\bросси\w*\b", r"\bтурци\w*\b", r"\bинд[иия]\w*\b", r"\bстрана\w*\b"))
    if "упаков" in field_lower:
        return _mentions_any(user_input, (r"\bупаков\w*\b", r"\bкоробк\w*\b", r"\bпачк\w*\b"))
    if "срок годности" in field_lower:
        return _mentions_any(user_input, (r"\bсрок\w*\s+годн\w*\b", r"\bгоден\b", r"\bмесяц\w*\b", r"\bдн(?:ей|я)\b"))
    if "гарант" in field_lower:
        return _mentions_any(user_input, (r"\bгарант\w*\b",))
    if "isbn" in field_lower:
        return _mentions_any(user_input, (r"\bisbn\b", r"\bисбн\b"))
    if "автор" in field_lower:
        return _mentions_any(user_input, (r"\bавтор\w*\b",))
    if "материал" in field_lower or "состав" in field_lower:
        return _mentions_any(user_input, (r"\bматериал\w*\b", r"\bсостав\w*\b", r"\bпластик\w*\b", r"\bметалл\w*\b", r"\bполиэстер\w*\b", r"\bхлоп\w*\b"))
    if "цвет" in field_lower:
        return _mentions_any(user_input, (r"\bцвет\w*\b", r"\bбел\w*\b", r"\bчерн\w*\b", r"\bсер\w*\b", r"\bкрасн\w*\b", r"\bсин\w*\b", r"\bзелен\w*\b"))
    if any(marker in field_lower for marker in ("размер", "длина", "ширина", "высота", "глубина")):
        return _mentions_any(user_input, (r"\b\d+\s*[xх×]\s*\d+", r"\b\d+\s*(см|мм|м)\b", r"\bразмер\w*\b", r"\bдлин\w*\b", r"\bширин\w*\b", r"\bвысот\w*\b"))
    if "вес" in field_lower:
        return _mentions_any(user_input, (r"\b\d+\s*(г|кг)\b", r"\bвес\w*\b"))
    if "объем" in field_lower or "объём" in field_lower:
        return _mentions_any(user_input, (r"\b\d+\s*(мл|л|литр)\w*\b", r"\bоб[ъь]ем\w*\b"))
    if "мощност" in field_lower:
        return _mentions_any(user_input, (r"\b\d+\s*(w|вт|ватт)\b", r"\bмощност\w*\b"))
    if "количество" in field_lower:
        return _mentions_any(user_input, (r"\b\d+\s*шт\b", r"\bколичеств\w*\b", r"\bкомплект\w*\b"))
    if "совместимость" in field_lower:
        return _mentions_any(user_input, (r"\bсовместим\w*\b", r"\bдля\s+[a-zа-я0-9 .-]+\b"))
    return False


def _infer_ozon_purpose(user_input: str) -> str:
    lowered = user_input.casefold()
    purposes: list[str] = []
    if "ванн" in lowered:
        purposes.append("для ванной комнаты")
    if "душев" in lowered or "душ" in lowered:
        purposes.append("душевой зоны")
    if "туалет" in lowered:
        purposes.append("туалета")
    if len(purposes) > 1:
        return ", ".join(purposes[:-1]) + " и " + purposes[-1]
    if purposes:
        return ", ".join(purposes)
    return ""


def _infer_ozon_kit(user_input: str) -> str:
    lowered = user_input.casefold()
    if "коврик" in lowered:
        return "коврик"
    if "рюкзак" in lowered:
        return "рюкзак"
    if "лампа" in lowered:
        return "лампа"
    return ""


def _is_blocked_field(field: str) -> bool:
    lowered = field.casefold()
    if field in OZON_DROP_FIELDS:
        return True
    if OZON_VALUE_LIKE_FIELD_RE.fullmatch(field.strip()):
        return True
    return any(marker in lowered for marker in OZON_BLOCKED_FIELD_MARKERS)


def _requires_grounding(field: str) -> bool:
    lowered = field.casefold()
    return any(marker in lowered for marker in OZON_GROUNDED_FIELD_MARKERS)


def _is_allowed_field(field: str, profile: dict[str, Any] | None) -> bool:
    return field in OZON_UNIVERSAL_FIELDS or field in _profile_fields(profile)


def apply_ozon_generation_quality(
    card: CardGeneration,
    category_profile: dict[str, Any] | None = None,
    user_input: str = "",
) -> CardGeneration:
    if card.marketplace != "ozon":
        return card

    normalized: dict[str, str] = {}
    for key, value in parse_characteristics_text(card.characteristics).items():
        clean_key = key.strip()
        clean_value = value.strip()
        if not clean_key or not clean_value:
            continue
        if _is_blocked_field(clean_key) and not _user_mentions_field(user_input, clean_key):
            continue
        if not _is_allowed_field(clean_key, category_profile):
            continue
        if _requires_grounding(clean_key) and not _user_mentions_field(user_input, clean_key):
            continue
        normalized[clean_key] = clean_value

    if "Страна-изготовитель" not in normalized:
        normalized["Страна-изготовитель"] = OZON_DEFAULT_COUNTRY
    if "Назначение" not in normalized:
        purpose = _infer_ozon_purpose(user_input)
        if purpose:
            normalized["Назначение"] = purpose
    if "Комплектация" not in normalized:
        kit = _infer_ozon_kit(user_input)
        if kit:
            normalized["Комплектация"] = kit

    return CardGeneration(
        title=card.title,
        description=card.description,
        keywords=_trim_ozon_hashtags(card.keywords),
        characteristics=_format_characteristics(normalized),
        tokens_used=card.tokens_used,
        marketplace=card.marketplace,
    )
