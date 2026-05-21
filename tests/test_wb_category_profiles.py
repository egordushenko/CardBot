from __future__ import annotations

import json
from pathlib import Path

from category_profiles import (
    detect_wb_category_profile,
    get_category_profile,
    load_category_profiles,
    load_wb_category_profiles,
)
from tools.build_wb_category_profiles import build_wb_category_profiles


def test_build_wb_category_profiles_extracts_required_and_recommended_fields():
    cards = [
        {
            "category": "Обувь",
            "source_category": "Обувь",
            "title": "Кроссовки женские летние",
            "description": "Легкие кроссовки для прогулок.",
            "characteristics": {
                "Цвет": "белый",
                "Пол": "Женский",
                "Сезон": "Лето",
                "Материал стельки": "текстиль",
                "Материал подошвы обуви": "ПВХ",
            },
        },
        {
            "category": "Обувь",
            "source_category": "Обувь",
            "title": "Кеды женские",
            "description": "Кеды на каждый день.",
            "characteristics": {
                "Цвет": "черный",
                "Пол": "Женский",
                "Сезон": "Демисезон",
                "Материал стельки": "кожа",
                "Вид застежки": "шнуровка",
            },
        },
    ]

    profiles = build_wb_category_profiles(cards)
    profile = profiles["Обувь"]

    assert profile["marketplace"] == "wb"
    assert profile["required_characteristics"][:3] == ["Цвет", "Пол", "Сезон"]
    assert "Материал стельки" in profile["recommended_characteristics"]
    assert profile["characteristics_target_min"] >= 8
    assert profile["hashtags_target"] == 0


def test_load_wb_category_profiles_and_detect_profile(tmp_path: Path):
    path = tmp_path / "wb_category_profiles.json"
    path.write_text(
        json.dumps(
            {
                "Обувь": {
                    "marketplace": "wb",
                    "category": "Обувь",
                    "parent_category": "Обувь",
                    "match_keywords": ["кроссовки", "кеды"],
                    "required_characteristics": ["Цвет"],
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    profiles = load_wb_category_profiles(path)
    profile = detect_wb_category_profile(profiles, "женские кроссовки белые")

    assert get_category_profile(profiles, "Обувь")["category"] == "Обувь"
    assert profile is not None
    assert profile["category"] == "Обувь"


def test_load_category_profiles_still_loads_ozon_by_default(tmp_path: Path):
    path = tmp_path / "category_profiles.json"
    path.write_text(
        json.dumps({"Одежда": {"top_characteristics": ["Цвет"]}}, ensure_ascii=False),
        encoding="utf-8",
    )

    assert load_category_profiles(path)["Одежда"]["category"] == "Одежда"
