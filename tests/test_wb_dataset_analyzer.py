from tools.wb_dataset_analyzer import analyze_dataset, build_markdown_report


def test_analyze_dataset_builds_wb_category_profiles():
    cards = [
        {
            "category": "Дом / Ванная / Коврики",
            "title": "Коврик для ванной",
            "description": "Мягкий коврик для ванной комнаты.",
            "characteristics": {"Состав": "полиэстер", "Цвет": "серый"},
            "hashtags": [],
        },
        {
            "category": "Дом / Ванная / Шторы",
            "title": "Штора для ванной",
            "description": "Водонепроницаемая штора для ванной.",
            "characteristics": {"Состав": "полиэстер", "Материал": "PEVA"},
            "hashtags": [],
        },
    ]

    report = analyze_dataset(cards)

    assert report["total_cards"] == 2
    assert report["categories"]["Дом"]["count"] == 2
    assert report["categories"]["Дом"]["top_characteristics"][0] == ("Состав", 2)
    assert report["global"]["hashtags_count"]["avg"] == 0


def test_build_markdown_report_mentions_wb_and_empty_hashtags():
    markdown = build_markdown_report(analyze_dataset([]))

    assert "# Wildberries dataset analysis" in markdown
    assert "по правилам WB" in markdown
    assert "поле оставляем пустым массивом" in markdown
