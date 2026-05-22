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


def test_apply_ozon_generation_quality_keeps_explicit_electronics_fields_only():
    card = CardGeneration(
        title="Наушники беспроводные Bluetooth с микрофоном",
        description="Беспроводные наушники для музыки и звонков.",
        keywords="#наушники #bluetooth #микрофон",
        characteristics=(
            "Тип: Наушники\n"
            "Цвет: черный\n"
            "Наличие микрофона: Да\n"
            "Тип беспроводной связи: Bluetooth\n"
            "Конструкция наушников: Внутриканальные\n"
            "Шумоподавление: Активное\n"
            "Время работы: 6 ч\n"
            "Версия Bluetooth: 5.3\n"
            "Страна-изготовитель: Китай"
        ),
        marketplace="ozon",
    )
    profile = {
        "category": "Электроника",
        "prompt_characteristics": [
            "Тип",
            "Цвет",
            "Наличие микрофона",
            "Тип беспроводной связи",
            "Конструкция наушников",
            "Шумоподавление",
            "Время работы",
            "Версия Bluetooth",
            "Страна-изготовитель",
        ],
    }

    result = apply_ozon_generation_quality(
        card,
        category_profile=profile,
        user_input=(
            "Наушники беспроводные Bluetooth с микрофоном. Внутриканальные, "
            "есть активное шумоподавление, время работы 6 часов."
        ),
    )

    assert "Наличие микрофона: Да" in result.characteristics
    assert "Тип беспроводной связи: Bluetooth" in result.characteristics
    assert "Конструкция наушников: Внутриканальные" in result.characteristics
    assert "Шумоподавление: Активное" in result.characteristics
    assert "Время работы: 6 ч" in result.characteristics
    assert "Версия Bluetooth:" not in result.characteristics
    assert "Цвет:" not in result.characteristics


def test_apply_ozon_generation_quality_drops_wrong_mentioned_values():
    card = CardGeneration(
        title="Настольная лампа черная 12 Вт",
        description="Лампа для рабочего стола.",
        keywords="#лампа #настольная",
        characteristics="Цвет: черный\nМощность: 12 Вт\nСтрана-изготовитель: Китай",
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        category_profile={
            "category": "Электроника",
            "prompt_characteristics": ["Цвет", "Мощность", "Страна-изготовитель"],
        },
        user_input="Настольная лампа белая, мощность 5W",
    )

    assert "Цвет: черный" not in result.characteristics
    assert "Мощность: 12 Вт" not in result.characteristics
    assert "Страна-изготовитель: Китай" in result.characteristics


def test_apply_ozon_generation_quality_infers_explicit_electronics_fields_from_input():
    card = CardGeneration(
        title="Наушники беспроводные",
        description="Наушники для музыки и звонков.",
        keywords="#наушники #bluetooth",
        characteristics="Тип: Наушники\nСтрана-изготовитель: Китай",
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        category_profile={"category": "Электроника"},
        user_input="Наушники Bluetooth с микрофоном, внутриканальные, шумоподавление, время работы 8 часов",
    )

    assert "Тип беспроводной связи: Bluetooth" in result.characteristics
    assert "Наличие микрофона: Да" in result.characteristics
    assert "Конструкция наушников: Внутриканальные" in result.characteristics
    assert "Шумоподавление: Да" in result.characteristics
    assert "Время работы: 8 ч" in result.characteristics


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


def test_apply_ozon_generation_quality_overrides_unmentioned_country_to_china():
    card = CardGeneration(
        title="Средство для кухни антижир 500 мл",
        description="Средство для очистки кухонных поверхностей.",
        keywords="#антижир #кухня #чистящее_средство",
        characteristics=(
            "Тип: Средство для удаления жира\n"
            "Страна-изготовитель: Россия\n"
            "Цвет: прозрачный"
        ),
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        category_profile={"prompt_characteristics": ["Тип", "Цвет", "Страна-изготовитель"]},
        user_input="Средство для кухни антижир 500 мл",
    )

    assert "Страна-изготовитель: Китай" in result.characteristics
    assert "Страна-изготовитель: Россия" not in result.characteristics


def test_apply_ozon_generation_quality_replaces_unknown_country_placeholder():
    card = CardGeneration(
        title="Подгузники детские размер 4 60 штук",
        description="Подгузники для ежедневного ухода.",
        keywords="#подгузники #детские #размер_4",
        characteristics="Тип: Подгузники\nСтрана-изготовитель: Не указана",
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        category_profile={"prompt_characteristics": ["Тип", "Страна-изготовитель"]},
        user_input="Подгузники детские размер 4 60 штук",
    )

    assert "Страна-изготовитель: Китай" in result.characteristics
    assert "Не указана" not in result.characteristics


def test_apply_ozon_generation_quality_drops_non_applicable_and_unknown_values():
    card = CardGeneration(
        title="Аккумуляторная отвертка 3.6 В с LED подсветкой",
        description="Отвертка для мелкого ремонта.",
        keywords="#отвертка #инструмент #ремонт",
        characteristics=(
            "Тип: Отвертка аккумуляторная\n"
            "Время полного высыхания, ч: Не применимо\n"
            "Партномер: Не указан\n"
            "Страна-изготовитель: Не указана"
        ),
        marketplace="ozon",
    )

    result = apply_ozon_generation_quality(
        card,
        category_profile={
            "prompt_characteristics": [
                "Тип",
                "Время полного высыхания, ч",
                "Партномер",
                "Страна-изготовитель",
            ]
        },
        user_input="Аккумуляторная отвертка 3.6 В с LED подсветкой и реверсом",
    )

    assert "Тип: Отвертка аккумуляторная" in result.characteristics
    assert "Страна-изготовитель: Китай" in result.characteristics
    assert "Не применимо" not in result.characteristics
    assert "Не указан" not in result.characteristics
    assert "Партномер:" not in result.characteristics
