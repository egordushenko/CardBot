from __future__ import annotations

from category_profiles import detect_wb_category_profile
from tools.build_wb_categories import build_wb_categories_payload, flatten_wb_menu


def test_flatten_wb_menu_preserves_nested_paths_and_leaf_flags():
    menu = [
        {
            "id": 1,
            "name": "Дом",
            "url": "/catalog/dom",
            "childs": [
                {
                    "id": 2,
                    "name": "Освещение",
                    "url": "/catalog/dom/osveshchenie",
                    "childs": [
                        {
                            "id": 3,
                            "name": "Настольные лампы",
                            "url": "/catalog/dom/osveshchenie/nastolnye-lampy",
                            "query": "subject=9215",
                        }
                    ],
                }
            ],
        }
    ]

    rows = flatten_wb_menu(menu)

    assert rows[-1] == {
        "id": 3,
        "name": "Настольные лампы",
        "path": "Дом / Освещение / Настольные лампы",
        "level": 3,
        "url": "https://www.wildberries.ru/catalog/dom/osveshchenie/nastolnye-lampy",
        "query": "subject=9215",
        "parent_path": "Дом / Освещение",
        "children_count": 0,
        "is_leaf": True,
    }


def test_build_wb_categories_payload_contains_summary():
    payload = build_wb_categories_payload(
        [{"id": 1, "name": "Дом", "url": "/catalog/dom"}],
        source_url="https://example.test/menu.json",
    )

    assert payload["source_url"] == "https://example.test/menu.json"
    assert payload["total"] == 1
    assert payload["leaf_total"] == 1
    assert payload["max_level"] == 1
    assert payload["categories"][0]["path"] == "Дом"


def test_detect_wb_category_profile_uses_catalog_tree_before_profile_scoring():
    profiles = {
        "Дом": {
            "marketplace": "wb",
            "category": "Дом",
            "parent_category": "Дом",
            "match_keywords": ["дом"],
        },
        "Электроника / Комплектующие для ПК / Видеокарты": {
            "marketplace": "wb",
            "category": "Электроника / Комплектующие для ПК / Видеокарты",
            "parent_category": "Электроника",
            "match_keywords": ["led", "мощность"],
        },
        "Бытовая техника": {
            "marketplace": "wb",
            "category": "Бытовая техника",
            "parent_category": "Бытовая техника",
            "match_keywords": ["блендер"],
        },
    }
    catalog = {
        "categories": [
            {"path": "Дом / Освещение / Настольные лампы", "name": "Настольные лампы", "is_leaf": True},
            {"path": "Бытовая техника / Техника для кухни / Блендеры", "name": "Блендеры", "is_leaf": True},
            {"path": "Дом / Хранение вещей / Органайзеры", "name": "Органайзеры", "is_leaf": True},
        ]
    }

    lamp = detect_wb_category_profile(
        profiles,
        "Настольная лампа LED спиральная белая USB 5W",
        wb_categories=catalog,
    )
    blender = detect_wb_category_profile(
        profiles,
        "Блендер погружной белый 600 Вт две скорости",
        wb_categories=catalog,
    )
    organizer = detect_wb_category_profile(
        profiles,
        "Органайзер для хранения вещей складной бежевый",
        wb_categories=catalog,
    )

    assert lamp is not None
    assert lamp["category"] == "Дом"
    assert blender is not None
    assert blender["category"] == "Бытовая техника"
    assert organizer is not None
    assert organizer["category"] == "Дом"


def test_detect_wb_category_profile_uses_safe_sport_fallback_when_catalog_has_no_profile():
    profiles = {
        "Дом / Ванная / Коврики": {
            "marketplace": "wb",
            "category": "Дом / Ванная / Коврики",
            "parent_category": "Дом",
            "match_keywords": ["коврик", "нескользящий"],
        }
    }
    catalog = {
        "categories": [
            {
                "path": "Спорт / Йога/Пилатес / Коврики и маты",
                "name": "Коврики и маты",
                "is_leaf": True,
            }
        ]
    }

    profile = detect_wb_category_profile(
        profiles,
        "Коврик для йоги фиолетовый нескользящий 183x61 см",
        wb_categories=catalog,
    )

    assert profile is not None
    assert profile["category"] == "Спорт"
    assert "Размер" in profile["prompt_characteristics"]


def test_detect_wb_category_profile_maps_repair_catalog_alias_to_existing_profile():
    profiles = {
        "Строительство и ремонт": {
            "marketplace": "wb",
            "category": "Строительство и ремонт",
            "parent_category": "Строительство и ремонт",
            "match_keywords": ["сантехника"],
        }
    }
    catalog = {
        "categories": [
            {
                "path": "Для ремонта / Сантехника / Смесители",
                "name": "Смесители",
                "is_leaf": True,
            }
        ]
    }

    profile = detect_wb_category_profile(
        profiles,
        "Смеситель для раковины хром однорычажный латунный корпус",
        wb_categories=catalog,
    )

    assert profile is not None
    assert profile["category"] == "Строительство и ремонт"
    assert profile["detected_category_path"] == "Для ремонта / Сантехника / Смесители"
