from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CATEGORY_PROFILES_PATH = BASE_DIR / "data" / "category_profiles.json"
DEFAULT_WB_CATEGORY_PROFILES_PATH = BASE_DIR / "data" / "wb_category_profiles.json"


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
