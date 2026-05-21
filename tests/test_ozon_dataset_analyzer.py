from tools.ozon_dataset_analyzer import analyze_dataset, build_markdown_report


def test_analyze_dataset_builds_global_and_category_profiles():
    cards = [
        {
            "collection_target_category": "Электроника",
            "category": "Электроника / Наушники",
            "title": "Наушники беспроводные Bluetooth с шумоподавлением",
            "description": "Короткое описание товара для Ozon с преимуществами и сценариями.",
            "characteristics": {
                "Тип": "Наушники",
                "Цвет": "Черный",
                "Бренд": "TestBrand",
            },
            "hashtags": ["#наушники", "#bluetooth"],
        },
        {
            "collection_target_category": "Электроника",
            "category": "Электроника / Зарядные устройства",
            "title": "Зарядное устройство USB C быстрое",
            "description": "Описание зарядного устройства с мощностью, совместимостью и комплектацией.",
            "characteristics": {
                "Тип": "Зарядное устройство",
                "Цвет": "Белый",
                "Мощность, Вт": "65",
            },
            "hashtags": ["#зарядка", "#usb_c", "#быстрая_зарядка"],
        },
        {
            "collection_target_category": "Дом и сад",
            "category": "Дом и сад / Освещение",
            "title": "Лампа настольная LED белая",
            "description": "Описание лампы для рабочего стола, спальни и декоративного освещения.",
            "characteristics": {
                "Тип": "Лампа",
                "Цвет": "Белый",
                "Материал": "Пластик",
            },
            "hashtags": ["#лампа"],
        },
    ]

    report = analyze_dataset(cards)

    assert report["total_cards"] == 3
    assert report["global"]["title_length"]["avg"] == 36
    assert report["global"]["description_length"]["min"] > 0
    assert report["categories"]["Электроника"]["count"] == 2
    assert report["categories"]["Электроника"]["top_characteristics"][0] == ("Тип", 2)
    assert report["categories"]["Дом и сад"]["top_characteristics"][0] == ("Тип", 1)


def test_build_markdown_report_contains_actionable_prompt_rules():
    report = analyze_dataset([])
    markdown = build_markdown_report(report)

    assert "# Ozon dataset analysis" in markdown
    assert "## Prompt rules" in markdown
    assert "Title" in markdown
    assert "Description" in markdown
    assert "Characteristics" in markdown
