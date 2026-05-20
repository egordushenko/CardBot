from tools.ozon_dataset_audit import (
    RECOMMENDED_CATEGORY_TARGETS,
    audit_dataset,
    build_markdown_report,
)


def test_audit_dataset_detects_quality_issues_and_duplicates():
    cards = [
        {
            "product_id": "1",
            "source_url": "https://www.ozon.ru/product/a-1/",
            "category": "Дом и сад / Освещение",
            "title": "Настольная лампа",
            "description": "Описание лампы",
            "rating": 4.8,
            "review_count": 1500,
            "characteristics": {"Тип": "Лампа", "Цвет": "Белый"},
            "hashtags": ["#лампа", "#свет"],
        },
        {
            "product_id": "1",
            "source_url": "https://www.ozon.ru/product/a-1/",
            "category": "Дом и сад / Освещение",
            "title": "",
            "description": "short",
            "rating": 4.1,
            "review_count": 10,
            "characteristics": {},
            "hashtags": [],
        },
    ]

    report = audit_dataset(cards)

    assert report["total_cards"] == 2
    assert report["duplicate_product_ids"] == ["1"]
    assert report["duplicate_source_urls"] == ["https://www.ozon.ru/product/a-1/"]
    assert report["quality"]["invalid_cards"] == 1
    assert "missing_title" in report["quality"]["issues"][1]
    assert "low_rating" in report["quality"]["issues"][1]
    assert report["category_counts"]["Дом и сад"] == 2


def test_audit_dataset_calculates_category_deficits():
    cards = [
        {
            "product_id": str(index),
            "source_url": f"https://www.ozon.ru/product/item-{index}/",
            "category": "Электроника / Смартфоны",
            "title": f"Смартфон {index}",
            "description": "Описание смартфона",
            "rating": 4.9,
            "review_count": 2000,
            "characteristics": {"Тип": "Смартфон"},
            "hashtags": ["#смартфон"],
        }
        for index in range(3)
    ]

    report = audit_dataset(cards)

    assert report["category_targets"]["Электроника"]["current"] == 3
    assert report["category_targets"]["Электроника"]["target"] == RECOMMENDED_CATEGORY_TARGETS["Электроника"]
    assert report["category_targets"]["Электроника"]["missing"] == RECOMMENDED_CATEGORY_TARGETS["Электроника"] - 3


def test_build_markdown_report_contains_core_sections():
    report = audit_dataset([])
    markdown = build_markdown_report(report)

    assert "# Ozon dataset audit" in markdown
    assert "## Quality" in markdown
    assert "## Category coverage" in markdown
    assert "## Recommendations" in markdown
