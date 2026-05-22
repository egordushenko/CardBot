from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CATEGORY_PROFILES_PATH = BASE_DIR / "data" / "category_profiles.json"
DEFAULT_WB_CATEGORY_PROFILES_PATH = BASE_DIR / "data" / "wb_category_profiles.json"
DEFAULT_WB_CATEGORIES_PATH = BASE_DIR / "data" / "wb_categories.json"
DEFAULT_OZON_CATEGORIES_PATH = BASE_DIR / "data" / "ozon_categories_full.json"


def load_category_profiles(
    path: str | Path = DEFAULT_CATEGORY_PROFILES_PATH,
) -> dict[str, dict[str, Any]]:
    profile_path = Path(path)
    if not profile_path.exists():
        return {}

    raw = json.loads(profile_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}

    profiles: dict[str, dict[str, Any]] = {}
    for category, profile in raw.items():
        if not isinstance(category, str) or not isinstance(profile, dict):
            continue
        profile_copy = dict(profile)
        profile_copy["category"] = category
        profiles[category] = profile_copy
    return profiles


def load_wb_category_profiles(
    path: str | Path = DEFAULT_WB_CATEGORY_PROFILES_PATH,
) -> dict[str, dict[str, Any]]:
    return load_category_profiles(path)


def load_wb_categories(path: str | Path = DEFAULT_WB_CATEGORIES_PATH) -> dict[str, Any]:
    categories_path = Path(path)
    if not categories_path.exists():
        return {"categories": []}
    raw = json.loads(categories_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {"categories": []}
    categories = raw.get("categories")
    if not isinstance(categories, list):
        raw["categories"] = []
    return raw


def load_ozon_categories(path: str | Path = DEFAULT_OZON_CATEGORIES_PATH) -> dict[str, Any]:
    categories_path = Path(path)
    if not categories_path.exists():
        return {"categories": []}
    raw = json.loads(categories_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {"categories": []}
    categories = raw.get("categories")
    if not isinstance(categories, list):
        raw["categories"] = []
    return raw


def get_category_profile(
    profiles: dict[str, dict[str, Any]],
    category: str,
) -> dict[str, Any] | None:
    profile = profiles.get(category)
    if not profile:
        return None

    profile_copy = dict(profile)
    profile_copy["category"] = category
    return profile_copy


WB_GENERIC_MATCH_TOKENS = {
    "для",
    "дом",
    "дома",
    "товар",
    "товары",
    "каталог",
    "одежда",
    "черный",
    "черная",
    "черные",
    "белый",
    "белая",
    "белые",
    "серый",
    "серая",
    "серые",
    "красный",
    "красная",
    "синий",
    "синяя",
    "зеленый",
    "зеленая",
    "женский",
    "женская",
    "женские",
    "мужской",
    "мужская",
    "мужские",
    "городской",
    "городская",
    "базовый",
    "базовая",
    "новый",
    "новая",
    "город",
    "города",
    "под",
}

WB_CLOTHING_PRODUCT_TOKENS = {
    "футболка",
    "футболки",
    "платье",
    "платья",
    "брюки",
    "куртка",
    "куртки",
    "костюм",
    "костюмы",
    "худи",
    "кофта",
    "кофты",
    "рубашка",
    "рубашки",
    "шорты",
    "юбка",
    "юбки",
}

WB_SHOES_PRODUCT_TOKENS = {
    "кроссовки",
    "кроссовок",
    "кеды",
    "ботинки",
    "туфли",
    "сапоги",
    "сандалии",
    "босоножки",
    "лоферы",
    "тапочки",
    "обувь",
}

WB_BACKPACK_PRODUCT_TOKENS = {
    "рюкзак",
    "рюкзаки",
    "ранец",
    "портфель",
}

WB_LIGHTING_PRODUCT_TOKENS = {
    "лампа",
    "лампы",
    "светильник",
    "ночник",
    "led",
}

WB_PET_PRODUCT_TOKENS = {
    "корм",
    "кошек",
    "кошки",
    "кота",
    "котят",
    "собак",
    "собаки",
    "щенков",
    "питомцев",
}


def _tokens(value: str) -> set[str]:
    return {
        token.casefold()
        for token in re.findall(r"[A-Za-zА-Яа-яЁё0-9]+", value)
        if len(token) >= 3 and not token.isdigit()
    }


def _token_matches(token: str, text: str, text_tokens: set[str]) -> bool:
    token = token.strip().casefold()
    if len(token) < 3 or token in WB_GENERIC_MATCH_TOKENS:
        return False
    if token in text_tokens:
        return True
    if len(token) >= 5 and any(item.startswith(token[:5]) or token.startswith(item[:5]) for item in text_tokens):
        return True
    return token in text


def _profile_depth(profile: dict[str, Any]) -> int:
    category = str(profile.get("category") or "")
    return len([part for part in category.split(" / ") if part.strip()])


WB_PARENT_ALIASES = {
    "Зоотовары": ("Зоотовары", "Товары для животных"),
    "Канцтовары": ("Канцтовары", "Канцелярские товары", "Канцелярия"),
    "Продукты": ("Продукты", "Продукты питания"),
    "Спорт": ("Спорт", "Спортивные товары"),
    "Для ремонта": ("Для ремонта", "Строительство и ремонт"),
}

WB_SYNTHETIC_FALLBACK_PROFILES: dict[str, dict[str, Any]] = {
    "Товары для животных": {
        "marketplace": "wb",
        "category": "Товары для животных",
        "parent_category": "Товары для животных",
        "match_keywords": ["корм", "кошка", "собака", "питомец"],
        "prompt_characteristics": [
            "Тип",
            "Вид животного",
            "Вес",
            "Вкус",
            "Назначение",
            "Комплектация",
            "Страна производства",
        ],
        "required_generation_characteristics": ["Тип", "Вид животного", "Страна производства"],
        "recommended_generation_characteristics": ["Вес", "Вкус", "Назначение", "Комплектация"],
        "characteristics_target_min": 5,
        "characteristics_target_max": 8,
        "title_target_min": 32,
        "title_target_max": 60,
        "description_target_min": 900,
        "description_target_max": 1500,
    },
    "Спорт": {
        "marketplace": "wb",
        "category": "Спорт",
        "parent_category": "Спорт",
        "match_keywords": ["коврик", "йога", "фитнес", "спорт", "тренировка"],
        "prompt_characteristics": [
            "Тип",
            "Цвет",
            "Размер",
            "Материал",
            "Назначение",
            "Комплектация",
            "Страна производства",
        ],
        "required_generation_characteristics": ["Тип", "Цвет", "Страна производства"],
        "recommended_generation_characteristics": ["Размер", "Материал", "Назначение", "Комплектация"],
        "characteristics_target_min": 5,
        "characteristics_target_max": 8,
        "title_target_min": 32,
        "title_target_max": 60,
        "description_target_min": 900,
        "description_target_max": 1500,
    },
}

WB_PROFILE_FIELD_DROP_MARKERS = (
    "упаков",
    "гарант",
    "партномер",
    "артикул",
    "сертификат",
    "толщина предмета",
    "длина предмета",
    "ширина предмета",
    "высота предмета",
)

WB_CONTEXT_PROFILE_FIELD_RULES: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (("коврик", "ворс"), ("коврик", "ванн", "душ", "туалет")),
    (("опрыскивател", "разбрызгивател", "объем бака"), ("опрыскивател", "разбрызгивател", "сад", "дача")),
)


def _category_depth(category: str) -> int:
    return len([part for part in category.split(" / ") if part.strip()])


def _catalog_category_score(item: dict[str, Any], product_description: str) -> int:
    text = product_description.casefold()
    text_tokens = _tokens(product_description)
    path = str(item.get("path") or "")
    name = str(item.get("name") or "")
    score = 0

    path_tokens = _tokens(path)
    name_tokens = _tokens(name)
    for token in path_tokens:
        if _token_matches(token, text, text_tokens):
            score += 3
    for token in name_tokens:
        if _token_matches(token, text, text_tokens):
            score += 3

    path_lower = path.casefold()
    lexical_score = score
    semantic_score = 0
    has_female_marker = bool(text_tokens & {"женская", "женские", "женский", "женское"})
    has_male_marker = bool(text_tokens & {"мужская", "мужские", "мужской", "мужское"})
    has_kids_marker = bool(text_tokens & {"детская", "детские", "детский", "детское", "ребенок", "малыш"})
    has_shoes_product = bool(text_tokens & WB_SHOES_PRODUCT_TOKENS)
    has_clothing_product = bool(text_tokens & WB_CLOTHING_PRODUCT_TOKENS)

    if has_shoes_product and path_lower.startswith("обувь"):
        semantic_score += 25
    if has_shoes_product and (path_lower.startswith("женщинам") or path_lower.startswith("мужчинам")):
        semantic_score -= 15
    if bool(text_tokens & WB_BACKPACK_PRODUCT_TOKENS) and path_lower.startswith("аксессуары"):
        semantic_score += 25
    if bool(text_tokens & WB_BACKPACK_PRODUCT_TOKENS) and path_lower.startswith("для ремонта"):
        semantic_score -= 25

    if "ламп" in text and "настольные лампы" in path_lower:
        semantic_score += 20
    elif "ламп" in text and "освещение" in path_lower:
        semantic_score += 10
    if "блендер" in text and path_lower.startswith("бытовая техника"):
        semantic_score += 20
    if "органайзер" in text and "хранение вещей" in path_lower:
        semantic_score += 20
    if "органайзер" in text and path_lower.startswith("дом"):
        semantic_score += 20
    if "органайзер" in text and path_lower.startswith("игрушки"):
        semantic_score -= 20
    if "коврик" in text and "йог" in text and path_lower.startswith("спорт"):
        semantic_score += 20
    if "коврик" in text and any(marker in text for marker in ("ванн", "душ", "туалет")) and "ванная" in path_lower:
        semantic_score += 20
    if "корм" in text and any(marker in text for marker in ("кош", "собак", "питом")) and path_lower.startswith("зоотовары"):
        semantic_score += 20
    if any(marker in text for marker in ("витамин", "бад", "капсул", "омега")) and path_lower.startswith("здоровье"):
        semantic_score += 25
    if any(marker in text for marker in ("витамин", "бад", "капсул", "омега")) and path_lower.startswith("мебель"):
        semantic_score -= 25
    if "смартфон" in text and path_lower.endswith(" / смартфоны"):
        semantic_score += 80
    if "смартфон" in text and "смартфоны" in path_lower:
        semantic_score += 40
    if "смартфон" in text and "карты памяти" in path_lower:
        semantic_score -= 30
    if "смартфон" in text and "аксессуары" in path_lower:
        semantic_score -= 40
    if "антистресс" in text and "антистресс" in path_lower:
        semantic_score += 35
    if "антистресс" in text and path_lower.startswith("игрушки") and "антистресс" not in path_lower:
        semantic_score -= 10

    if lexical_score <= 0 and semantic_score <= 0:
        return 0

    score += semantic_score
    if has_female_marker and path_lower.startswith("мужчинам"):
        score -= 30
    if has_male_marker and path_lower.startswith("женщинам"):
        score -= 30
    if has_male_marker and path_lower.startswith("мужчинам"):
        score += 10
    if has_female_marker and path_lower.startswith("женщинам"):
        score += 10
    if has_kids_marker and path_lower.startswith("детям"):
        score += 12
    if has_kids_marker and (path_lower.startswith("женщинам") or path_lower.startswith("мужчинам")):
        score -= 20
    if not has_kids_marker and has_clothing_product and path_lower.startswith("детям"):
        score -= 20
    if has_clothing_product and has_female_marker and path_lower.startswith("женщинам"):
        score += 18
    if has_clothing_product and has_male_marker and path_lower.startswith("мужчинам"):
        score += 18
    if has_clothing_product and has_kids_marker and path_lower.startswith("детям"):
        score += 18
    if has_clothing_product and not (
        path_lower.startswith("женщинам")
        or path_lower.startswith("мужчинам")
        or path_lower.startswith("детям")
    ):
        score -= 20
    if has_clothing_product and path_lower.startswith("детям") and not any(
        marker in path_lower for marker in ("одеж", "пижам", "брюк", "шорт", "футбол", "куртк", "худи")
    ):
        score -= 20
    if any(marker in text for marker in ("сыворот", "гиалурон", "кожи", "лица")) and path_lower.startswith("красота"):
        score += 25
    if any(marker in text for marker in ("сыворот", "гиалурон", "кожи", "лица")) and path_lower.startswith("детям"):
        score -= 25
    if "маска" in text and "сна" in text and path_lower.startswith("аксессуары"):
        score += 25
    if "маска" in text and "сна" in text and path_lower.startswith("дом"):
        score -= 20
    if "игруш" in text and path_lower.startswith("игрушки"):
        score += 25
    if "игруш" in text and path_lower.startswith("детям"):
        score -= 10

    if item.get("is_leaf"):
        score += 1
    if score >= 2:
        score += max(0, _category_depth(path) - 1)
    return score


def detect_wb_category_path(
    product_description: str,
    wb_categories: dict[str, Any] | None = None,
) -> str | None:
    catalog = wb_categories if wb_categories is not None else load_wb_categories()
    categories = catalog.get("categories") if isinstance(catalog, dict) else None
    if not isinstance(categories, list):
        return None

    best_path: str | None = None
    best_score = 0
    for item in categories:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path") or "").strip()
        if not path:
            continue
        score = _catalog_category_score(item, product_description)
        if score > best_score or (
            score == best_score and best_path and _category_depth(path) > _category_depth(best_path)
        ):
            best_score = score
            best_path = path
    if best_score >= 4:
        return best_path
    return None


OZON_LIGHTING_PRODUCT_TOKENS = {"лампа", "лампы", "светильник", "ночник", "led"}
OZON_AUDIO_PRODUCT_TOKENS = {"наушники", "наушник", "гарнитура", "bluetooth", "колонка", "микрофон"}
OZON_BATH_MAT_PRODUCT_TOKENS = {"коврик", "коврики", "ванной", "ванная", "душ", "туалет"}
OZON_BACKPACK_PRODUCT_TOKENS = {"рюкзак", "рюкзаки", "ранец", "портфель"}
OZON_CLOTHING_PRODUCT_TOKENS = WB_CLOTHING_PRODUCT_TOKENS
OZON_SHOES_PRODUCT_TOKENS = WB_SHOES_PRODUCT_TOKENS


def _ozon_catalog_category_score(item: dict[str, Any], product_description: str) -> int:
    text = product_description.casefold()
    text_tokens = _tokens(product_description)
    path = str(item.get("path") or "")
    name = str(item.get("name") or "")
    path_lower = path.casefold()
    score = 0

    for token in _tokens(path):
        if _token_matches(token, text, text_tokens):
            score += 3
    for token in _tokens(name):
        if _token_matches(token, text, text_tokens):
            score += 4

    if bool(text_tokens & OZON_AUDIO_PRODUCT_TOKENS) and "наушники" in path_lower:
        score += 35
    if bool(text_tokens & OZON_AUDIO_PRODUCT_TOKENS) and "аудиотехника" in path_lower:
        score += 15
    if "смартфон" in text and "смартфоны" in path_lower:
        score += 40
    if "смартфон" in text and "аксессуары" in path_lower:
        score -= 25
    if bool(text_tokens & OZON_LIGHTING_PRODUCT_TOKENS) and any(marker in path_lower for marker in ("освещение", "светильник", "ламп")):
        score += 28
    if bool(text_tokens & OZON_BATH_MAT_PRODUCT_TOKENS) and any(marker in path_lower for marker in ("ванн", "коврик", "текстиль")):
        score += 30
    if bool(text_tokens & OZON_BACKPACK_PRODUCT_TOKENS) and any(marker in path_lower for marker in ("рюкзак", "сумк", "аксессуар")):
        score += 25
    if bool(text_tokens & OZON_CLOTHING_PRODUCT_TOKENS) and any(marker in path_lower for marker in ("одеж", "женщ", "мужч", "детск")):
        score += 18
    if bool(text_tokens & OZON_SHOES_PRODUCT_TOKENS) and "обув" in path_lower:
        score += 25
    if "корм" in text and any(marker in text for marker in ("кош", "собак", "питом")) and "животн" in path_lower:
        score += 30
    if any(marker in text for marker in ("витамин", "бад", "капсул", "омега")) and any(marker in path_lower for marker in ("аптека", "витамин", "бад")):
        score += 28
    if "книга" in text and "книг" in path_lower:
        score += 25

    if item.get("is_leaf"):
        score += 2
    if score >= 2:
        score += max(0, _category_depth(path) - 1)
    return score


def detect_ozon_category_path(
    product_description: str,
    ozon_categories: dict[str, Any] | None = None,
) -> str | None:
    catalog = ozon_categories if ozon_categories is not None else load_ozon_categories()
    categories = catalog.get("categories") if isinstance(catalog, dict) else None
    if not isinstance(categories, list):
        return None

    best_path: str | None = None
    best_score = 0
    for item in categories:
        if not isinstance(item, dict):
            continue
        path = str(item.get("path") or "").strip()
        if not path:
            continue
        score = _ozon_catalog_category_score(item, product_description)
        if score > best_score or (
            score == best_score and best_path and _category_depth(path) > _category_depth(best_path)
        ):
            best_score = score
            best_path = path
    if best_score >= 4:
        return best_path
    return None


OZON_PARENT_ALIASES = {
    "Товары для животных": ("Товары для животных", "Зоотовары"),
    "Канцелярские товары": ("Канцелярские товары", "Канцелярия"),
    "Продукты питания": ("Продукты питания", "Продукты"),
    "Спорт и отдых": ("Спорт и отдых", "Спорт"),
    "Строительство и ремонт": ("Строительство и ремонт", "Для ремонта"),
    "Игры и консоли": ("Игры и консоли", "Все для игр"),
}


def _ozon_catalog_profile_candidates(category_path: str) -> list[str]:
    parts = [part.strip() for part in category_path.split(" / ") if part.strip()]
    candidates: list[str] = []
    for size in range(len(parts), 0, -1):
        candidates.append(" / ".join(parts[:size]))
    if parts:
        for alias in OZON_PARENT_ALIASES.get(parts[0], ()):
            if alias not in candidates:
                candidates.append(alias)
    return candidates


def _profile_from_ozon_catalog_path(
    profiles: dict[str, dict[str, Any]],
    category_path: str,
) -> dict[str, Any] | None:
    profiles_by_casefold = {category.casefold(): profile for category, profile in profiles.items()}
    for candidate in _ozon_catalog_profile_candidates(category_path):
        profile = profiles.get(candidate) or profiles_by_casefold.get(candidate.casefold())
        if profile:
            profile_copy = dict(profile)
            if candidate.casefold() != category_path.casefold():
                profile_copy["source_profile_category"] = profile_copy.get("category") or candidate
                profile_copy["category"] = category_path
                profile_copy["parent_category"] = category_path.split(" / ", 1)[0].strip()
            return profile_copy

    top = category_path.split(" / ", 1)[0].strip()
    if top:
        top_lower = top.casefold()
        descendants = [
            profile
            for category, profile in profiles.items()
            if category.casefold() == top_lower or category.casefold().startswith(f"{top_lower} / ")
        ]
        if descendants:
            profile_copy = dict(sorted(descendants, key=_profile_depth)[0])
            profile_copy["source_profile_category"] = profile_copy.get("category") or top
            profile_copy["category"] = category_path
            profile_copy["parent_category"] = top
            return profile_copy
    return None


def _score_ozon_profile(profile: dict[str, Any], product_description: str) -> int:
    text = product_description.casefold()
    text_tokens = _tokens(product_description)
    score = 0
    category = str(profile.get("category") or "")
    parent = str(profile.get("parent_category") or "")
    for part in (category, parent):
        for token in part.replace("/", " ").split():
            if _token_matches(token, text, text_tokens):
                score += 3
    for keyword in profile.get("match_keywords") or []:
        if _token_matches(str(keyword), text, text_tokens):
            score += 3
    for keyword in profile.get("top_title_words") or []:
        if _token_matches(str(keyword), text, text_tokens):
            score += 1

    category_lower = category.casefold()
    if bool(text_tokens & OZON_AUDIO_PRODUCT_TOKENS) and "наушники" in category_lower:
        score += 14
    if bool(text_tokens & OZON_BATH_MAT_PRODUCT_TOKENS) and any(marker in category_lower for marker in ("ванн", "коврик")):
        score += 14
    if bool(text_tokens & OZON_LIGHTING_PRODUCT_TOKENS) and any(marker in category_lower for marker in ("освещение", "ламп", "светильник")):
        score += 12
    if bool(text_tokens & OZON_BACKPACK_PRODUCT_TOKENS) and any(marker in category_lower for marker in ("рюкзак", "сумк", "аксессуар")):
        score += 10

    if score >= 2:
        score += max(0, _profile_depth(profile) - 1)
    return score


def detect_ozon_category_profile(
    profiles: dict[str, dict[str, Any]],
    product_description: str,
    ozon_categories: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    catalog_path = detect_ozon_category_path(product_description, ozon_categories)
    if catalog_path:
        profile = _profile_from_ozon_catalog_path(profiles, catalog_path)
        if profile:
            profile["detected_category_path"] = catalog_path
            return profile

    best_profile: dict[str, Any] | None = None
    best_score = 0
    for profile in profiles.values():
        score = _score_ozon_profile(profile, product_description)
        if score > best_score or (score == best_score and best_profile and _profile_depth(profile) > _profile_depth(best_profile)):
            best_score = score
            best_profile = profile
    if best_profile and best_score >= 3:
        return dict(best_profile)
    return None


def _catalog_profile_candidates(category_path: str) -> list[str]:
    parts = [part.strip() for part in category_path.split(" / ") if part.strip()]
    candidates: list[str] = []
    for size in range(len(parts), 0, -1):
        candidate = " / ".join(parts[:size])
        candidates.append(candidate)

    if parts:
        parent = parts[0]
        path_lower = category_path.casefold()
        insert_at = len(candidates) - 1 if candidates and candidates[-1] == parent else len(candidates)
        if parent in {"Женщинам", "Мужчинам"} and not any(marker in path_lower for marker in ("белье", "купаль")):
            candidates.insert(insert_at, f"{parent} / Одежда")
            insert_at += 1
        if parent == "Детям" and any(
            marker in path_lower
            for marker in ("одеж", "брюк", "шорт", "футбол", "костюм", "пижам", "куртк", "худи")
        ):
            candidates.insert(insert_at, "Детям / Одежда")
            insert_at += 1
        for alias in WB_PARENT_ALIASES.get(parent, ()):
            if alias not in candidates:
                candidates.append(alias)
    return candidates


def _synthetic_profile(category: str) -> dict[str, Any] | None:
    profile = WB_SYNTHETIC_FALLBACK_PROFILES.get(category)
    return dict(profile) if profile else None


def _fallback_profile_for_top_category(category_path: str) -> dict[str, Any] | None:
    top = category_path.split(" / ", 1)[0].strip()
    if not top:
        return None
    if top in WB_SYNTHETIC_FALLBACK_PROFILES:
        return _synthetic_profile(top)
    for category, aliases in WB_PARENT_ALIASES.items():
        if top in aliases:
            return _synthetic_profile(category)
    return None


def _context_allows_profile_field(field: str, product_description: str, profile: dict[str, Any]) -> bool:
    field_lower = field.casefold()
    context = f"{product_description} {profile.get('category') or ''}".casefold()
    if any(marker in field_lower for marker in WB_PROFILE_FIELD_DROP_MARKERS):
        return False
    for field_markers, context_markers in WB_CONTEXT_PROFILE_FIELD_RULES:
        if any(marker in field_lower for marker in field_markers):
            return any(marker in context for marker in context_markers)
    return True


def _sanitize_wb_profile_for_product(
    profile: dict[str, Any],
    product_description: str,
) -> dict[str, Any]:
    result = dict(profile)
    for key in (
        "prompt_characteristics",
        "required_generation_characteristics",
        "recommended_generation_characteristics",
    ):
        value = result.get(key)
        if not isinstance(value, list):
            continue
        result[key] = [
            str(field).strip()
            for field in value
            if str(field).strip() and _context_allows_profile_field(str(field), product_description, result)
        ]
    return result


def _direct_wb_profile_override(
    profiles: dict[str, dict[str, Any]],
    product_description: str,
) -> dict[str, Any] | None:
    text = product_description.casefold()
    text_tokens = _tokens(product_description)
    if bool(text_tokens & WB_PET_PRODUCT_TOKENS):
        return _synthetic_profile("Товары для животных")
    if "коврик" in text and any(marker in text for marker in ("йог", "фитнес", "трениров")):
        return _synthetic_profile("Спорт")
    if bool(text_tokens & WB_LIGHTING_PRODUCT_TOKENS) and any(
        marker in text for marker in ("led", "usb", "мощност", "яркост", "режим", "свет")
    ):
        profile = profiles.get("Электроника")
        if profile:
            return dict(profile)
    return None


def _profile_from_catalog_path(
    profiles: dict[str, dict[str, Any]],
    category_path: str,
) -> dict[str, Any] | None:
    for candidate in _catalog_profile_candidates(category_path):
        profile = profiles.get(candidate)
        if profile:
            return dict(profile)
    top = category_path.split(" / ", 1)[0].strip()
    if top:
        descendants = [
            profile
            for category, profile in profiles.items()
            if category == top or category.startswith(f"{top} / ")
        ]
        if descendants:
            return dict(sorted(descendants, key=_profile_depth)[0])
    return _fallback_profile_for_top_category(category_path)


def _best_scored_wb_profile(
    profiles: dict[str, dict[str, Any]],
    product_description: str,
) -> dict[str, Any] | None:
    best_profile: dict[str, Any] | None = None
    best_score = 0
    for profile in profiles.values():
        score = _score_profile(profile, product_description)
        if score > best_score or (score == best_score and best_profile and _profile_depth(profile) > _profile_depth(best_profile)):
            best_score = score
            best_profile = profile
    if best_profile and best_score >= 2:
        return dict(best_profile)
    return None


def _score_profile(profile: dict[str, Any], product_description: str) -> int:
    text = product_description.casefold()
    text_tokens = _tokens(product_description)
    score = 0
    category = str(profile.get("category") or "")
    parent = str(profile.get("parent_category") or "")
    for part in (category, parent):
        for token in part.replace("/", " ").split():
            if _token_matches(token, text, text_tokens):
                score += 3
    for keyword in profile.get("match_keywords") or []:
        if _token_matches(str(keyword), text, text_tokens):
            score += 2
    for keyword in profile.get("top_title_words") or []:
        if _token_matches(str(keyword), text, text_tokens):
            score += 1

    category_lower = category.casefold()
    has_clothing_product = bool(text_tokens & WB_CLOTHING_PRODUCT_TOKENS)
    has_shoes_product = bool(text_tokens & WB_SHOES_PRODUCT_TOKENS)
    has_backpack_product = bool(text_tokens & WB_BACKPACK_PRODUCT_TOKENS)
    has_lighting_product = bool(text_tokens & WB_LIGHTING_PRODUCT_TOKENS)
    has_pet_product = bool(text_tokens & WB_PET_PRODUCT_TOKENS)
    has_female_marker = bool(text_tokens & {"женская", "женские", "женский", "женское"})
    has_male_marker = bool(text_tokens & {"мужская", "мужские", "мужской", "мужское"})

    if has_female_marker and category_lower.startswith("мужчинам"):
        score -= 20
    if has_male_marker and category_lower.startswith("женщинам"):
        score -= 20

    if has_shoes_product and category_lower.startswith("обувь"):
        score += 8
    if has_shoes_product and (
        category_lower.startswith("женщинам") or category_lower.startswith("мужчинам")
    ):
        score -= 4
    if has_backpack_product and category_lower == "аксессуары":
        score += 10
    if has_backpack_product and "маски для сна" in category_lower:
        score -= 12
    if has_lighting_product and category_lower.startswith("электроника"):
        score += 10
    if has_lighting_product and category_lower.startswith("бытовая техника"):
        score += 4
    if has_lighting_product and category_lower.startswith("красота"):
        score -= 10
    if has_pet_product and not (
        category_lower.startswith("зоотовары")
        or category_lower.startswith("товары для животных")
    ):
        score -= 10

    if has_clothing_product and category_lower.startswith("женщинам") and has_female_marker:
        score += 5
    if has_clothing_product and category_lower.startswith("мужчинам") and has_male_marker:
        score += 5
    if has_clothing_product and "одежда" in category_lower:
        score += 4

    if score >= 2:
        score += max(0, _profile_depth(profile) - 1)
    return score


def detect_wb_category_profile(
    profiles: dict[str, dict[str, Any]],
    product_description: str,
    wb_categories: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    direct_profile = _direct_wb_profile_override(profiles, product_description)
    if direct_profile:
        return _sanitize_wb_profile_for_product(direct_profile, product_description)

    catalog_path = detect_wb_category_path(product_description, wb_categories)
    if catalog_path:
        profile = _profile_from_catalog_path(profiles, catalog_path)
        if profile:
            profile["detected_category_path"] = catalog_path
            return _sanitize_wb_profile_for_product(profile, product_description)

    best_profile = _best_scored_wb_profile(profiles, product_description)
    if best_profile:
        return _sanitize_wb_profile_for_product(best_profile, product_description)
    return None
