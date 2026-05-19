import pytest

from llm import CardGeneration, LLMResponseError, parse_generation_payload


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
