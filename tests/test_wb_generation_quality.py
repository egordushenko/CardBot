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


def test_apply_wb_generation_quality_removes_clothing_size_and_composition_from_title():
    card = CardGeneration(
        title="Рашгард Therapy черный M 100% хлопок облегающий",
        description="Рашгард для тренировок.",
        keywords="",
        characteristics=(
            "Цвет: черный\n"
            "Состав: 100% хлопок\n"
            "Страна производства: Китай\n"
            "Комплектация: рашгард\n"
            "Назначение: для спорта\n"
            "Материал изделия: хлопок"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Мужчинам / Одежда / Рашгарды"},
        user_input=(
            "Рашгард therapy черный размер M, 100% хлопок, тянущийся облегающий "
            "с горловиной качественная печать текста на спине (Therapy)"
        ),
    )

    assert result.title == "Рашгард Therapy черный облегающий"
    assert "Состав: 100% хлопок" in result.characteristics
    assert "Материал изделия:" not in result.characteristics


def test_apply_wb_generation_quality_removes_rashguard_size_without_category_profile():
    card = CardGeneration(
        title="Рашгард Therapy черный M",
        description="Рашгард для тренировок.",
        keywords="",
        characteristics="Цвет: черный\nСостав: 100% хлопок",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        user_input="Рашгард Therapy черный размер M 100% хлопок с принтом на спине",
    )

    assert result.title == "Рашгард Therapy черный"
    assert " M " not in f" {result.title} "
    assert "100% хлопок" not in result.title



def test_apply_wb_generation_quality_converts_live_clothing_material_to_composition():
    card = CardGeneration(
        title="Рашгард Therapy черный M 100% хлопок облегающий с принтом",
        description="Рашгард с принтом Therapy создан для тренировок.",
        keywords="",
        characteristics=(
            "Страна производства: Китай\n"
            "Цвет: Черный\n"
            "Материал изделия: 100% хлопок\n"
            "Назначение: для спорта и повседневной носки\n"
            "Комплектация: рашгард"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Мужчинам / Одежда / Рашгарды"},
        user_input=(
            "Рашгард therapy черный размер M, 100% хлопок, тянущийся облегающий "
            "с горловиной качественная печать текста на спине (Therapy)"
        ),
    )

    assert result.title == "Рашгард Therapy черный облегающий с принтом"
    assert " M " not in f" {result.title} "
    assert "100% хлопок" not in result.title
    assert "Состав: 100% хлопок" in result.characteristics
    assert "Материал изделия:" not in result.characteristics


def test_apply_wb_generation_quality_drops_unmentioned_factual_values():
    card = CardGeneration(
        title="Настольная лампа LED черная 12 Вт",
        description="Настольная лампа для рабочего стола.",
        keywords="",
        characteristics=(
            "Цвет: черный\n"
            "Тип лампы: LED\n"
            "Мощность: 12 Вт\n"
            "Регулировка яркости: есть\n"
            "Страна производства: Китай"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Электроника"},
        user_input="Настольная лампа",
    )

    assert "Цвет:" not in result.characteristics
    assert "Тип лампы:" not in result.characteristics
    assert "Мощность:" not in result.characteristics
    assert "Регулировка яркости:" not in result.characteristics
    assert "Страна производства: Китай" in result.characteristics


def test_apply_wb_generation_quality_drops_wrong_mentioned_values():
    card = CardGeneration(
        title="Футболка женская оверсайз черная",
        description="Женская футболка оверсайз.",
        keywords="",
        characteristics="Цвет: черный\nСостав: полиэстер\nСтрана производства: Китай",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        user_input="Женская футболка оверсайз белая",
        category_profile={"category": "Женщинам / Одежда"},
    )

    assert "Цвет: черный" not in result.characteristics
    assert "Состав: 100% хлопок" in result.characteristics


def test_apply_wb_generation_quality_adds_adaptive_clothing_composition():
    card = CardGeneration(
        title="Футболка женская черная базовая",
        description="Женская футболка для повседневной носки.",
        keywords="",
        characteristics="Цвет: черный\nПол: женский\nСтрана производства: Китай",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Женщинам / Одежда"},
        user_input="Женская футболка черная",
    )

    assert "Состав: 100% хлопок" in result.characteristics


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


def test_apply_wb_generation_quality_drops_non_numeric_dimension_fields():
    card = CardGeneration(
        title="Футболка женская оверсайз черная",
        description="Женская футболка свободного кроя.",
        keywords="",
        characteristics=(
            "Цвет: черный\n"
            "Состав: полиэстер\n"
            "Ширина предмета: свободная\n"
            "Высота предмета: стандартная\n"
            "Состояние товара: новое"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Женщинам / Одежда"},
        user_input="Женская футболка оверсайз черная",
    )

    assert "Ширина предмета:" not in result.characteristics
    assert "Высота предмета:" not in result.characteristics
    assert "Состояние товара:" not in result.characteristics
    assert "Покрой: свободный" in result.characteristics
    assert "Состав: 100% хлопок" in result.characteristics


def test_apply_wb_generation_quality_converts_item_dimensions_to_size():
    card = CardGeneration(
        title="Настольная лампа LED",
        description="Настольная лампа.",
        keywords="",
        characteristics="Высота предмета: 35 см\nШирина предмета: 12 см",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Электроника"},
        user_input="Настольная лампа высота 35 см ширина 12 см",
    )

    assert "Высота предмета:" not in result.characteristics
    assert "Ширина предмета:" not in result.characteristics
    assert "Размер: 35 см" in result.characteristics


def test_apply_wb_generation_quality_keeps_ml_volume_when_grounded():
    card = CardGeneration(
        title="Шампунь увлажняющий 400 мл",
        description="Шампунь для ухода за волосами.",
        keywords="",
        characteristics="Тип: шампунь\nОбъем: 400 мл\nСтрана производства: Китай",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Красота"},
        user_input="Шампунь увлажняющий 400 мл для волос",
    )

    assert "Объем: 400 мл" in result.characteristics


def test_apply_wb_generation_quality_drops_packaging_if_user_did_not_provide_packaging():
    card = CardGeneration(
        title="Коврик для ванной серый противоскользящий 50x80",
        description="Коврик для ванной комнаты с мягким ворсом.",
        keywords="",
        characteristics=(
            "Цвет: серый\n"
            "Форма коврика: прямоугольный\n"
            "Размер коврика: 50x80 см\n"
            "Основа коврика: противоскользящая\n"
            "Длина упаковки: 50 см\n"
            "Ширина упаковки: 10 см\n"
            "Высота упаковки: 10 см\n"
            "Вес с упаковкой (кг): 0.4"
        ),
        marketplace="wb",
    )
    profile = {
        "category": "Дом / Ванная / Коврики",
        "prompt_characteristics": [
            "Цвет",
            "Форма коврика",
            "Размер коврика",
            "Основа коврика",
        ],
    }

    result = apply_wb_generation_quality(
        card,
        category_profile=profile,
        user_input="Коврик для ванной серый. Размер 50 на 80 см. Мягкий ворс, нескользящее основание.",
    )

    assert "Цвет: серый" in result.characteristics
    assert "Форма коврика: прямоугольный" in result.characteristics
    assert "Размер коврика: 50x80 см" in result.characteristics
    assert "Длина упаковки:" not in result.characteristics
    assert "Ширина упаковки:" not in result.characteristics
    assert "Высота упаковки:" not in result.characteristics
    assert "Вес с упаковкой" not in result.characteristics


def test_apply_wb_generation_quality_drops_generic_size_when_specific_rug_size_exists():
    card = CardGeneration(
        title="Коврик для ванной серый противоскользящий 50x80",
        description="Коврик для ванной комнаты с мягким ворсом.",
        keywords="",
        characteristics=(
            "Цвет: серый\n"
            "Размер коврика: 50x80 см\n"
            "Размер: 50 см\n"
            "Страна производства: Китай"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={
            "category": "Дом / Ванная / Коврики",
            "prompt_characteristics": ["Цвет", "Размер коврика"],
        },
        user_input="Коврик для ванной серый. Размер 50 на 80 см.",
    )

    assert "Размер коврика: 50x80 см" in result.characteristics
    assert "Размер: 50 см" not in result.characteristics


def test_apply_wb_generation_quality_drops_non_profile_freeform_backpack_fields():
    card = CardGeneration(
        title="Рюкзак городской мужской черный 22л 45x30x15 см",
        description="Рюкзак для города, учебы и поездок.",
        keywords="",
        characteristics=(
            "Цвет: черный\n"
            "Материал: полиэстер\n"
            "Объем (л): 22\n"
            "Размер: 45x30x15 см\n"
            "Тип застежки: молния\n"
            "Страна производства: Китай\n"
            "Комплектация: рюкзак; USB-кабель\n"
            "Количество внешних карманов: 3\n"
            "Карман для бутылки: Да\n"
            "Мягкая спинка: Да\n"
            "Водоотталкивающая пропитка: Да\n"
            "Назначение: городские, поездки, учеба, работа"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile=None,
        user_input=(
            "Рюкзак городской мужской черный. Объем 22 литра, размер 45x30x15 см. "
            "Материал полиэстер с водоотталкивающей пропиткой. Застежка молния. "
            "Комплектация: рюкзак, съемный USB-кабель. Страна производства Китай."
        ),
    )

    assert "Цвет: черный" in result.characteristics
    assert "Материал: полиэстер" in result.characteristics
    assert "Объем (л): 22" in result.characteristics
    assert "Размер: 45x30x15 см" in result.characteristics
    assert "Тип застежки: молния" in result.characteristics
    assert "Комплектация: рюкзак; USB-кабель" in result.characteristics
    assert "Назначение:" in result.characteristics
    assert "Мягкая спинка:" not in result.characteristics
    assert "Карман для бутылки:" not in result.characteristics
    assert "Водоотталкивающая пропитка:" not in result.characteristics


def test_apply_wb_generation_quality_infers_pet_food_fields_from_input():
    card = CardGeneration(
        title="Сухой корм для кошек с курицей 1 кг",
        description="Сухой корм для взрослых кошек.",
        keywords="",
        characteristics="Назначение: Для взрослых кошек",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile=None,
        user_input="Сухой корм для кошек с курицей. Для взрослых кошек, упаковка 1 кг.",
    )

    assert "Назначение: Для взрослых кошек" in result.characteristics
    assert "Тип: сухой корм" in result.characteristics
    assert "Вид животного: кошки" in result.characteristics
    assert "Вес: 1 кг" in result.characteristics
    assert "Вкус: курица" in result.characteristics


def test_apply_wb_generation_quality_drops_rug_fields_from_generic_home_profile():
    card = CardGeneration(
        title="Органайзер складной бежевый 40x30x25 см спанбонд",
        description="Органайзер для хранения вещей.",
        keywords="",
        characteristics=(
            "Цвет: бежевый\n"
            "Материал изделия: спанбонд\n"
            "Размер: 40x30x25 см\n"
            "Форма коврика: прямоугольная\n"
            "Основа коврика: жесткие стенки\n"
            "Особенности коврика: прозрачное окно, ручки по бокам\n"
            "Страна производства: Китай"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={
            "category": "Дом",
            "prompt_characteristics": [
                "Страна производства",
                "Комплектация",
                "Материал изделия",
                "Цвет",
                "Форма коврика",
                "Основа коврика",
                "Особенности коврика",
                "Размер коврика",
            ],
        },
        user_input=(
            "Органайзер для хранения вещей складной бежевый. Размер 40x30x25 см, "
            "материал спанбонд, жесткие стенки, прозрачное окно, ручки по бокам."
        ),
    )

    assert "Цвет: бежевый" in result.characteristics
    assert "Материал изделия: спанбонд" in result.characteristics
    assert "Размер: 40x30x25 см" in result.characteristics
    assert "Форма коврика:" not in result.characteristics
    assert "Основа коврика:" not in result.characteristics
    assert "Особенности коврика:" not in result.characteristics


def test_apply_wb_generation_quality_keeps_explicit_weight_from_input():
    card = CardGeneration(
        title="Сухой корм для кошек с курицей 1 кг",
        description="Сухой корм для взрослых кошек.",
        keywords="",
        characteristics=(
            "Тип: сухой корм\n"
            "Вид животного: кошки\n"
            "Вес: 1 кг\n"
            "Вкус: курица\n"
            "Страна производства: Китай"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Товары для животных"},
        user_input="Сухой корм для кошек с курицей. Для взрослых кошек, упаковка 1 кг.",
    )

    assert "Вес: 1 кг" in result.characteristics


def test_apply_wb_generation_quality_drops_neckline_from_pants():
    card = CardGeneration(
        title="Брюки женские черные прямые",
        description="Женские брюки прямого кроя для повседневных образов.",
        keywords="",
        characteristics=(
            "Цвет: черный\n"
            "Пол: женский\n"
            "Покрой: прямой\n"
            "Вырез горловины: круглый\n"
            "Страна производства: Китай"
        ),
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={
            "category": "Женщинам / Одежда / Брюки",
            "prompt_characteristics": ["Цвет", "Пол", "Покрой", "Вырез горловины", "Страна производства"],
        },
        user_input="Брюки женские черные прямого кроя",
    )

    assert "Цвет: черный" in result.characteristics
    assert "Пол: женский" in result.characteristics
    assert "Вырез горловины:" not in result.characteristics


def test_apply_wb_generation_quality_uses_outerwear_composition_default():
    card = CardGeneration(
        title="Куртка мужская черная демисезонная",
        description="Куртка для повседневной носки.",
        keywords="",
        characteristics="Цвет: черный\nСтрана производства: Китай",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Мужчинам / Одежда / Куртки"},
        user_input="Куртка мужская черная демисезонная",
    )

    assert "Состав: полиэстер 100%" in result.characteristics
    assert "Состав: хлопок 95%, эластан 5%" not in result.characteristics


def test_apply_wb_generation_quality_infers_shoe_fields_from_input():
    card = CardGeneration(
        title="Кроссовки мужские черные демисезонные",
        description="Кроссовки для повседневной носки.",
        keywords="",
        characteristics="Страна производства: Китай",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Обувь / Кроссовки"},
        user_input="Кроссовки мужские черные демисезонные на шнуровке",
    )

    assert "Пол: мужской" in result.characteristics
    assert "Цвет: черный" in result.characteristics
    assert "Сезон: демисезон" in result.characteristics
    assert "Вид застежки: шнуровка" in result.characteristics


def test_apply_wb_generation_quality_infers_beauty_volume_and_type():
    card = CardGeneration(
        title="Сыворотка для лица гиалуроновая 30 мл",
        description="Сыворотка для ухода за кожей лица.",
        keywords="",
        characteristics="Страна производства: Китай",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Красота / Уход за лицом"},
        user_input="Сыворотка для лица гиалуроновая 30 мл увлажняющая",
    )

    assert "Тип: сыворотка" in result.characteristics
    assert "Объем: 30 мл" in result.characteristics
    assert "Назначение: увлажнение" in result.characteristics


def test_apply_wb_generation_quality_infers_lamp_grounded_fields_from_input():
    card = CardGeneration(
        title="Настольная лампа LED белая USB",
        description="Лампа для рабочего стола.",
        keywords="",
        characteristics="Страна производства: Китай",
        marketplace="wb",
    )

    result = apply_wb_generation_quality(
        card,
        category_profile={"category": "Дом / Освещение"},
        user_input="Настольная лампа LED белая USB мощность 5W высота 35 см",
    )

    assert "Цвет: белый" in result.characteristics
    assert "Тип лампы: LED" in result.characteristics
    assert "Мощность: 5 Вт" in result.characteristics
    assert "Подключение: USB" in result.characteristics
    assert "Высота: 35 см" in result.characteristics
