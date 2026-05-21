from __future__ import annotations

import json
from pathlib import Path

from category_profiles import get_category_profile, load_category_profiles
from tools.build_category_profiles import build_category_profiles


def test_build_category_profiles_extracts_category_signals(tmp_path: Path):
    dataset = [
        {
            "collection_target_category": "Красота и здоровье",
            "title": "Крем для лица увлажняющий дневной",
            "description": "Увлажняющий крем для сухой кожи.",
            "hashtags": ["#крем", "#уход_за_кожей", "#крем"],
            "characteristics": {
                "Тип": "Крем",
                "Тип кожи": "Сухая",
                "Объем, мл": "50",
            },
        },
        {
            "collection_target_category": "Красота и здоровье",
            "title": "Крем ночной питание кожи",
            "description": "Ночной крем для ухода за кожей лица.",
            "hashtags": "#крем #ночной",
            "characteristics": {
                "Тип": "Крем",
                "Тип кожи": "Нормальная",
                "Страна-изготовитель": "Россия",
            },
        },
        {
            "collection_target_category": "Одежда",
            "title": "Футболка хлопковая базовая",
            "description": "Футболка из хлопка.",
            "hashtags": ["#футболка"],
            "characteristics": {"Цвет": "Белый", "Размер": "M"},
        },
    ]

    profiles = build_category_profiles(dataset)

    beauty = profiles["Красота и здоровье"]
    assert beauty["top_characteristics"][:2] == ["Тип", "Тип кожи"]
    assert beauty["top_hashtags"][:2] == ["#крем", "#уход_за_кожей"]
    assert "крем" in beauty["top_title_words"]
    assert beauty["desc_target_chars"] == 1400
    assert beauty["hashtags_target"] == 8


def test_load_category_profiles_adds_category_name(tmp_path: Path):
    path = tmp_path / "category_profiles.json"
    path.write_text(
        json.dumps({"Одежда": {"top_characteristics": ["Цвет"]}}, ensure_ascii=False),
        encoding="utf-8",
    )

    profiles = load_category_profiles(path)
    profile = get_category_profile(profiles, "Одежда")

    assert profile is not None
    assert profile["category"] == "Одежда"
    assert profile["top_characteristics"] == ["Цвет"]
