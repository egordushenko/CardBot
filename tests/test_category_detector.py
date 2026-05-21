from category_detector import _deterministic_category_override, _heuristic_detect_category


OZON_CATEGORIES = ["Автотовары", "Дом и сад", "Спорт и отдых"]


def test_deterministic_category_override_detects_bath_mat_as_home():
    assert (
        _deterministic_category_override(
            "Коврик для ванной серый 50 на 80 см, подходит для душевой зоны и туалета.",
            OZON_CATEGORIES,
        )
        == "Дом и сад"
    )


def test_deterministic_category_override_keeps_car_mats_as_auto():
    assert (
        _deterministic_category_override(
            "Автомобильные коврики резиновые черные для Lada Granta, комплект 4 штуки.",
            OZON_CATEGORIES,
        )
        == "Автотовары"
    )


def test_heuristic_category_does_not_treat_plain_bath_mat_as_auto():
    assert (
        _heuristic_detect_category(
            "Коврик для ванной серый, мягкий ворс, нескользящее основание.",
            OZON_CATEGORIES,
        )
        == "Дом и сад"
    )
