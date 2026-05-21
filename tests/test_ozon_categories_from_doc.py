from __future__ import annotations

from tools.build_ozon_categories_from_doc import (
    build_ozon_categories_payload,
    extract_json_payloads,
)


def test_extract_json_payloads_from_markdown():
    markdown = """
Text before.

{
  "page_url": "https://www.ozon.ru/",
  "root": "Unknown",
  "count": 3,
  "categories": [
    {"name": "Одежда", "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"},
    {"name": "Обувь", "url": "https://www.ozon.ru/category/obuv-17777/"},
    {"name": "Женская одежда", "url": "https://www.ozon.ru/category/zhenskaya-odezhda-7501/"}
  ]
}

Noise after.
"""

    payloads = extract_json_payloads(markdown)

    assert len(payloads) == 1
    assert payloads[0]["categories"][2]["name"] == "Женская одежда"


def test_build_ozon_categories_payload_removes_sidebar_and_infers_root():
    payloads = [
        {
            "page_url": "https://www.ozon.ru/",
            "root": "Unknown",
            "categories": [
                {"name": "Одежда", "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"},
                {"name": "Обувь", "url": "https://www.ozon.ru/category/obuv-17777/"},
                {"name": "Женская одежда", "url": "https://www.ozon.ru/category/zhenskaya-odezhda-7501/"},
                {"name": "Платья и сарафаны", "url": "https://www.ozon.ru/category/platya-zhenskie-7502/"},
            ],
        },
        {
            "page_url": "https://www.ozon.ru/",
            "root": "Unknown",
            "categories": [
                {"name": "Одежда", "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"},
                {"name": "Обувь", "url": "https://www.ozon.ru/category/obuv-17777/"},
                {"name": "Женская обувь", "url": "https://www.ozon.ru/category/zhenskaya-obuv-7640/"},
                {"name": "Кроссовки", "url": "https://www.ozon.ru/category/krossovki-zhenskie-7650/"},
            ],
        },
    ]

    payload = build_ozon_categories_payload(payloads)
    paths = {item["path"] for item in payload["categories"]}

    assert payload["payload_total"] == 2
    assert payload["sidebar_count"] == 2
    assert "Одежда" in paths
    assert "Обувь" in paths
    assert "Одежда / Женская одежда" in paths
    assert "Одежда / Платья и сарафаны" in paths
    assert "Обувь / Женская обувь" in paths
    assert "Обувь / Кроссовки" in paths
    assert payload["unresolved_payloads"] == []


def test_build_ozon_categories_payload_merges_seed_categories():
    payload = build_ozon_categories_payload(
        [],
        seed_categories={
            "categories": [
                {
                    "name": "Электроника",
                    "url": "https://www.ozon.ru/category/elektronika-15500/",
                    "subcategories": [
                        {
                            "name": "Смартфоны",
                            "url": "https://www.ozon.ru/category/smartfony-15502/",
                        }
                    ],
                }
            ]
        },
    )
    paths = {item["path"] for item in payload["categories"]}

    assert "Электроника" in paths
    assert "Электроника / Смартфоны" in paths


def test_build_ozon_categories_payload_infers_electronics_root():
    payload = build_ozon_categories_payload(
        [
            {
                "page_url": "https://www.ozon.ru/",
                "root": "Unknown",
                "categories": [
                    {"name": "Одежда", "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"},
                    {"name": "Обувь", "url": "https://www.ozon.ru/category/obuv-17777/"},
                    {"name": "Телефоны и смарт-часы", "url": "https://www.ozon.ru/category/telefony-i-smart-chasy-15501/"},
                    {"name": "Смартфоны", "url": "https://www.ozon.ru/category/smartfony-15502/"},
                ],
            },
            {
                "page_url": "https://www.ozon.ru/",
                "root": "Unknown",
                "categories": [
                    {"name": "Одежда", "url": "https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/"},
                    {"name": "Обувь", "url": "https://www.ozon.ru/category/obuv-17777/"},
                    {"name": "Женская обувь", "url": "https://www.ozon.ru/category/zhenskaya-obuv-7640/"},
                ],
            },
        ],
    )
    paths = {item["path"] for item in payload["categories"]}

    assert "Электроника / Телефоны и смарт-часы" in paths
    assert "Электроника / Смартфоны" in paths
