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
