import pytest

from llm import (
    CardGeneration,
    ImageConcept,
    LLMResponseError,
    build_user_prompt,
    build_image_director_user_prompt,
    parse_image_concepts_payload,
    parse_generation_payload,
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


def test_parse_generation_payload_rejects_missing_required_field():
    with pytest.raises(LLMResponseError, match="keywords"):
        parse_generation_payload(
            '{"title":"Название","description":"Описание","characteristics":"Материал: хлопок"}'
        )


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


def test_parse_generation_payload_accepts_ozon_hashtags_field():
    result = parse_generation_payload(
        '{"title":"Title","description":"Description","hashtags":"#tag #other","characteristics":"A: B"}',
        marketplace="ozon",
    )

    assert result.marketplace == "ozon"
    assert result.keywords == "#tag #other"


def test_select_system_prompt_uses_marketplace_specific_rules():
    wb_prompt = select_system_prompt("wb")
    ozon_prompt = select_system_prompt("ozon")

    assert "Wildberries" in wb_prompt
    assert "не указывай пол и цвет" in wb_prompt
    assert "Ozon" in ozon_prompt
    assert "hashtags" in ozon_prompt
    assert "600-900" in ozon_prompt


def test_build_user_prompt_includes_marketplace_name():
    assert build_user_prompt("wb", "товар").startswith("Маркетплейс: Wildberries")
    assert build_user_prompt("ozon", "товар").startswith("Маркетплейс: Ozon")


def test_parse_image_concepts_payload_validates_and_clamps_photo_index():
    result = parse_image_concepts_payload(
        (
            '{"concepts":['
            '{"image_index":1,"purpose":"main","photo_index":0,"prompt":"Prompt one"},'
            '{"image_index":2,"purpose":"details","photo_index":99,"prompt":"Prompt two"}'
            ']}'
        ),
        photos_count=2,
        images_count=2,
    )

    assert result == [
        ImageConcept(image_index=1, purpose="main", photo_index=0, prompt="Prompt one"),
        ImageConcept(image_index=2, purpose="details", photo_index=1, prompt="Prompt two"),
    ]


def test_parse_image_concepts_payload_rejects_missing_concepts():
    with pytest.raises(LLMResponseError, match="concepts"):
        parse_image_concepts_payload("{}", photos_count=1, images_count=1)


def test_build_image_director_user_prompt_includes_counts_and_marketplace():
    prompt = build_image_director_user_prompt(
        product_description="коврик EVA",
        marketplace="wb",
        photos_count=3,
        images_count=5,
    )

    assert "Маркетплейс: Wildberries" in prompt
    assert "Загружено фото: 3" in prompt
    assert "Нужно сгенерировать изображений: 5" in prompt
