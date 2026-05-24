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
    assert profile["prompt_characteristics"][:3] == ["Цвет", "Пол", "Сезон"]
    assert profile["characteristics_target_min"] >= 5
    assert profile["hashtags_target"] == 0


def test_build_wb_category_profiles_excludes_logistics_fields_from_prompt_profile():
    cards = [
        {
            "category": "Дом",
            "source_category": "Дом / Ванная / Коврики",
            "title": "Коврик для ванной серый",
            "description": "Мягкий коврик для ванной комнаты.",
            "characteristics": {
                "Ширина упаковки": "10 см",
                "Высота упаковки": "10 см",
                "Длина упаковки": "50 см",
                "Вес с упаковкой (кг)": "0.4 кг",
                "Цвет": "серый",
                "Материал изделия": "микрофибра",
                "Форма коврика": "прямоугольный",
            },
        },
        {
            "category": "Дом",
            "source_category": "Дом / Ванная / Коврики",
            "title": "Коврик для ванной противоскользящий",
            "description": "Коврик для ванной и туалета.",
            "characteristics": {
                "Ширина упаковки": "12 см",
                "Высота упаковки": "12 см",
                "Длина упаковки": "52 см",
                "Вес с упаковкой (кг)": "0.5 кг",
                "Цвет": "белый",
                "Материал изделия": "полиэстер",
                "Форма коврика": "прямоугольный",
            },
        },
    ]

    profiles = build_wb_category_profiles(cards)
    profile = profiles["Дом / Ванная / Коврики"]

    assert "Ширина упаковки" in profile["required_characteristics"]
    assert "Ширина упаковки" not in profile["prompt_characteristics"]
    assert "Высота упаковки" not in profile["prompt_characteristics"]
    assert "Длина упаковки" not in profile["prompt_characteristics"]
    assert "Вес с упаковкой (кг)" not in profile["prompt_characteristics"]
    assert "Форма коврика" in profile["prompt_characteristics"]


def test_build_wb_category_profiles_excludes_item_dimensions_from_prompt_profile():
    cards = [
        {
            "category": "Дом",
            "source_category": "Дом / Ванная / Коврики",
            "title": "Коврик для ванной 50x80",
            "description": "Коврик для ванной комнаты.",
            "characteristics": {
                "Длина предмета": "80 см",
                "Ширина предмета": "50 см",
                "Высота предмета": "1 см",
                "Цвет": "серый",
                "Материал изделия": "микрофибра",
            },
        },
        {
            "category": "Дом",
            "source_category": "Дом / Ванная / Коврики",
            "title": "Коврик для ванной 60x90",
            "description": "Коврик для душевой зоны.",
            "characteristics": {
                "Длина предмета": "90 см",
                "Ширина предмета": "60 см",
                "Высота предмета": "1 см",
                "Цвет": "белый",
                "Материал изделия": "полиэстер",
            },
        },
    ]

    profile = build_wb_category_profiles(cards)["Дом / Ванная / Коврики"]

    assert "Длина предмета" in profile["required_characteristics"]
    assert "Длина предмета" not in profile["prompt_characteristics"]
    assert "Ширина предмета" not in profile["prompt_characteristics"]
    assert "Высота предмета" not in profile["prompt_characteristics"]
    assert profile["prompt_characteristics"] == ["Цвет", "Материал изделия"]


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


def test_detect_wb_category_profile_prefers_shoes_over_womens_clothes_for_sneakers():
    profile = detect_wb_category_profile(
        load_wb_category_profiles(),
        "Кроссовки женские белые, размер 38, сезон лето. Материал стельки текстиль.",
    )

    assert profile is not None
    assert profile["category"] == "Обувь"


def test_detect_wb_category_profile_uses_gender_and_product_guards():
    profiles = load_wb_category_profiles()

    hoodie = detect_wb_category_profile(
        profiles,
        "Худи мужское на молнии черное, хлопок, свободный крой",
    )
    backpack = detect_wb_category_profile(
        profiles,
        "Рюкзак городской мужской черный, объем 22 литра, отделение для ноутбука",
    )
    lamp = detect_wb_category_profile(
        profiles,
        "Настольная лампа LED спиральная белая USB 5W, высота 35 см",
    )
    pet_food = detect_wb_category_profile(
        profiles,
        "Сухой корм для кошек с курицей 1 кг, для взрослых кошек",
    )

    assert hoodie is not None
    assert hoodie["category"].startswith("Мужчинам")
    assert backpack is not None
    assert backpack["category"] == "Аксессуары"
    assert lamp is not None
    assert lamp["category"] == "Электроника"
    assert pet_food is not None
    assert pet_food["category"] == "Товары для животных"


def test_detect_wb_category_profile_routes_rashguard_to_clothing():
    profile = detect_wb_category_profile(
        load_wb_category_profiles(),
        "Рашгард therapy черный размер M, 100% хлопок, тянущийся облегающий с горловиной качественная печать текста на спине (Therapy)",
    )

    assert profile is not None
    assert "Одежда" in profile["category"]
    assert "Состав" in profile["prompt_characteristics"]


def test_detect_wb_category_profile_falls_back_to_safe_synthetic_profiles():
    profiles = load_wb_category_profiles()

    sport_mat = detect_wb_category_profile(
        profiles,
        "Коврик для йоги фиолетовый 183x61 см 6 мм нескользящий с ремнем",
    )
    pet_food = detect_wb_category_profile(
        profiles,
        "Сухой корм для кошек с курицей. Для взрослых кошек, упаковка 1 кг.",
    )

    assert sport_mat is not None
    assert sport_mat["category"] == "Спорт"
    assert "Размер" in sport_mat["prompt_characteristics"]
    assert pet_food is not None
    assert pet_food["category"] == "Товары для животных"
    assert "Вес" in pet_food["prompt_characteristics"]


def test_detect_wb_category_profile_prefers_specific_profile_and_has_no_unsafe_fallback(tmp_path: Path):
    path = tmp_path / "wb_category_profiles.json"
    path.write_text(
        json.dumps(
            {
                "Дом": {
                    "marketplace": "wb",
                    "category": "Дом",
                    "parent_category": "Дом",
                    "match_keywords": ["дом", "ванная"],
                },
                "Дом / Ванная / Коврики": {
                    "marketplace": "wb",
                    "category": "Дом / Ванная / Коврики",
                    "parent_category": "Дом",
                    "match_keywords": ["коврик", "ванной", "туалета"],
                },
                "Женщинам / Одежда": {
                    "marketplace": "wb",
                    "category": "Женщинам / Одежда",
                    "parent_category": "Женщинам",
                    "match_keywords": ["футболка", "оверсайз"],
                },
                "Продукты питания / Чай, кофе / Чай": {
                    "marketplace": "wb",
                    "category": "Продукты питания / Чай, кофе / Чай",
                    "parent_category": "Продукты питания",
                    "match_keywords": ["чай", "кофе"],
                    "top_title_words": ["черный"],
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    profiles = load_wb_category_profiles(path)

    mat_profile = detect_wb_category_profile(profiles, "Коврик для ванной серый 50 на 80 см")
    shirt_profile = detect_wb_category_profile(profiles, "Женская футболка оверсайз черная")
    unknown_profile = detect_wb_category_profile(profiles, "Рюкзак городской мужской черный")

    assert mat_profile is not None
    assert mat_profile["category"] == "Дом / Ванная / Коврики"
    assert shirt_profile is not None
    assert shirt_profile["category"] == "Женщинам / Одежда"
    assert unknown_profile is None


def test_load_category_profiles_still_loads_ozon_by_default(tmp_path: Path):
    path = tmp_path / "category_profiles.json"
    path.write_text(
        json.dumps({"Одежда": {"top_characteristics": ["Цвет"]}}, ensure_ascii=False),
        encoding="utf-8",
    )

    assert load_category_profiles(path)["Одежда"]["category"] == "Одежда"
