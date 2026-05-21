from llm import CardGeneration
from wb_generation_quality import apply_wb_generation_quality, validate_wb_generation


def test_validate_wb_generation_reports_missing_required_characteristics():
    card = CardGeneration(
        title="Кроссовки женские летние",
        description="Легкие кроссовки для прогулок.",
        keywords="",
        characteristics="Цвет: белый\nСезон: Лето",
        marketplace="wb",
    )
    profile = {
        "category": "Обувь",
        "required_characteristics": ["Цвет", "Пол", "Сезон"],
        "characteristics_target_min": 8,
    }

    report = validate_wb_generation(card, profile)

    assert report["missing_required_characteristics"] == ["Пол"]
    assert "too_few_characteristics" in report["issues"]


def test_apply_wb_generation_quality_adds_placeholders_and_clears_keywords():
    card = CardGeneration(
        title="Кроссовки женские летние со скидкой",
        description="Представляем вашему вниманию легкие кроссовки.",
        keywords="кроссовки женские, обувь",
        characteristics="Цвет: белый\nСезон: Лето",
        marketplace="wb",
    )
    profile = {
        "category": "Обувь",
        "required_characteristics": ["Цвет", "Пол", "Сезон"],
        "recommended_characteristics": ["Материал стельки"],
        "characteristics_target_min": 8,
    }

    result = apply_wb_generation_quality(card, profile)

    assert result.keywords == ""
    assert "Пол: [укажите пол]" in result.characteristics
    assert "Материал стельки: [укажите материал стельки]" in result.characteristics
    assert "скидк" not in result.title.lower()
    assert "Представляем вашему вниманию" not in result.description
