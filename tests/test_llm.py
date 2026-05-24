import sys
import pytest
from types import SimpleNamespace

from llm import (
    CardGeneration,
    ImageConcept,
    LLMResponseError,
    build_openrouter_model_fallbacks,
    build_category_profile_prompt_block,
    build_user_prompt,
    generate_image_prompts,
    parse_generation_payload,
    request_chat_completion_with_fallback,
    select_system_prompt,
)


def test_parse_generation_payload_accepts_valid_json():
    result = parse_generation_payload(
        '{"title":"Название","description":"Описание","keywords":"ключ 1, ключ 2","characteristics":"Материал: хлопок"}'
    )

    assert result == CardGeneration(
        title="Название",
        description="Описание",
        keywords="ключ 1, ключ 2",
        characteristics="Материал: хлопок",
        tokens_used=0,
    )


def test_build_openrouter_model_fallbacks_keeps_normalized_model_single():
    assert build_openrouter_model_fallbacks("deepseek/deepseek-v4-flash") == [
        "deepseek/deepseek-v4-flash",
    ]


def test_build_openrouter_model_fallbacks_tolerates_legacy_free_model():
    assert build_openrouter_model_fallbacks("deepseek/deepseek-v4-flash:free") == [
        "deepseek/deepseek-v4-flash:free",
        "deepseek/deepseek-v4-flash",
    ]


def _chat_response(content: str | None):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage=SimpleNamespace(total_tokens=123),
    )


class _FakeCompletions:
    def __init__(self, results):
        self.results = list(results)
        self.calls: list[str] = []

    async def create(self, **kwargs):
        self.calls.append(kwargs["model"])
        self.last_kwargs = kwargs
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result


class _FakeChat:
    def __init__(self, results):
        self.completions = _FakeCompletions(results)


class _FakeClient:
    def __init__(self, results):
        self.chat = _FakeChat(results)


class _RateLimitError(Exception):
    status_code = 429


@pytest.mark.asyncio
async def test_request_chat_completion_retries_empty_response_on_same_model():
    client = _FakeClient(
        [
            _chat_response(None),
            _chat_response('{"title":"ok"}'),
        ]
    )

    response = await request_chat_completion_with_fallback(
        client,
        model_candidates=["deepseek/deepseek-v4-flash"],
        messages=[],
        max_tokens=100,
        temperature=0.7,
    )

    assert response.choices[0].message.content == '{"title":"ok"}'
    assert client.chat.completions.calls == [
        "deepseek/deepseek-v4-flash",
        "deepseek/deepseek-v4-flash",
    ]
    assert client.chat.completions.last_kwargs["extra_body"] == {
        "reasoning": {"effort": "none", "exclude": True},
        "include_reasoning": False,
    }


@pytest.mark.asyncio
async def test_request_chat_completion_uses_paid_fallback_after_rate_limit():
    client = _FakeClient(
        [
            _RateLimitError(),
            _chat_response('{"title":"ok"}'),
        ]
    )

    response = await request_chat_completion_with_fallback(
        client,
        model_candidates=["deepseek/deepseek-v4-flash:free", "deepseek/deepseek-v4-flash"],
        messages=[],
        max_tokens=100,
        temperature=0.7,
    )

    assert response.choices[0].message.content == '{"title":"ok"}'
    assert client.chat.completions.calls == [
        "deepseek/deepseek-v4-flash:free",
        "deepseek/deepseek-v4-flash",
    ]


@pytest.mark.asyncio
async def test_request_chat_completion_raises_after_repeated_empty_response():
    client = _FakeClient([_chat_response(""), _chat_response(None)])

    with pytest.raises(LLMResponseError, match="empty response"):
        await request_chat_completion_with_fallback(
            client,
            model_candidates=["deepseek/deepseek-v4-flash"],
            messages=[],
            max_tokens=100,
            temperature=0.7,
        )


def test_parse_generation_payload_rejects_missing_ozon_hashtags():
    with pytest.raises(LLMResponseError, match="hashtags"):
        parse_generation_payload(
            '{"title":"Title","description":"Description","characteristics":"Material: cotton"}',
            marketplace="ozon",
        )


def test_parse_generation_payload_allows_wb_without_keywords():
    result = parse_generation_payload(
        '{"title":"Title","description":"Description","characteristics":"Material: cotton"}',
        marketplace="wb",
    )

    assert result.keywords == ""


def test_parse_generation_payload_removes_characteristics_service_tail():
    payload = (
        '{"title":"Title","description":"Description","keywords":"kw1, kw2",'
        '"characteristics":"'
        '\\u0412\\u0438\\u0434 \\u0442\\u043e\\u0432\\u0430\\u0440\\u0430: '
        '\\u0420\\u0430\\u0448\\u0433\\u0430\\u0440\\u0434\\n'
        '\\u0411\\u0440\\u0435\\u043d\\u0434: Berserk\\n'
        '\\u0426\\u0432\\u0435\\u0442: '
        '\\u0427\\u0435\\u0440\\u043d\\u043e-\\u0431\\u0435\\u043b\\u044b\\u0439\\n'
        '\\u041e\\u0441\\u043e\\u0431\\u0435\\u043d\\u043d\\u043e\\u0441\\u0442\\u0438: '
        '\\u041a\\u043e\\u043c\\u043f\\u0440\\u0435\\u0441\\u0441\\u0438\\u043e\\u043d\\u043d\\u044b\\u0439'
        '\\u5168\\u56fd;\\u0442\\u043e\\u0432 >- depth:1 summary:bad tfo=.00. \\\\r\\\\n"}'
    )

    result = parse_generation_payload(payload)

    assert result.characteristics == (
        "\u0412\u0438\u0434 \u0442\u043e\u0432\u0430\u0440\u0430: "
        "\u0420\u0430\u0448\u0433\u0430\u0440\u0434\n"
        "\u0411\u0440\u0435\u043d\u0434: Berserk\n"
        "\u0426\u0432\u0435\u0442: "
        "\u0427\u0435\u0440\u043d\u043e-\u0431\u0435\u043b\u044b\u0439"
    )


def test_parse_generation_payload_filters_characteristics_lines_without_colon():
    payload = (
        '{"title":"Title","description":"Description","keywords":"kw1, kw2",'
        '"characteristics":"Material: cotton\\nloose text\\nSize: XL"}'
    )

    result = parse_generation_payload(payload)

    assert result.characteristics == "Material: cotton\nSize: XL"


def test_parse_generation_payload_removes_unknown_characteristic_placeholders():
    result = parse_generation_payload(
        '{"title":"Title","description":"Description","keywords":"kw",'
        '"characteristics":"Color: white\\nSurface: [укажите поверхность]\\nCountry: Китай"}',
        marketplace="wb",
    )

    assert result.characteristics == "Color: white\nCountry: Китай"


def test_parse_generation_payload_accepts_ozon_hashtags_field():
    result = parse_generation_payload(
        '{"title":"Title","description":"Description","hashtags":"#tag #other","characteristics":"A: B"}',
        marketplace="ozon",
    )

    assert result.marketplace == "ozon"
    assert result.keywords == "#tag #other"


def test_parse_generation_payload_applies_ozon_marketplace_rules():
    long_title = "Супер товар ™ акция скидка " + "оченьдлинноесловодлиннеедвадцатисемисимволов " * 8
    payload = (
        '{"title":'
        + repr(long_title).replace("'", '"')
        + ',"description":"Купить сейчас, скидка 30%. Подробнее https://example.com и @seller",'
        + '"hashtags":"декор, #декор_для_дома #декор_для_дома #оченьдлинныйхэштегкоторыйточнодлиннеетридцати",'
        + '"characteristics":"A: B"}'
    )

    result = parse_generation_payload(payload, marketplace="ozon")

    assert len(result.title) <= 200
    assert all(len(word) <= 27 for word in result.title.split())
    assert "™" not in result.title
    assert "акция" not in result.title.lower()
    assert "скидка" not in result.description.lower()
    assert "https://" not in result.description
    assert "@seller" not in result.description
    assert result.keywords == "#декор #декор_для_дома"


def test_parse_generation_payload_applies_wb_title_limit():
    result = parse_generation_payload(
        '{"title":"Очень длинное название товара с цветом и размером для проверки ограничения Wildberries",'
        '"description":"Описание","keywords":"ключ 1, ключ 2","characteristics":"A: B"}',
        marketplace="wb",
    )

    assert len(result.title) <= 60


def test_select_system_prompt_uses_marketplace_specific_rules():
    wb_prompt = select_system_prompt("wb")
    ozon_prompt = select_system_prompt("ozon")

    assert "Wildberries" in wb_prompt
    assert "Пол и цвет можно указывать" in wb_prompt
    assert "Ozon" in ozon_prompt
    assert "hashtags" in ozon_prompt
    assert "200 символов" in ozon_prompt
    assert "900-1400 символов" in ozon_prompt
    assert "30 хештегов" in ozon_prompt



def test_wb_prompt_keeps_clothing_size_and_composition_out_of_title():
    prompt = select_system_prompt("wb")

    assert "Для одежды не выноси размер в название" in prompt
    assert "Для одежды не выноси состав в название" in prompt


def test_ozon_prompt_keeps_clothing_size_and_composition_out_of_title():
    prompt = select_system_prompt(
        "ozon",
        {
            "category": "Одежда / Мужская одежда / Рашгарды",
            "title_target_min": 40,
            "title_target_max": 70,
            "description_target_min": 900,
            "description_target_max": 1400,
            "prompt_characteristics": ["Тип", "Цвет", "Размер", "Состав"],
        },
    )

    assert "Для одежды не выноси размер в название" in prompt
    assert "Для одежды не выноси состав в название" in prompt
    assert "название должно быть содержательным" in prompt
    assert "тип товара + бренд/надпись/модель" in prompt
    assert "с воротником-стойкой" in prompt
    assert "с принтом на спине" in prompt


def test_marketplace_prompts_require_selling_description_pattern():
    wb_prompt = select_system_prompt("wb")
    ozon_prompt = select_system_prompt("ozon")

    for prompt in (wb_prompt, ozon_prompt):
        lowered = prompt.lower()
        assert "Не начинай описание с клише" in prompt
        assert "переводи характеристику в выгоду" in lowered
        assert "не дублируй блок характеристик" in lowered
        assert "сценарии применения" in lowered


def test_marketplace_prompts_forbid_duplicate_fact_rephrasing():
    wb_prompt = select_system_prompt("wb")
    ozon_prompt = select_system_prompt("ozon")

    for prompt in (wb_prompt, ozon_prompt):
        assert "Не повторяй один и тот же факт" in prompt
        assert "Если факт уже раскрыт в первом абзаце" in prompt


def test_wb_prompt_includes_category_profile():
    prompt = select_system_prompt(
        "wb",
        {
            "category": "Обувь",
            "title_formula": "тип обуви + пол + сезон",
            "title_target_min": 25,
            "title_target_max": 50,
            "description_target_min": 700,
            "description_target_max": 1200,
            "required_characteristics": ["Цвет", "Пол", "Сезон"],
            "recommended_characteristics": ["Материал стельки"],
            "prompt_characteristics": ["Цвет", "Пол", "Сезон", "Материал стельки"],
            "characteristics_target_min": 8,
            "characteristics_target_max": 16,
        },
    )

    assert "Категорийный профиль WB" in prompt
    assert "Категория товара: Обувь" in prompt
    assert "Разрешенные характеристики для генерации: Цвет, Пол, Сезон, Материал стельки" in prompt
    assert "Материал стельки" in prompt


def test_ozon_prompt_includes_beauty_category_profile():
    prompt = select_system_prompt(
        "ozon",
        {
            "category": "Красота и здоровье",
            "title_target_chars": 87,
            "desc_target_chars": 1400,
            "top_characteristics": ["Тип", "Тип кожи", "Объем, мл"],
            "prompt_characteristics": ["Тип", "Тип кожи", "Объем, мл"],
            "top_hashtags": ["#крем", "#уход_за_кожей"],
            "top_title_words": ["крем", "кожи", "уход"],
        },
    )

    assert "Категория товара: Красота и здоровье" in prompt
    assert "Разрешенные характеристики для генерации: Тип, Тип кожи, Объем, мл" in prompt
    assert "Тип кожи" in prompt
    assert "#уход_за_кожей" in prompt


def test_ozon_prompt_includes_v2_category_profile_targets():
    prompt = select_system_prompt(
        "ozon",
        {
            "category": "Электроника / Наушники и аудиотехника / Наушники",
            "title_target_min": 40,
            "title_target_max": 70,
            "description_target_min": 900,
            "description_target_max": 1400,
            "characteristics_target_min": 6,
            "characteristics_target_max": 12,
            "prompt_characteristics": ["Тип", "Цвет", "Конструкция наушников", "Тип беспроводной связи"],
            "top_hashtags": ["#наушники", "#bluetooth"],
            "top_title_words": ["наушники", "беспроводные"],
        },
    )

    assert "Категорийный профиль Ozon" in prompt
    assert "Категория товара: Электроника / Наушники и аудиотехника / Наушники" in prompt
    assert "Длина названия: 40-70 символов" in prompt
    assert "Длина описания: 900-1400 символов" in prompt
    assert "Целевое количество характеристик: 6-12" in prompt
    assert "Конструкция наушников" in prompt
    assert "#bluetooth" in prompt


def test_ozon_prompt_includes_clothes_category_profile():
    block = build_category_profile_prompt_block(
        {
            "category": "Одежда",
            "title_target_chars": 92,
            "desc_target_chars": 1400,
            "top_characteristics": ["Цвет", "Российский размер", "Материал"],
            "top_hashtags": ["#платье", "#одежда"],
            "top_title_words": ["платье", "женское"],
        }
    )

    assert "Категория товара: Одежда" in block
    assert "Цвет" in block


def test_parse_generation_payload_removes_forbidden_title_words():
    result = parse_generation_payload(
        (
            '{"title":"Крем для лица акция скидка original",'
            '"description":"Описание товара",'
            '"hashtags":"крем уход",'
            '"characteristics":"Тип: Крем"}'
        ),
        marketplace="ozon",
    )

    lowered = result.title.lower()
    assert "акция" not in lowered
    assert "скидка" not in lowered
    assert "original" not in lowered


def test_build_user_prompt_includes_marketplace_name():
    assert build_user_prompt("wb", "товар").startswith("Маркетплейс: Wildberries")
    assert build_user_prompt("ozon", "товар").startswith("Маркетплейс: Ozon")


def test_build_user_prompt_includes_resolved_fields_and_instructions():
    prompt = build_user_prompt(
        "ozon",
        "крем для лица",
        {
            "Страна-изготовитель": "Россия",
            "Цвет": "[укажите цвет]",
            "__prompt_instructions": ["Извлеки цвет из изображения товара."],
        },
    )

    assert "Страна-изготовитель: Россия" in prompt
    assert "Цвет: [укажите цвет]" in prompt
    assert "Извлеки цвет из изображения товара." in prompt


@pytest.mark.asyncio
async def test_generate_image_prompts_uses_clothing_template_sequence(monkeypatch):
    async def fail_request_chat_completion_with_fallback(client, **kwargs):
        raise AssertionError("image prompts must not call a secondary LLM")

    monkeypatch.setattr(
        "llm.request_chat_completion_with_fallback",
        fail_request_chat_completion_with_fallback,
    )

    result = await generate_image_prompts(
        product_description="Рашгард Therapy черный, прилегающий крой, принт на спине",
        marketplace="ozon",
        photos_count=2,
        images_count=5,
        api_key="test-key",
        model="deepseek/deepseek-v4-flash:free",
        site_url="https://alterega.ru",
        image_guidance="дорогой светлый фон",
        category_profile={"category": "Одежда / Мужская одежда / Рашгарды"},
    )

    assert [concept.purpose for concept in result.concepts] == [
        "инфографика преимуществ",
        "детали товара",
        "на модели спереди",
        "на модели сзади",
        "главная карточка",
    ]
    assert "вид спереди" in result.concepts[2].prompt.casefold()
    assert "вид сзади" in result.concepts[3].prompt.casefold()
    assert "Желательно добавить один небольшой аккуратный блок инфографики" in result.concepts[1].prompt
    assert "Одежда / Мужская одежда / Рашгарды" in result.concepts[0].prompt
    assert all("Рашгард Therapy" in concept.prompt for concept in result.concepts)
    assert all("дорогой светлый фон" in concept.prompt for concept in result.concepts)
    assert all("не добавляй неподтвержденные" in concept.prompt.casefold() for concept in result.concepts)
    assert result.source == "direct"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("images_count", "expected_purposes"),
    [
        (1, ["инфографика преимуществ"]),
        (3, ["инфографика преимуществ", "детали товара", "на модели"]),
        (
            7,
            [
                "главная карточка",
                "инфографика преимуществ",
                "на модели спереди",
                "на модели сзади",
                "детали товара",
                "размеры и посадка",
                "сценарий использования",
            ],
        ),
    ],
)
async def test_generate_image_prompts_selects_clothing_roles_by_requested_count(
    images_count,
    expected_purposes,
):
    result = await generate_image_prompts(
        product_description="Рашгард Therapy черный, прилегающий крой, принт на спине",
        marketplace="ozon",
        photos_count=2,
        images_count=images_count,
        api_key="test-key",
        model="deepseek/deepseek-v4-flash:free",
        site_url="https://alterega.ru",
        category_profile={"category": "Одежда / Мужская одежда / Рашгарды"},
    )

    assert [concept.purpose for concept in result.concepts] == expected_purposes
    if images_count == 3:
        assert "вид спереди" not in result.concepts[2].prompt.casefold()
        assert "вид сзади" not in result.concepts[2].prompt.casefold()


@pytest.mark.asyncio
async def test_generate_image_prompts_routes_rashguard_text_to_clothing_when_profile_missing():
    result = await generate_image_prompts(
        product_description="Рашгард therapy черный размер M, 100% хлопок, тянущийся облегающий с горловиной",
        marketplace="wb",
        photos_count=5,
        images_count=3,
        api_key="test-key",
        model="deepseek/deepseek-v4-flash:free",
        site_url="https://alterega.ru",
        category_profile=None,
    )

    assert [concept.purpose for concept in result.concepts] == [
        "инфографика преимуществ",
        "детали товара",
        "на модели",
    ]
    assert "Категория товара: Одежда" in result.concepts[0].prompt


@pytest.mark.asyncio
async def test_generate_image_prompts_overrides_wrong_non_clothing_profile_for_rashguard():
    result = await generate_image_prompts(
        product_description="Рашгард therapy черный размер M, 100% хлопок, принт Therapy на спине",
        marketplace="wb",
        photos_count=5,
        images_count=3,
        api_key="test-key",
        model="deepseek/deepseek-v4-flash:free",
        site_url="https://alterega.ru",
        category_profile={"category": "Дом"},
    )

    assert [concept.purpose for concept in result.concepts] == [
        "инфографика преимуществ",
        "детали товара",
        "на модели",
    ]
    assert "Категория товара: Дом" not in result.concepts[0].prompt
    assert "Категория товара: Одежда" in result.concepts[0].prompt


@pytest.mark.asyncio
async def test_generate_image_prompts_uses_universal_full_template_sequence(monkeypatch):
    async def fake_request_chat_completion_with_fallback(client, **kwargs):
        raise RuntimeError("secondary LLM unavailable")

    monkeypatch.setattr(
        "llm.request_chat_completion_with_fallback",
        fake_request_chat_completion_with_fallback,
    )

    result = await generate_image_prompts(
        product_description="Часы песочные, черное основание, белый песок, цикл 5 минут",
        marketplace="ozon",
        photos_count=4,
        images_count=7,
        api_key="test-key",
        model="deepseek/deepseek-v4-flash:free",
        site_url="https://alterega.ru",
        image_guidance="премиальная современная подача",
        category_profile={"category": "Дом и интерьер / Декор / Песочные часы"},
    )

    assert result.source == "direct"
    assert [concept.purpose for concept in result.concepts] == [
        "главная карточка",
        "инфографика преимуществ",
        "детали товара",
        "товар в применении",
        "характеристики и параметры",
        "комплектация",
        "ключевая особенность",
    ]
    assert [concept.photo_index for concept in result.concepts] == [0] * 7
    assert "КРУПНЫЙ ПЛАН" in result.concepts[2].prompt
    assert "КОМПЛЕКТАЦИЯ" in result.concepts[5].prompt
    assert "премиальная современная подача" in result.concepts[0].prompt


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("images_count", "expected_purposes"),
    [
        (1, ["инфографика преимуществ"]),
        (3, ["инфографика преимуществ", "детали товара", "товар в применении"]),
        (
            5,
            [
                "инфографика преимуществ",
                "детали товара",
                "товар в применении",
                "характеристики и параметры",
                "главная карточка",
            ],
        ),
    ],
)
async def test_generate_image_prompts_selects_universal_roles_by_requested_count(
    images_count,
    expected_purposes,
):
    result = await generate_image_prompts(
        product_description="Часы песочные, черное основание, белый песок, цикл 5 минут",
        marketplace="ozon",
        photos_count=4,
        images_count=images_count,
        api_key="test-key",
        model="deepseek/deepseek-v4-flash:free",
        site_url="https://alterega.ru",
        category_profile={"category": "Дом и интерьер / Декор / Песочные часы"},
    )

    assert [concept.purpose for concept in result.concepts] == expected_purposes
    if images_count >= 3:
        assert "Желательно добавить один небольшой аккуратный блок инфографики" in result.concepts[1].prompt


@pytest.mark.asyncio
async def test_generate_image_prompts_rejects_more_than_seven_images():
    with pytest.raises(LLMResponseError, match="images_count must be between 1 and 7"):
        await generate_image_prompts(
            product_description="hourglass",
            marketplace="ozon",
            photos_count=1,
            images_count=8,
            api_key="test-key",
        )
