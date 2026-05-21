from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CATEGORY_PROFILES_PATH = BASE_DIR / "data" / "category_profiles.json"


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
