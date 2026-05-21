from tools.ozon_cards_parser import (
    build_card_record,
    is_reference_card,
    parse_characteristics_from_text,
    parse_json_ld_products,
    parse_review_count,
)


def test_parse_characteristics_from_o_tovare_section():
    text = """
    О товаре
    Наличие микрофона
    Да
    Конструкция наушников
    Внутриканальные
    Шумоподавление
    Активное
    Тип беспроводной связи
    Bluetooth
    Фото
    """

    assert parse_characteristics_from_text(text) == {
        "Наличие микрофона": "Да",
        "Конструкция наушников": "Внутриканальные",
        "Шумоподавление": "Активное",
        "Тип беспроводной связи": "Bluetooth",
    }


def test_parse_characteristics_prefers_full_characteristics_section():
    text = """
    О товаре
    Перейти к описанию
    Сезон
    На любой сезон
    Фото и видео покупателей
    Характеристики
    Артикул
    2609226249
    Сезон
    На любой сезон
    Материал
    Хлопок, Лайкра
    Тип
    Футболка
    Цвет
    Escape-exhaust
    Вопросы
    """

    assert parse_characteristics_from_text(text) == {
        "Артикул": "2609226249",
        "Сезон": "На любой сезон",
        "Материал": "Хлопок, Лайкра",
        "Тип": "Футболка",
        "Цвет": "Escape-exhaust",
    }


def test_parse_characteristics_stops_before_reviews_and_supports_inline_pairs():
    text = """
    Характеристики
    Артикул
    1781292319
    Тип
    Витамины
    Направление витаминов: Для выносливости, Для мужского здоровья
    Информация о технических характеристиках, комплекте поставки, стране изготовления носит справочный характер.
    Подборки товаров в категории Витаминно-минеральные комплексы
    Отзывы о товаре
    39695
    """

    assert parse_characteristics_from_text(text) == {
        "Артикул": "1781292319",
        "Тип": "Витамины",
        "Направление витаминов": "Для выносливости, Для мужского здоровья",
    }


def test_parse_review_count_supports_thousands_variants():
    assert parse_review_count("1 234 отзыва") == 1234
    assert parse_review_count("1,2 тыс. отзывов") == 1200
    assert parse_review_count("2.5 тыс отзывов") == 2500


def test_parse_json_ld_products_extracts_product_fields():
    html = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Product",
      "name": "Беспроводные наушники Air Pro 3",
      "description": "Наушники с активным шумоподавлением",
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "1583"
      }
    }
    </script>
    """

    assert parse_json_ld_products(html) == [
        {
            "title": "Беспроводные наушники Air Pro 3",
            "description": "Наушники с активным шумоподавлением",
            "rating": 4.9,
            "review_count": 1583,
        }
    ]


def test_build_card_record_combines_json_ld_and_visible_characteristics():
    html = """
    <script type="application/ld+json">
    {"@type":"Product","name":"Наушники Bluetooth","description":"Описание товара","aggregateRating":{"ratingValue":"4.8","reviewCount":"2400"}}
    </script>
    О товаре
    Наличие микрофона
    Да
    Тип беспроводной связи
    Bluetooth
    Описание
    Подробное описание товара для покупателей.
    """

    record = build_card_record(html, source_url="https://www.ozon.ru/product/example-123/")

    assert record["source_url"] == "https://www.ozon.ru/product/example-123/"
    assert record["title"] == "Наушники Bluetooth"
    assert record["description"] == "Описание товара"
    assert record["rating"] == 4.8
    assert record["review_count"] == 2400
    assert record["characteristics"] == {
        "Наличие микрофона": "Да",
        "Тип беспроводной связи": "Bluetooth",
    }
    assert is_reference_card(record, min_rating=4.7, min_reviews=1000)
