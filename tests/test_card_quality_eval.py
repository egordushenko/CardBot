from llm import CardGeneration
from tools.card_quality_eval import evaluate_card_quality, summarize_quality_results


def test_evaluate_card_quality_flags_weak_wb_card():
    card = CardGeneration(
        title="Футболка женская оверсайз черная",
        description="Женская футболка свободного кроя.",
        keywords="футболка женская",
        characteristics=(
            "Цвет: черный\n"
            "Ширина предмета: свободная\n"
            "Высота предмета: стандартная"
        ),
        marketplace="wb",
    )

    result = evaluate_card_quality(
        card,
        user_input="Женская футболка оверсайз черная",
    )

    assert "description_too_short" in result["issues"]
    assert "wb_keywords_present" in result["issues"]
    assert "missing_country" in result["issues"]
    assert "forbidden_characteristic_field:Ширина предмета" in result["issues"]
    assert "forbidden_characteristic_field:Высота предмета" in result["issues"]


def test_evaluate_card_quality_accepts_grounded_wb_card():
    description = (
        "Женская футболка оверсайз подходит для повседневных образов, прогулок и "
        "расслабленных комплектов на каждый день. Свободный крой не сковывает движения, "
        "а черный цвет легко сочетается с джинсами, брюками, юбкой и спортивной одеждой. "
        "Модель можно носить дома, на учебу, в поездку или как базовый слой под рубашку "
        "и куртку. Футболка помогает быстро собрать аккуратный образ без лишних деталей."
    )
    card = CardGeneration(
        title="Футболка женская оверсайз черная",
        description=description,
        keywords="",
        characteristics=(
            "Цвет: черный\n"
            "Покрой: свободный\n"
            "Пол: Женский\n"
            "Состав: 100% хлопок\n"
            "Страна производства: Китай"
        ),
        marketplace="wb",
    )

    result = evaluate_card_quality(
        card,
        user_input="Женская футболка оверсайз черная",
    )

    assert result["issues"] == []
    assert result["score"] == 100


def test_evaluate_card_quality_flags_unmentioned_factual_characteristics():
    card = CardGeneration(
        title="Настольная лампа LED черная 12 Вт",
        description=(
            "Настольная лампа подходит для рабочего стола и помогает организовать комфортное освещение. "
            "Ее можно использовать дома, в офисе и в зоне учебы, чтобы сделать повседневные задачи удобнее."
        ),
        keywords="",
        characteristics=(
            "Цвет: черный\n"
            "Мощность: 12 Вт\n"
            "Страна производства: Китай\n"
            "Комплектация: лампа"
        ),
        marketplace="wb",
    )

    result = evaluate_card_quality(card, user_input="Настольная лампа")

    assert "hallucinated_characteristic_value:Цвет" in result["issues"]
    assert "hallucinated_characteristic_value:Мощность" in result["issues"]
    assert "hallucinated_characteristic_value:Комплектация" not in result["issues"]
    assert "hallucinated_characteristic_value:Страна производства" not in result["issues"]


def test_evaluate_card_quality_uses_wb_category_characteristics_target():
    card = CardGeneration(
        title="Коврик для ванной серый 50x80",
        description=(
            "Коврик для ванной помогает сделать пол после душа безопаснее и приятнее для ног. "
            "Мягкая поверхность подходит для зоны ванной, душевой кабины и туалета, а спокойный серый цвет "
            "легко сочетается с разными интерьерами. Размер 50x80 см закрывает основную мокрую зону."
        ),
        keywords="",
        characteristics=(
            "Тип: коврик для ванной\n"
            "Цвет: серый\n"
            "Размер: 50x80 см\n"
            "Страна производства: Китай\n"
            "Комплектация: коврик"
        ),
        marketplace="wb",
    )

    result = evaluate_card_quality(
        card,
        user_input="Коврик для ванной серый. Размер 50 на 80 см.",
        category_profile={
            "category": "Дом / Ванная / Коврики",
            "characteristics_target_min": 8,
            "prompt_characteristics": ["Тип", "Цвет", "Размер", "Страна производства", "Комплектация"],
        },
    )

    assert "too_few_characteristics" in result["issues"]


def test_evaluate_card_quality_counts_only_clean_wb_characteristics_toward_target():
    card = CardGeneration(
        title="Коврик для ванной серый 50x80",
        description=(
            "Коврик для ванной помогает сделать пол после душа безопаснее и приятнее для ног. "
            "Мягкая поверхность подходит для зоны ванной, душевой кабины и туалета, а спокойный серый цвет "
            "легко сочетается с разными интерьерами. Размер 50x80 см закрывает основную мокрую зону."
        ),
        keywords="",
        characteristics=(
            "Тип: коврик для ванной\n"
            "Цвет: серый\n"
            "Размер: 50x80 см\n"
            "Страна производства: Китай\n"
            "Комплектация: коврик\n"
            "Длина упаковки: 50 см\n"
            "Ширина упаковки: 10 см\n"
            "Длина предмета: 80 см\n"
            "Материал изделия: микрофибра"
        ),
        marketplace="wb",
    )

    result = evaluate_card_quality(
        card,
        user_input="Коврик для ванной серый. Размер 50 на 80 см.",
        category_profile={
            "category": "Дом / Ванная / Коврики",
            "characteristics_target_min": 6,
            "prompt_characteristics": ["Тип", "Цвет", "Размер", "Страна производства", "Комплектация", "Материал изделия"],
        },
    )

    assert "forbidden_characteristic_field:Длина упаковки" in result["issues"]
    assert "forbidden_characteristic_field:Ширина упаковки" in result["issues"]
    assert "forbidden_characteristic_field:Длина предмета" in result["issues"]
    assert "hallucinated_characteristic_value:Материал изделия" in result["issues"]
    assert "too_few_grounded_characteristics" in result["issues"]


def test_evaluate_card_quality_flags_wrong_mentioned_characteristic_values():
    card = CardGeneration(
        title="Настольная лампа черная 12 Вт",
        description=(
            "Настольная лампа подходит для рабочего стола, прикроватной зоны и учебного места. "
            "Она помогает организовать локальное освещение дома или в офисе и не занимает много места."
        ),
        keywords="",
        characteristics="Цвет: черный\nМощность: 12 Вт\nСтрана производства: Китай",
        marketplace="wb",
    )

    result = evaluate_card_quality(
        card,
        user_input="Настольная лампа белая, мощность 5 Вт",
    )

    assert "hallucinated_characteristic_value:Цвет" in result["issues"]
    assert "hallucinated_characteristic_value:Мощность" in result["issues"]


def test_evaluate_card_quality_flags_missing_clothing_composition_user_data():
    card = CardGeneration(
        title="Платье женское летнее",
        description=(
            "Платье подходит для прогулок, отдыха и повседневных образов. "
            "Свободная посадка помогает чувствовать себя комфортно в течение дня, "
            "а базовый крой легко сочетается с разной обувью и аксессуарами."
        ),
        keywords="",
        characteristics="Пол: женский\nСтрана производства: Китай\nКомплектация: платье\nЦвет: синий",
        marketplace="wb",
    )

    result = evaluate_card_quality(
        card,
        user_input="Женское летнее платье синее",
        category_profile={"category": "Женщинам / Одежда", "required_generation_characteristics": ["Состав"]},
    )

    assert "missing_required_user_data:Состав" in result["issues"]


def test_evaluate_card_quality_flags_weak_ozon_card():
    card = CardGeneration(
        title="Беспроводные наушники Bluetooth",
        description="Наушники для музыки.",
        keywords="#наушники",
        characteristics=(
            "Тип: Наушники\n"
            "Bluetooth: Да\n"
            "Добавить к сравнению: Да"
        ),
        marketplace="ozon",
    )

    result = evaluate_card_quality(
        card,
        user_input="Беспроводные наушники черные Bluetooth с микрофоном",
    )

    assert "description_too_short" in result["issues"]
    assert "ozon_too_few_hashtags" in result["issues"]
    assert "missing_country" in result["issues"]
    assert "forbidden_characteristic_field:Bluetooth" in result["issues"]
    assert "forbidden_characteristic_field:Добавить к сравнению" in result["issues"]


def test_evaluate_card_quality_flags_ozon_wrong_default_country():
    card = CardGeneration(
        title="Средство для кухни антижир 500 мл",
        description=(
            "Средство помогает быстро очистить кухонные поверхности от жира и следов готовки. "
            "Подходит для плиты, вытяжки, фартука и рабочей зоны, упрощает ежедневную уборку."
        ),
        keywords="#антижир #кухня #уборка",
        characteristics="Тип: Средство для удаления жира\nСтрана-изготовитель: Россия",
        marketplace="ozon",
    )

    result = evaluate_card_quality(
        card,
        user_input="Средство для кухни антижир 500 мл",
    )

    assert "hallucinated_characteristic_value:Страна-изготовитель" in result["issues"]


def test_evaluate_card_quality_flags_unknown_and_non_applicable_values():
    card = CardGeneration(
        title="Аккумуляторная отвертка 3.6 В",
        description=(
            "Аккумуляторная отвертка подходит для сборки мебели и мелкого ремонта. "
            "Компактный корпус удобно держать в руке, а подсветка помогает работать в плохо освещенных местах."
        ),
        keywords="#отвертка #инструмент #ремонт",
        characteristics=(
            "Тип: Отвертка аккумуляторная\n"
            "Партномер: Не указан\n"
            "Время полного высыхания, ч: Не применимо\n"
            "Страна-изготовитель: Не указана"
        ),
        marketplace="ozon",
    )

    result = evaluate_card_quality(
        card,
        user_input="Аккумуляторная отвертка 3.6 В с LED подсветкой",
        category_profile={
            "prompt_characteristics": [
                "Тип",
                "Партномер",
                "Время полного высыхания, ч",
                "Страна-изготовитель",
            ]
        },
    )

    assert "placeholder_characteristic_value:Партномер" in result["issues"]
    assert "placeholder_characteristic_value:Время полного высыхания, ч" in result["issues"]
    assert "placeholder_characteristic_value:Страна-изготовитель" in result["issues"]


def test_evaluate_card_quality_accepts_wb_pet_food_weight_from_packaging_input():
    card = CardGeneration(
        title="Сухой корм для кошек с курицей 1 кг",
        description=(
            "Сухой корм для взрослых кошек подходит для ежедневного рациона. "
            "Куриный вкус помогает поддерживать интерес к корму, а удобная упаковка подходит для дома."
        ),
        keywords="",
        characteristics=(
            "Тип: сухой корм\n"
            "Вид животного: кошки\n"
            "Вкус: курица\n"
            "Назначение: Для взрослых кошек\n"
            "Страна производства: Китай\n"
            "Вес: 1 кг"
        ),
        marketplace="wb",
    )

    result = evaluate_card_quality(
        card,
        user_input="Сухой корм для кошек с курицей. Для взрослых кошек, упаковка 1 кг.",
        category_profile={"category": "Товары для животных", "characteristics_target_min": 5},
    )

    assert "hallucinated_characteristic_value:Вес" not in result["issues"]


def test_summarize_quality_results_counts_failures():
    passing = {"id": "ok", "issues": [], "score": 100}
    failing = {"id": "bad", "issues": ["description_too_short"], "score": 90}

    summary = summarize_quality_results([passing, failing])

    assert summary["total"] == 2
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["issue_counts"] == {"description_too_short": 1}
