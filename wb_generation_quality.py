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

WB_DROP_CHARACTERISTIC_FIELDS = {
    "Состояние товара",
}

WB_ITEM_DIMENSION_FIELDS = {
    "Высота предмета",
    "Ширина предмета",
    "Длина предмета",
    "Глубина предмета",
}

WB_UNIVERSAL_CHARACTERISTIC_FIELDS = {
    "Цвет",
    "Пол",
    "Страна производства",
    "Комплектация",
    "Материал",
    "Материал изделия",
    "Состав",
    "Тип",
    "Вид",
    "Назначение",
    "Размер",
    "Размеры",
    "Вес",
    "Вес товара",
    "Объем",
    "Объем (л)",
    "Мощность",
    "Подключение",
    "Тип лампы",
    "Тип застежки",
    "Форма",
    "Покрой",
    "Сезон",
    "Количество предметов в упаковке",
}

WB_GENERATION_BLOCKED_FIELD_MARKERS = (
    "упаков",
    "вес с упаков",
    "вес товара с упаков",
    "рост модели",
    "параметры модели",
    "размер на модели",
    "imei",
    "сертификат",
    "гарантийный талон",
    "состояние товара",
)

WB_GROUNDED_VALUE_FIELD_MARKERS = (
    "цвет",
    "пол",
    "материал",
    "состав",
    "вес",
    "размер",
    "длина",
    "ширина",
    "высота",
    "объем",
    "мощность",
    "количество",
    "подключение",
    "тип лампы",
    "регулиров",
    "ярк",
    "покрой",
    "сезон",
    "застеж",
    "застёж",
    "форма",
)

WB_NUMERIC_VALUE_FIELDS = (
    "Высота предмета",
    "Ширина предмета",
    "Длина предмета",
    "Глубина предмета",
    "Вес товара",
    "Вес без упаковки",
    "Вес с упаковкой",
    "Длина упаковки",
    "Высота упаковки",
    "Ширина упаковки",
)

WB_SAFE_FIELD_ALIASES = {
    "Основной материал": "Материал",
}

WB_CLOTHING_PROFILE_MARKERS = (
    "женщинам",
    "мужчинам",
    "детям / одежда",
    "одежда",
    "футболка",
    "платье",
    "брюки",
    "худи",
    "кофта",
    "костюм",
)

WB_CLOTHING_TITLE_SIZE_RE = re.compile(
    r"(?<![A-Za-zА-Яа-яЁё0-9])(?:XXXS|XXS|XS|S|M|L|XL|XXL|XXXL|XXXXL)(?![A-Za-zА-Яа-яЁё0-9])",
    flags=re.IGNORECASE,
)

WB_CLOTHING_TITLE_MATERIAL_RE = re.compile(
    r"(?<![A-Za-zА-Яа-яЁё0-9])(?:\d{1,3}\s*%\s*)?"
    r"(?:хлопок|полиэстер|эластан|вискоза|нейлон|спандекс|лайкра)"
    r"(?:\s*\d{1,3}\s*%)?(?![A-Za-zА-Яа-яЁё0-9])",
    flags=re.IGNORECASE,
)

WB_CLOTHING_MATERIAL_WORDS = (
    "хлопок",
    "полиэстер",
    "эластан",
    "вискоза",
    "нейлон",
    "спандекс",
    "лайкра",
)

WB_CONTEXTUAL_FIELD_RULES: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (
        ("коврик", "ворс"),
        ("коврик", "ванн", "душ", "туалет"),
    ),
    (
        ("опрыскивател", "разбрызгивател", "объем бака", "механизм работы"),
        ("опрыскивател", "разбрызгивател", "сад", "дача"),
    ),
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


def _is_placeholder(value: str) -> bool:
    return value.strip().startswith("[укажите")


def _is_contextually_wrong_field(
    field: str,
    user_input: str,
    title: str,
    category_profile: dict[str, Any] | None,
) -> bool:
    field_lower = field.casefold()
    context = f"{user_input} {title} {(category_profile or {}).get('category') or ''}".casefold()
    for field_markers, context_markers in WB_CONTEXTUAL_FIELD_RULES:
        if any(marker in field_lower for marker in field_markers):
            return not any(marker in context for marker in context_markers)
    return False


def _has_digit(value: str) -> bool:
    return bool(re.search(r"\d", value))


def _mentions_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _number_tokens(text: str) -> set[str]:
    return {item.replace(",", ".") for item in re.findall(r"\d+(?:[,.]\d+)?", text)}


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
    if "мощност" in field_lower:
        return _mentions_any(user_input, (r"\b\d+\s*(w|вт|ватт)\b", r"\bмощност\w*\b"))
    if "объем" in field_lower or "объём" in field_lower:
        return _mentions_any(user_input, (r"\b\d+\s*(мл|л|литр)\w*\b", r"\bоб[ъь]ем\w*\b"))
    if "вес" in field_lower:
        return _mentions_any(user_input, (r"\b\d+(?:[,.]\d+)?\s*(г|кг)\b", r"\bвес\w*\b", r"\bупаковк\w*\s+\d+(?:[,.]\d+)?\s*(г|кг)\b"))
    if any(marker in field_lower for marker in ("размер", "длина", "ширина", "высота")):
        return _mentions_any(user_input, (r"\b\d+\s*[xх×]\s*\d+", r"\b\d+\s*(см|мм|м)\b", r"\bразмер\w*\b", r"\bдлин\w*\b", r"\bширин\w*\b", r"\bвысот\w*\b"))
    if "цвет" in field_lower:
        return _mentions_any(user_input, (r"\bцвет\w*\b", r"\bбел\w*\b", r"\bчерн\w*\b", r"\bсер\w*\b", r"\bкрасн\w*\b", r"\bсин\w*\b", r"\bзелен\w*\b", r"\bрозов\w*\b", r"\bбеж\w*\b", r"\bпрозрачн\w*\b"))
    if "пол" in field_lower:
        return _mentions_any(user_input, (r"\bженск\w*\b", r"\bмужск\w*\b", r"\bдетск\w*\b", r"\bдевоч\w*\b", r"\bмальчик\w*\b"))
    if "тип лампы" in field_lower:
        return _mentions_any(user_input, (r"\bled\b", r"\bсветодиод\w*\b", r"\bнакаливан\w*\b", r"\bгалоген\w*\b"))
    if "подключение" in field_lower:
        return _mentions_any(user_input, (r"\busb\b", r"\btype-c\b", r"\bтайп-с\b", r"\bсеть\b", r"\bрозетк\w*\b", r"\bаккумулятор\w*\b"))
    if "регулиров" in field_lower or "ярк" in field_lower:
        return _mentions_any(user_input, (r"\bрегулиров\w*\b", r"\bяркост\w*\b", r"\bдиммер\w*\b"))
    if "застеж" in field_lower or "застёж" in field_lower:
        return _mentions_any(user_input, (r"\bмолни\w*\b", r"\bзаст[её]ж\w*\b", r"\bлипуч\w*\b", r"\bкнопк\w*\b"))
    if "покрой" in field_lower:
        return _mentions_any(user_input, (r"\bоверсайз\b", r"\bсвободн\w*\b", r"\bпритал\w*\b"))
    if "сезон" in field_lower:
        return _mentions_any(user_input, (r"\bсезон\w*\b", r"\bлет\w*\b", r"\bзим\w*\b", r"\bдемисезон\w*\b", r"\bвсесезон\w*\b"))
    if "форма" in field_lower:
        return _mentions_any(user_input, (r"\bформ\w*\b", r"\bпрямоугольн\w*\b", r"\bкругл\w*\b", r"\bовальн\w*\b", r"\b\d+\s*(?:[xх×]|на)\s*\d+"))
    return False


def _value_is_grounded(user_input: str, field: str, value: str) -> bool:
    field_lower = field.casefold()
    user_lower = user_input.casefold()
    value_lower = value.casefold()
    value_numbers = _number_tokens(value_lower)
    if value_numbers:
        return value_numbers <= _number_tokens(user_lower)
    if value_lower in {"да", "есть"}:
        return _user_mentions_field(user_input, field)
    if value_lower == "нет":
        return _mentions_any(user_lower, (r"\bнет\b", r"\bне\s+\w+", r"\bбез\b"))
    if "цвет" in field_lower:
        for color_pattern in (
            r"бел\w*",
            r"черн\w*",
            r"сер\w*",
            r"красн\w*",
            r"син\w*",
            r"зелен\w*",
            r"розов\w*",
            r"беж\w*",
            r"прозрачн\w*",
        ):
            if re.search(color_pattern, value_lower) and not re.search(color_pattern, user_lower):
                return False
        return True
    if "пол" in field_lower:
        for gender_pattern in (r"женск\w*", r"мужск\w*", r"детск\w*", r"девоч\w*", r"мальчик\w*"):
            if re.search(gender_pattern, value_lower) and re.search(gender_pattern, user_lower):
                return True
        return False
    if "покрой" in field_lower and "свобод" in value_lower:
        return _mentions_any(user_lower, (r"\bсвободн\w*\b", r"\bоверсайз\b"))
    if "сезон" in field_lower:
        return any(
            re.search(pattern, value_lower) and re.search(pattern, user_lower)
            for pattern in (r"лет\w*", r"зим\w*", r"демисезон\w*", r"всесезон\w*")
        )
    if "форма" in field_lower:
        if _mentions_any(user_lower, (r"\b\d+\s*(?:[xх×]|на)\s*\d+",)) and _mentions_any(value_lower, (r"\bпрямоугольн\w*\b",)):
            return True
        return any(
            re.search(pattern, value_lower) and re.search(pattern, user_lower)
            for pattern in (r"прямоугольн\w*", r"кругл\w*", r"овальн\w*")
        )
    if "подключение" in field_lower or "тип лампы" in field_lower:
        return any(
            re.search(pattern, value_lower) and re.search(pattern, user_lower)
            for pattern in (r"usb", r"type-c", r"bluetooth", r"блютуз", r"led", r"светодиод\w*", r"аккумулятор\w*", r"сеть")
        )
    if "регулиров" in field_lower or "ярк" in field_lower:
        return _user_mentions_field(user_input, field)
    value_words = {word for word in re.findall(r"[a-zа-яё0-9]+", value_lower) if len(word) >= 4}
    return any(word in user_lower for word in value_words)


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
        if _mentions_any(sentence_lower, (r"\bне\s+входит\s+в\s+комплект\b",)) and not user_mentions["kit"]:
            continue
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
    user_input: str,
    title: str,
    category_profile: dict[str, Any] | None,
) -> dict[str, str]:
    normalized: dict[str, str] = {}
    country_explicit = _user_mentions_country(user_input)

    for key, value in characteristics.items():
        clean_key = key.strip()
        clean_value = value.strip()
        if not clean_key or not clean_value:
            continue
        clean_key = WB_SAFE_FIELD_ALIASES.get(clean_key, clean_key)
        if clean_key in WB_ITEM_DIMENSION_FIELDS:
            alternative = _clothing_dimension_alternative(
                clean_key,
                clean_value,
                user_input=user_input,
                title=title,
                category_profile=category_profile,
            )
            if alternative:
                alt_key, alt_value = alternative
                normalized.setdefault(alt_key, alt_value)
                continue
            if _has_digit(clean_value) and _user_mentions_field(user_input, clean_key):
                normalized.setdefault("Размер", clean_value)
            continue
        if clean_key in WB_DROP_CHARACTERISTIC_FIELDS:
            continue
        if _is_contextually_wrong_field(clean_key, user_input, title, category_profile):
            continue
        if _is_blocked_generation_field(clean_key) and not _user_mentions_field(user_input, clean_key):
            continue
        if _requires_numeric_value(clean_key) and not _has_digit(clean_value):
            alternative = _clothing_dimension_alternative(
                clean_key,
                clean_value,
                user_input=user_input,
                title=title,
                category_profile=category_profile,
            )
            if alternative:
                alt_key, alt_value = alternative
                normalized.setdefault(alt_key, alt_value)
            continue
        if not _is_allowed_wb_characteristic(clean_key, clean_value, user_input, category_profile):
            continue
        if clean_key == "Страна производства" and not country_explicit:
            normalized[clean_key] = WB_DEFAULT_COUNTRY
            continue
        if clean_key == "Требуется сборка" and not _user_mentions_field(user_input, clean_key):
            continue
        if _requires_grounded_value(clean_key) and not _user_mentions_field(user_input, clean_key):
            continue
        if _requires_grounded_value(clean_key) and not _value_is_grounded(user_input, clean_key, clean_value):
            continue
        if _is_placeholder(clean_value):
            continue
        normalized[clean_key] = clean_value

    normalized["Страна производства"] = (
        normalized.get("Страна производства") or WB_DEFAULT_COUNTRY
    )
    inferred_composition = infer_wb_clothing_composition(user_input, title, category_profile)
    if inferred_composition and "Состав" not in normalized:
        normalized["Состав"] = inferred_composition
    inferred_kit = _infer_wb_kit(user_input, title)
    if inferred_kit and "Комплектация" not in normalized:
        normalized["Комплектация"] = inferred_kit
    normalized.update(_infer_wb_pet_food_characteristics(user_input))
    _drop_redundant_generic_size(normalized)
    _drop_duplicate_clothing_material(normalized, user_input, title, category_profile)

    return normalized


def infer_wb_clothing_composition(
    user_input: str,
    title: str,
    category_profile: dict[str, Any] | None,
) -> str:
    if not _is_clothing_context(user_input, title, category_profile):
        return ""
    text = f"{user_input} {title}".casefold()
    if not _mentions_any(text, (r"\bфутболк\w*\b", r"\bмайк\w*\b", r"\bлонгслив\w*\b", r"\bтоп\b")):
        if _mentions_any(text, (r"\bхуди\b", r"\bтолстовк\w*\b", r"\bсвитшот\w*\b")):
            return "хлопок 80%, полиэстер 20%"
        if _mentions_any(text, (r"\bплать\w*\b", r"\bбрюк\w*\b", r"\bкостюм\w*\b", r"\bюбк\w*\b")):
            return "полиэстер 95%, эластан 5%"
        return "хлопок 95%, эластан 5%"
    return "100% хлопок"


def _requires_numeric_value(field: str) -> bool:
    field_lower = field.casefold()
    return any(marker.casefold() in field_lower for marker in WB_NUMERIC_VALUE_FIELDS)


def _is_blocked_generation_field(field: str) -> bool:
    field_lower = field.casefold()
    return any(marker in field_lower for marker in WB_GENERATION_BLOCKED_FIELD_MARKERS)


def _requires_grounded_value(field: str) -> bool:
    field_lower = field.casefold()
    return any(marker in field_lower for marker in WB_GROUNDED_VALUE_FIELD_MARKERS)


def _allowed_profile_fields(profile: dict[str, Any] | None) -> set[str]:
    fields: set[str] = set()
    for key in (
        "prompt_characteristics",
        "required_generation_characteristics",
        "recommended_generation_characteristics",
    ):
        fields.update(_profile_fields(profile, key))
    if not fields:
        fields.update(_profile_fields(profile, "required_characteristics"))
        fields.update(_profile_fields(profile, "recommended_characteristics"))
    return {field for field in fields if field and not _is_blocked_generation_field(field)}


def _is_allowed_wb_characteristic(
    field: str,
    value: str,
    user_input: str,
    category_profile: dict[str, Any] | None,
) -> bool:
    if field in WB_UNIVERSAL_CHARACTERISTIC_FIELDS:
        return True
    if field in _allowed_profile_fields(category_profile):
        return True
    if _requires_numeric_value(field) and _has_digit(value) and _user_mentions_field(user_input, field):
        return True
    return False


def _is_clothing_context(
    user_input: str,
    title: str,
    category_profile: dict[str, Any] | None,
) -> bool:
    category = str((category_profile or {}).get("category") or "")
    text = f"{category} {title} {user_input}".casefold()
    return any(marker in text for marker in WB_CLOTHING_PROFILE_MARKERS)


def _remove_clothing_title_noise(
    title: str,
    user_input: str,
    category_profile: dict[str, Any] | None,
) -> str:
    if not _is_clothing_context(user_input, title, category_profile):
        return title
    cleaned = WB_CLOTHING_TITLE_SIZE_RE.sub(" ", title)
    cleaned = WB_CLOTHING_TITLE_MATERIAL_RE.sub(" ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip(" ,.;:-")


def _drop_duplicate_clothing_material(
    normalized: dict[str, str],
    user_input: str,
    title: str,
    category_profile: dict[str, Any] | None,
) -> None:
    if not _is_clothing_context(user_input, title, category_profile):
        return
    composition = normalized.get("Состав", "").casefold()
    if not composition:
        return
    for material_field in ("Материал изделия", "Материал"):
        material = normalized.get(material_field, "").casefold()
        if not material:
            continue
        if any(word in composition and word in material for word in WB_CLOTHING_MATERIAL_WORDS):
            normalized.pop(material_field, None)


def _clothing_dimension_alternative(
    field: str,
    value: str,
    user_input: str,
    title: str,
    category_profile: dict[str, Any] | None,
) -> tuple[str, str] | None:
    if not _is_clothing_context(user_input, title, category_profile):
        return None
    if "ширина предмета" not in field.casefold():
        return None
    value_lower = value.casefold()
    if "свобод" in value_lower:
        return ("Покрой", "свободный")
    if "оверсайз" in value_lower or "oversize" in value_lower:
        return ("Покрой", "оверсайз")
    return None


def _infer_product_name_for_kit(title: str, user_input: str) -> str:
    source = title.strip() or user_input.strip()
    words = [
        word.strip(" ,.;:-")
        for word in source.split()
        if word.strip(" ,.;:-")
    ]
    if not words:
        return "товар"
    stop_words = {
        "usb",
        "led",
        "rgb",
        "белая",
        "белый",
        "черная",
        "черный",
        "красная",
        "красный",
        "35",
        "см",
    }
    product_words: list[str] = []
    for word in words:
        lowered = word.casefold()
        if lowered in stop_words or re.fullmatch(r"\d+[a-zа-яё]*", lowered):
            if product_words:
                break
            continue
        product_words.append(word)
        if len(product_words) >= 2:
            break
    return " ".join(product_words) if product_words else words[0]


def _infer_wb_kit(user_input: str, title: str) -> str:
    if not _mentions_any(user_input, (r"\busb\b", r"\bюсб\b", r"\btype-c\b", r"\bтайп-с\b")):
        return ""
    if _mentions_any(user_input, (r"\bбез\s+кабел\w*\b", r"\bкабел\w*\s+не\s+входит\b")):
        return ""
    product = _infer_product_name_for_kit(title, user_input)
    return f"{product}; USB-кабель"


def _infer_wb_pet_food_characteristics(user_input: str) -> dict[str, str]:
    text = user_input.casefold()
    if "корм" not in text or not _mentions_any(text, (r"\bкош\w*\b", r"\bкот\w*\b", r"\bсобак\w*\b", r"\bщен\w*\b")):
        return {}

    inferred: dict[str, str] = {}
    if "сухой корм" in text:
        inferred["Тип"] = "сухой корм"
    elif "влажный корм" in text:
        inferred["Тип"] = "влажный корм"
    elif "корм" in text:
        inferred["Тип"] = "корм"

    if _mentions_any(text, (r"\bкош\w*\b", r"\bкот\w*\b")):
        inferred["Вид животного"] = "кошки"
    elif _mentions_any(text, (r"\bсобак\w*\b", r"\bщен\w*\b")):
        inferred["Вид животного"] = "собаки"

    weight_match = re.search(r"\b(\d+(?:[,.]\d+)?)\s*(кг|г)\b", text)
    if weight_match:
        inferred["Вес"] = f"{weight_match.group(1).replace(',', '.')} {weight_match.group(2)}"

    if "куриц" in text:
        inferred["Вкус"] = "курица"
    elif "говядин" in text:
        inferred["Вкус"] = "говядина"
    elif "лосос" in text:
        inferred["Вкус"] = "лосось"
    elif "индейк" in text:
        inferred["Вкус"] = "индейка"

    return inferred


def _drop_redundant_generic_size(characteristics: dict[str, str]) -> None:
    generic_size = characteristics.get("Размер")
    if not generic_size:
        return
    generic_lower = generic_size.casefold()
    for key, value in characteristics.items():
        if key == "Размер" or "размер" not in key.casefold():
            continue
        value_lower = value.casefold()
        if "x" in value_lower or "х" in value_lower or "×" in value_lower:
            del characteristics["Размер"]
            return
        if generic_lower and generic_lower in value_lower and value_lower != generic_lower:
            del characteristics["Размер"]
            return


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
    required = (
        _profile_fields(category_profile, "required_generation_characteristics")
        or _profile_fields(category_profile, "prompt_characteristics")
        or _profile_fields(category_profile, "required_characteristics")
    )
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
    characteristics = _normalize_wb_characteristics(
        characteristics=characteristics,
        user_input=user_input,
        title=card.title,
        category_profile=category_profile,
    )

    title = sanitize_title(
        _remove_clothing_title_noise(
            _remove_forbidden_title_words(card.title),
            user_input=user_input,
            category_profile=category_profile,
        ),
        "wb",
    )
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
