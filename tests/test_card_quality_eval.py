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


def test_summarize_quality_results_counts_failures():
    passing = {"id": "ok", "issues": [], "score": 100}
    failing = {"id": "bad", "issues": ["description_too_short"], "score": 90}

    summary = summarize_quality_results([passing, failing])

    assert summary["total"] == 2
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["issue_counts"] == {"description_too_short": 1}
