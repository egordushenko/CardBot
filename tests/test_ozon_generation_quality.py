from llm import CardGeneration
from ozon_generation_quality import apply_ozon_generation_quality


def test_apply_ozon_generation_quality_drops_service_and_parser_fields():
    card = CardGeneration(
        title="Коврик для ванной серый 50x80",
        description="Коврик для ванной комнаты.",
        keywords="#коврик #для_ванной",
        characteristics=(
            "Артикул: 12345\n"
            "Добавить к сравнению: Да\n"
            "Китай: Китай\n"
            "20: 20\n"
            "Цвет: серый\n"
            "Размер: 50x80 см\n"
            "Упаковка: пакет\n"
            "Вес товара, г: 400\n"
            "Страна-изготовитель: Китай"
        ),
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        category_profile={"prompt_characteristics": ["Цвет", "Размер"]},
        user_input="Коврик для ванной серый. Размер 50 на 80 см.",
    )

    assert "Цвет: серый" in result.characteristics
    assert "Размер: 50x80 см" in result.characteristics
    assert "Страна-изготовитель: Китай" in result.characteristics
    assert "Артикул:" not in result.characteristics
    assert "Добавить к сравнению:" not in result.characteristics
    assert "Китай:" not in result.characteristics
    assert "20:" not in result.characteristics
    assert "Упаковка:" not in result.characteristics
    assert "Вес товара, г:" not in result.characteristics


def test_apply_ozon_generation_quality_drops_freeform_fields_not_in_profile():
    card = CardGeneration(
        title="Рюкзак городской мужской черный",
        description="Рюкзак для города.",
        keywords="#рюкзак",
        characteristics=(
            "Цвет: черный\n"
            "Материал: полиэстер\n"
            "Объем, л: 22\n"
            "Мягкая спинка: Да\n"
            "Карман для бутылки: Да\n"
            "Водоотталкивающая пропитка: Да"
        ),
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        category_profile=None,
        user_input="Рюкзак городской мужской черный. Объем 22 литра. Материал полиэстер.",
    )

    assert "Цвет: черный" in result.characteristics
    assert "Материал: полиэстер" in result.characteristics
    assert "Объем, л: 22" in result.characteristics
    assert "Мягкая спинка:" not in result.characteristics
    assert "Карман для бутылки:" not in result.characteristics
    assert "Водоотталкивающая пропитка:" not in result.characteristics
