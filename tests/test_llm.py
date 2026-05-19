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
