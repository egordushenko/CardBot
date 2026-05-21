import json
from pathlib import Path

from tools.quality_dashboard import build_quality_dashboard, write_quality_dashboard


def test_build_quality_dashboard_groups_metrics_by_marketplace_category():
    report = {
        "results": [
            {
                "marketplace": "ozon",
                "category": "Дом и сад",
                "description": "a" * 100,
                "keywords": "#one #two",
                "characteristics": "Тип: Коврик\nЦвет: Серый",
                "issues": [],
            },
            {
                "marketplace": "ozon",
                "category": "Дом и сад",
                "description": "b" * 200,
                "keywords": "#one",
                "characteristics": "Тип: Лампа",
                "issues": ["parse_error"],
            },
            {
                "marketplace": "wb",
                "category": "Обувь",
                "description": "c" * 80,
                "keywords": "",
                "characteristics": "Цвет: Белый\nПол: Мужской\nРазмер: 42",
                "issues": [],
            },
        ]
    }

    dashboard = build_quality_dashboard(report)

    ozon_home = dashboard["categories"]["ozon / Дом и сад"]
    assert ozon_home["cases"] == 2
    assert ozon_home["avg_description_length"] == 150
    assert ozon_home["avg_characteristics_count"] == 1.5
    assert ozon_home["avg_hashtags_count"] == 1.5
    assert ozon_home["issue_counts"] == {"parse_error": 1}

    wb_shoes = dashboard["categories"]["wb / Обувь"]
    assert wb_shoes["avg_hashtags_count"] == 0
    assert wb_shoes["avg_characteristics_count"] == 3


def test_write_quality_dashboard_creates_json_and_md(tmp_path: Path):
    source = tmp_path / "eval.json"
    json_path = tmp_path / "dashboard.json"
    md_path = tmp_path / "dashboard.md"
    source.write_text(
        json.dumps(
            {
                "summary": {"total": 1, "passed": 1, "failed": 0},
                "results": [
                    {
                        "id": "case",
                        "marketplace": "ozon",
                        "category": "Дом и сад",
                        "description": "Описание",
                        "keywords": "#tag",
                        "characteristics": "Тип: Коврик",
                        "issues": [],
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    write_quality_dashboard(source, json_path, md_path)

    assert "ozon / Дом и сад" in json_path.read_text(encoding="utf-8")
    assert "| ozon / Дом и сад | 1 |" in md_path.read_text(encoding="utf-8")
