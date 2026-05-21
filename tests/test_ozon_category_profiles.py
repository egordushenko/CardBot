from tools.build_category_profiles import build_category_profiles


def test_build_ozon_category_profiles_excludes_service_fields_from_prompt_profile():
    cards = [
        {
            "collection_target_category": "Одежда",
            "title": "Футболка женская черная",
            "description": "Футболка для повседневной носки.",
            "characteristics": {
                "Артикул": "123",
                "Добавить к сравнению": "Да",
                "Китай": "Китай",
                "20": "20",
                "Упаковка": "Пакет",
                "Цвет": "Черный",
                "Тип": "Футболка",
                "Материал": "Хлопок",
            },
            "hashtags": ["#футболка"],
        },
        {
            "collection_target_category": "Одежда",
            "title": "Футболка женская белая",
            "description": "Базовая футболка.",
            "characteristics": {
                "Артикул": "456",
                "Добавить к сравнению": "Да",
                "Китай": "Китай",
                "20": "20",
                "Упаковка": "Пакет",
                "Цвет": "Белый",
                "Тип": "Футболка",
                "Материал": "Хлопок",
            },
            "hashtags": ["#футболка"],
        },
    ]

    profile = build_category_profiles(cards)["Одежда"]

    assert "Артикул" in profile["top_characteristics"]
    assert "Артикул" not in profile["prompt_characteristics"]
    assert "Добавить к сравнению" not in profile["prompt_characteristics"]
    assert "Китай" not in profile["prompt_characteristics"]
    assert "20" not in profile["prompt_characteristics"]
    assert "Упаковка" not in profile["prompt_characteristics"]
    assert profile["prompt_characteristics"] == ["Цвет", "Тип", "Материал"]
