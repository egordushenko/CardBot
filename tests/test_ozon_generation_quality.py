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


def test_apply_ozon_generation_quality_drops_unmentioned_isbn():
    card = CardGeneration(
        title="Книга по саморазвитию",
        description="Книга для чтения.",
        keywords="#книга #чтение #саморазвитие",
        characteristics=(
            "Тип: Книга\n"
            "ISBN: 978-5-00000-000-0\n"
            "Автор: Иван Иванов\n"
            "Страна-изготовитель: Китай"
        ),
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        category_profile={
            "prompt_characteristics": ["Тип", "ISBN", "Автор", "Страна-изготовитель"],
        },
        user_input="Книга по саморазвитию в мягкой обложке",
    )

    assert "Тип: Книга" in result.characteristics
    assert "ISBN:" not in result.characteristics
    assert "Автор:" not in result.characteristics


def test_apply_ozon_generation_quality_limits_and_deduplicates_similar_hashtags():
    repeated_tags = " ".join(
        [
            "#коврик_для_ванной",
            "#коврик_для_ванной_комнаты",
            "#коврик_для_ванны",
            "#коврик_для_душа",
            "#коврик_для_душевой",
            "#серый_коврик",
            "#коврик_серый",
            "#мягкий_ворс",
            "#коврик_с_ворсом",
            "#нескользящий_коврик",
            "#коврик_против_скольжения",
            "#впитывающий_коврик",
            "#коврик_впитывающий",
            "#ванная_комната",
            "#безопасность_в_ванной",
            "#текстиль_для_ванной",
            "#коврик_для_пола",
            "#коврик_на_пол",
            "#коврик_для_унитаза",
            "#коврик_для_раковины",
        ]
    )
    card = CardGeneration(
        title="Коврик для ванной серый 50x80 см",
        description="Коврик для ванной комнаты.",
        keywords=repeated_tags,
        characteristics="Тип: Коврик для ванной\nЦвет: Серый",
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        user_input="Коврик для ванной серый. Размер 50 на 80 см.",
    )

    tags = result.keywords.split()
    assert 12 <= len(tags) <= 18
    assert "#коврик_для_ванной_комнаты" not in tags
    assert "#коврик_для_ванны" not in tags
    assert "#коврик_серый" not in tags
    assert "#коврик_для_душевой" not in tags
    assert "#коврик_на_пол" not in tags


def test_apply_ozon_generation_quality_adds_safe_purpose_and_kit_from_input():
    card = CardGeneration(
        title="Коврик для ванной серый 50x80 см",
        description="Коврик для ванной комнаты.",
        keywords="#коврик #ванная #серый",
        characteristics="Тип: Коврик для ванной\nЦвет: Серый\nРазмер: 50x80 см",
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        user_input=(
            "Коврик для ванной серый. Размер 50 на 80 см. Подходит для ванной комнаты, "
            "душевой зоны и туалета."
        ),
    )

    assert "Назначение: для ванной комнаты, душевой зоны и туалета" in result.characteristics
    assert "Комплектация: коврик" in result.characteristics
