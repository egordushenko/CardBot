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


def test_apply_wb_generation_quality_does_not_add_unknown_characteristics():
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
    assert "Пол:" not in result.characteristics
    assert "Материал стельки:" not in result.characteristics
    assert "Страна производства: Китай" in result.characteristics
    assert "скидк" not in result.title.lower()
    assert "Представляем вашему вниманию" not in result.description


def test_apply_wb_generation_quality_removes_secondary_placeholders_and_defaults_country():
    card = CardGeneration(
        title="Настольная лампа LED спиральная белая, USB, 35 см",
        description=(
            "Стильная настольная лампа в форме спирали. "
            "Корпус выполнен из качественного пластика. "
            "Адаптер не входит в комплект. "
            "Идеальный выбор для тех, кто ценит функциональность. "
            "Подходит для рабочего стола и прикроватной тумбы."
        ),
        keywords="",
        characteristics=(
            "Цвет: белый\n"
            "Тип лампы: LED\n"
            "Материал изделия: [укажите материал]\n"
            "Комплектация: [укажите комплектацию]\n"
            "Длина упаковки: [укажите значение]\n"
            "Требуется сборка: Нет"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Электроника", "characteristics_target_min": 10},
        user_input=(
            "Настольная лампа LED спиральная белая. Подключение USB, мощность 5W. "
            "Три режима света. Высота примерно 35 см. Цвет белый."
        ),
    )

    assert result.title == "Настольная лампа LED спиральная белая USB 35 см"
    assert "Страна производства: Китай" in result.characteristics
    assert "Материал изделия:" not in result.characteristics
    assert "Комплектация: Настольная лампа; USB-кабель" in result.characteristics
    assert "Длина упаковки:" not in result.characteristics
    assert "Требуется сборка:" not in result.characteristics
    assert "пластик" not in result.description.lower()
    assert "комплект" not in result.description.lower()
    assert "Стильная" not in result.description
    assert "функциональность" not in result.description


def test_apply_wb_generation_quality_preserves_explicit_country():
    card = CardGeneration(
        title="Крем для рук",
        description="Крем произведен в России.",
        keywords="",
        characteristics="Страна производства: Россия\nТип: крем",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        user_input="Крем для рук, страна производства Россия",
    )

    assert "Страна производства: Россия" in result.characteristics


def test_apply_wb_generation_quality_does_not_infer_usb_kit_when_cable_excluded():
    card = CardGeneration(
        title="Настольная лампа LED USB",
        description="Настольная лампа подключается по USB.",
        keywords="",
        characteristics="Тип лампы: LED",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        user_input="Настольная лампа USB, кабель не входит в комплект",
    )

    assert "Комплектация:" not in result.characteristics
