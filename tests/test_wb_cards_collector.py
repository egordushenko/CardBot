from tools.wb_cards_collector import (
    build_card_record,
    extract_nmids_from_text,
    parse_card_info,
    parse_detail_product,
)


def test_extract_nmids_from_markdown_blocks():
    text = """
    **Женщинам/Одежда (3):**
    63077906, 54806389, 555301440

    dom-i-dacha/vannaya/kovriki?sort=popular:

    '334272823\\n239356519'
    """

    rows = extract_nmids_from_text(text)

    assert rows[:5] == [
        {"nmid": 63077906, "source_category": "Женщинам/Одежда"},
        {"nmid": 54806389, "source_category": "Женщинам/Одежда"},
        {"nmid": 555301440, "source_category": "Женщинам/Одежда"},
        {"nmid": 334272823, "source_category": "dom-i-dacha/vannaya/kovriki"},
        {"nmid": 239356519, "source_category": "dom-i-dacha/vannaya/kovriki"},
    ]


def test_parse_card_info_reads_description_and_characteristics():
    payload = {
        "imt_name": "Коврик для ванной",
        "subj_root_name": "Дом",
        "subj_name": "Коврики для ванной",
        "description": "Мягкий коврик для ванной комнаты.",
        "options": [
            {"name": "Состав", "value": "полиэстер 100%"},
            {"name": "Цвет", "value": "серый"},
        ],
    }

    parsed = parse_card_info(payload)

    assert parsed["title"] == "Коврик для ванной"
    assert parsed["category"] == "Дом / Коврики для ванной"
    assert parsed["description"] == "Мягкий коврик для ванной комнаты."
    assert parsed["characteristics"] == {
        "Состав": "полиэстер 100%",
        "Цвет": "серый",
    }


def test_parse_detail_product_reads_brand_and_reviews():
    product = {
        "id": 334272823,
        "brand": "Homely",
        "name": "Коврик для ванной",
        "reviewRating": 4.9,
        "feedbacks": 3100,
    }

    parsed = parse_detail_product(product)

    assert parsed == {
        "brand": "Homely",
        "title": "Коврик для ванной",
        "rating": 4.9,
        "reviews_count": 3100,
    }


def test_build_card_record_combines_info_and_detail():
    info = {
        "title": "Коврик для ванной",
        "category": "Дом / Коврики для ванной",
        "description": "Мягкий коврик для ванной комнаты.",
        "characteristics": {"Цвет": "серый"},
    }
    detail = {
        "brand": "Homely",
        "title": "Коврик Homely",
        "rating": 4.9,
        "reviews_count": 3100,
    }

    card = build_card_record(334272823, info, detail, "Дом / Ванная / Коврики")

    assert card["url"] == "https://www.wildberries.ru/catalog/334272823/detail.aspx"
    assert card["title"] == "Коврик Homely"
    assert card["category"] == "Дом / Ванная / Коврики"
    assert card["brand"] == "Homely"
    assert card["reviews_count"] == 3100
    assert card["hashtags"] == []
