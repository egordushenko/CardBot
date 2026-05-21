from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULTS_PATH = BASE_DIR / "data" / "field_defaults.json"
RULES_PATH = BASE_DIR / "data" / "field_rules.json"
INSTRUCTION_KEY = "__prompt_instructions"


FIELD_NAMES: dict[str, dict[str, str]] = {
    "wb": {
        "brand": "Бренд",
        "article": "Артикул",
        "color": "Цвет",
        "composition": "Состав",
        "country": "Страна производства",
        "care_instructions": "Уход за вещами",
        "size": "Размер",
        "model_parameters": "Параметры модели",
        "gender": "Пол",
    },
    "ozon": {
        "brand": "Бренд",
        "article": "Артикул",
        "color": "Цвет",
        "composition": "Состав",
        "country": "Страна-изготовитель",
        "care_instructions": "Уход за вещами",
        "size": "Размер",
        "model_parameters": "Параметры модели",
        "gender": "Пол",
    },
}


def _normalize_marketplace(marketplace: str) -> str:
    normalized = marketplace.strip().lower()
    if normalized == "wildberries":
        return "wb"
    if normalized in {"wb", "ozon"}:
        return normalized
    raise ValueError(f"Unsupported marketplace: {marketplace}")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _user_value(user_input: dict[str, Any], field_key: str, field_name: str) -> str:
    for key in (field_key, field_name):
        value = user_input.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def _category_defaults(
    defaults: dict[str, Any],
    marketplace: str,
    category: str,
) -> dict[str, Any]:
    marketplace_defaults = defaults.get(marketplace)
    if not isinstance(marketplace_defaults, dict):
        return {}

    direct = marketplace_defaults.get(category)
    if isinstance(direct, dict):
        return direct

    category_lower = category.casefold()
    aliases: list[str] = []
    if marketplace == "wb":
        if "женск" in category_lower:
            aliases.append("Женщинам")
        if "мужск" in category_lower:
            aliases.append("Мужчинам")
        if "детск" in category_lower:
            aliases.append("Детям")
    for alias in aliases:
        alias_defaults = marketplace_defaults.get(alias)
        if isinstance(alias_defaults, dict):
            return alias_defaults

    generic = marketplace_defaults.get("Одежда")
    if isinstance(generic, dict) and "одеж" in category_lower:
        return generic
    return {}


def _infer_gender(category: str) -> str:
    category_lower = category.casefold()
    if "женск" in category_lower:
        return "Женский"
    if "мужск" in category_lower:
        return "Мужской"
    if "детск" in category_lower:
        return "Детский"
    return ""


def resolve_fields(
    user_input: dict[str, Any],
    category: str,
    marketplace: str,
    has_photo: bool,
) -> dict[str, Any]:
    normalized_marketplace = _normalize_marketplace(marketplace)
    rules = _read_json(RULES_PATH)
    defaults = _read_json(DEFAULTS_PATH)
    category_default_values = _category_defaults(defaults, normalized_marketplace, category)
    field_names = FIELD_NAMES[normalized_marketplace]

    resolved: dict[str, Any] = {}
    prompt_instructions: list[str] = []

    for field_key, rule in rules.items():
        field_name = field_names.get(field_key)
        if not field_name:
            continue

        explicit_value = _user_value(user_input, field_key, field_name)
        if explicit_value:
            resolved[field_name] = explicit_value
            continue

        if rule == "skip":
            continue
        if rule == "use_category_default":
            if normalized_marketplace == "wb":
                if field_name == "Страна производства":
                    resolved[field_name] = "Китай"
                continue
            default_value = category_default_values.get(field_name)
            if default_value is not None and str(default_value).strip():
                resolved[field_name] = str(default_value).strip()
            continue
        if rule == "extract_from_image_or_placeholder":
            if has_photo:
                prompt_instructions.append(
                    f"Если поле \"{field_name}\" не указано пользователем, извлеки цвет из изображения товара."
                )
            else:
                resolved[field_name] = f"[укажите {field_name.lower()}]"
            continue
        if rule == "infer_from_category":
            gender = _infer_gender(category)
            if gender:
                resolved[field_name] = gender
            continue

    if prompt_instructions:
        resolved[INSTRUCTION_KEY] = prompt_instructions
    return resolved
