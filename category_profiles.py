from __future__ import annotations

import json
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


def _score_profile(profile: dict[str, Any], product_description: str) -> int:
    text = product_description.casefold()
    score = 0
    category = str(profile.get("category") or "")
    parent = str(profile.get("parent_category") or "")
    for part in (category, parent):
        for token in part.replace("/", " ").split():
            token = token.strip().casefold()
            if len(token) >= 3 and token in text:
                score += 3
    for keyword in profile.get("match_keywords") or []:
        token = str(keyword).strip().casefold()
        if len(token) >= 3 and token in text:
            score += 2
    for keyword in profile.get("top_title_words") or []:
        token = str(keyword).strip().casefold()
        if len(token) >= 3 and token in text:
            score += 1
    return score


def detect_wb_category_profile(
    profiles: dict[str, dict[str, Any]],
    product_description: str,
) -> dict[str, Any] | None:
    best_profile: dict[str, Any] | None = None
    best_score = 0
    for profile in profiles.values():
        score = _score_profile(profile, product_description)
        if score > best_score:
            best_score = score
            best_profile = profile
    if best_profile:
        return dict(best_profile)

    fallback = profiles.get("Дом") or profiles.get("Женщинам")
    return dict(fallback) if fallback else None
