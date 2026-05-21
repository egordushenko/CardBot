from __future__ import annotations

import json
from pathlib import Path

from category_profiles import (
    detect_ozon_category_profile,
    get_category_profile,
    load_category_profiles,
)
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


def test_build_category_profiles_adds_ozon_v2_signals_and_excludes_garbage_fields():
    cards = [
        {
            "category": "Дом и сад / Ванная / Коврики",
            "title": "Коврик для ванной серый 50x80 см",
            "description": "Мягкий коврик для ванной комнаты с противоскользящим основанием.",
            "hashtags": ["#коврик_для_ванной", "#ванная"],
            "characteristics": {
                "Цвет": "серый",
                "Материал изделия": "микрофибра",
                "Размер коврика": "50x80 см",
                "Длина упаковки": "50 см",
                "Ширина упаковки": "10 см",
                "Вес с упаковкой (кг)": "0.4",
                "Длина предмета": "80 см",
                "Артикул": "123",
            },
        },
        {
            "category": "Дом и сад / Ванная / Коврики",
            "title": "Коврик для ванной противоскользящий бежевый",
            "description": "Коврик для душевой зоны и туалета, приятный на ощупь.",
            "hashtags": "#коврик_для_ванной #душевая",
            "characteristics": {
                "Цвет": "бежевый",
                "Материал изделия": "полиэстер",
                "Размер коврика": "60x90 см",
                "Высота упаковки": "12 см",
                "Вес товара, г": "500",
                "Ширина предмета": "60 см",
                "Бренд": "No name",
            },
        },
    ]

    profiles = build_category_profiles(cards)
    detailed = profiles["Дом и сад / Ванная / Коврики"]
    top = profiles["Дом и сад"]

    assert detailed["marketplace"] == "ozon"
    assert detailed["parent_category"] == "Дом и сад"
    assert detailed["cards_count"] == 2
    assert detailed["required_characteristics"][:2] == ["Цвет", "Материал изделия"]
    assert "Размер коврика" in detailed["required_characteristics"] + detailed["recommended_characteristics"]
    assert detailed["characteristics_target_min"] >= 3
    assert detailed["title_target_min"] <= detailed["title_target_max"]
    assert detailed["description_target_min"] <= detailed["description_target_max"]
    assert "Цвет" in detailed["prompt_characteristics"]
    assert "Материал изделия" in detailed["prompt_characteristics"]
    assert "Длина упаковки" not in detailed["prompt_characteristics"]
    assert "Ширина упаковки" not in detailed["prompt_characteristics"]
    assert "Высота упаковки" not in detailed["prompt_characteristics"]
    assert "Вес с упаковкой (кг)" not in detailed["prompt_characteristics"]
    assert "Вес товара, г" not in detailed["prompt_characteristics"]
    assert "Длина предмета" not in detailed["prompt_characteristics"]
    assert "Ширина предмета" not in detailed["prompt_characteristics"]
    assert "Артикул" not in detailed["prompt_characteristics"]
    assert top["category"] == "Дом и сад"


def test_detect_ozon_category_profile_prefers_catalog_leaf_profile():
    profiles = {
        "Дом и сад": {
            "category": "Дом и сад",
            "parent_category": "Дом и сад",
            "match_keywords": ["дом", "сад"],
        },
        "Дом и сад / Ванная / Коврики": {
            "category": "Дом и сад / Ванная / Коврики",
            "parent_category": "Дом и сад",
            "match_keywords": ["коврик", "ванной", "душевой"],
        },
        "Электроника / Наушники и аудиотехника / Наушники": {
            "category": "Электроника / Наушники и аудиотехника / Наушники",
            "parent_category": "Электроника",
            "match_keywords": ["наушники", "bluetooth"],
        },
    }
    ozon_categories = {
        "categories": [
            {"path": "Дом и сад", "name": "Дом и сад", "is_leaf": False},
            {"path": "Дом и сад / Ванная / Коврики", "name": "Коврики", "is_leaf": True},
            {
                "path": "Электроника / Наушники и аудиотехника / Наушники",
                "name": "Наушники",
                "is_leaf": True,
            },
        ]
    }

    mat = detect_ozon_category_profile(profiles, "Коврик для ванной серый 50 на 80 см", ozon_categories)
    headphones = detect_ozon_category_profile(profiles, "Беспроводные наушники Bluetooth с микрофоном", ozon_categories)

    assert mat is not None
    assert mat["category"] == "Дом и сад / Ванная / Коврики"
    assert mat["detected_category_path"] == "Дом и сад / Ванная / Коврики"
    assert headphones is not None
    assert headphones["category"] == "Электроника / Наушники и аудиотехника / Наушники"


def test_detect_ozon_category_profile_uses_detected_path_with_parent_profile_fallback():
    profiles = {
        "Дом и сад": {
            "category": "Дом и сад",
            "parent_category": "Дом и сад",
            "match_keywords": ["дом", "ванной"],
            "prompt_characteristics": ["Цвет", "Материал"],
        }
    }
    ozon_categories = {
        "categories": [
            {"path": "Дом и сад", "name": "Дом и сад", "is_leaf": False},
            {"path": "Дом и сад / Аксессуары для ванной", "name": "Аксессуары для ванной", "is_leaf": True},
        ]
    }

    profile = detect_ozon_category_profile(profiles, "Коврик для ванной серый", ozon_categories)

    assert profile is not None
    assert profile["category"] == "Дом и сад / Аксессуары для ванной"
    assert profile["source_profile_category"] == "Дом и сад"
    assert profile["prompt_characteristics"] == ["Цвет", "Материал"]


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
