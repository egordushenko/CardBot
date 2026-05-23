import base64
import asyncio

import pytest

import image_generator
from image_generator import (
    GeneratedImage,
    ImageGenerationError,
    ImageGenerationUsage,
    PRODUCT_PRESERVATION_SUFFIX,
    build_safe_image_prompt,
    extract_openrouter_image_bytes,
    extract_openrouter_image_usage,
)
from visual_pipeline import ImageQualityReport


def test_extract_openrouter_image_bytes_reads_data_url():
    expected = b"png-bytes"
    payload = {
        "choices": [
            {
                "message": {
                    "images": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/png;base64,"
                                + base64.b64encode(expected).decode("ascii")
                            },
                        }
                    ]
                }
            }
        ]
    }

    assert extract_openrouter_image_bytes(payload) == expected


def test_extract_openrouter_image_bytes_reads_legacy_data_shape():
    expected = b"png-bytes"
    payload = {
        "data": [
            {
                "url": "data:image/png;base64,"
                + base64.b64encode(expected).decode("ascii")
            }
        ]
    }

    assert extract_openrouter_image_bytes(payload) == expected


def test_extract_openrouter_image_bytes_rejects_missing_images():
    with pytest.raises(ImageGenerationError, match="images"):
        extract_openrouter_image_bytes({"choices": [{"message": {}}]})


def test_extract_openrouter_image_usage_reads_model_and_cost():
    payload = {
        "model": "openai/gpt-5.4-image-2-20260421",
        "usage": 0.200231,
    }

    usage = extract_openrouter_image_usage(payload, fallback_model="fallback")

    assert usage.model == "openai/gpt-5.4-image-2-20260421"
    assert usage.cost_usd == 0.200231


def test_build_safe_image_prompt_appends_product_preservation_rules():
    prompt = build_safe_image_prompt("Show product on white background")

    assert prompt.startswith("Show product on white background")
    assert PRODUCT_PRESERVATION_SUFFIX in prompt
    assert "Do NOT add any buttons" in prompt
    assert "Preserve exact product geometry" in prompt
    assert "Do NOT squash, stretch, compress or elongate the product" in prompt
    assert "Preserve original product color and material texture" in prompt


def test_generate_single_image_sends_safe_prompt_to_api(monkeypatch):
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "choices": [
                    {
                        "message": {
                            "images": [
                                {
                                    "image_url": {
                                        "url": "data:image/png;base64,"
                                        + base64.b64encode(b"png").decode("ascii")
                                    }
                                }
                            ]
                        }
                    }
                ]
            }

    class FakeClient:
        def __init__(self, timeout):
            self.timeout = timeout

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def post(self, url, headers, json):
            captured["payload"] = json
            return FakeResponse()

    monkeypatch.setattr(image_generator.httpx, "AsyncClient", FakeClient)

    result = asyncio.run(
        image_generator.generate_single_image(
            prompt="Original prompt",
            reference_photo_bytes=b"photo",
            api_key="key",
            model="model",
        )
    )

    sent_text = captured["payload"]["messages"][0]["content"][1]["text"]
    assert result == b"png"
    assert sent_text.startswith("Original prompt")
    assert PRODUCT_PRESERVATION_SUFFIX in sent_text


def test_generate_marketplace_image_result_blocks_failed_quality_check(monkeypatch):
    class FakeFile:
        async def download_as_bytearray(self):
            return bytearray(b"reference")

    class FakeBot:
        async def get_file(self, file_id):
            return FakeFile()

    async def fake_generate_single_image_result(**kwargs):
        return GeneratedImage(
            image_bytes=b"generated",
            usage=ImageGenerationUsage(model="image-model", cost_usd=0.2),
        )

    async def fake_evaluate_generated_image_quality(**kwargs):
        return ImageQualityReport(
            passed=False,
            issues=("print_mismatch",),
            summary="print changed",
        )

    monkeypatch.setattr(
        image_generator,
        "generate_single_image_result",
        fake_generate_single_image_result,
    )
    monkeypatch.setattr(
        image_generator,
        "evaluate_generated_image_quality",
        fake_evaluate_generated_image_quality,
    )

    with pytest.raises(ImageGenerationError, match="image QA failed: print_mismatch"):
        asyncio.run(
            image_generator.generate_marketplace_image_result(
                prompt="Prompt",
                reference_photo_file_id="file-id",
                bot=FakeBot(),
                api_key="key",
                model="image-model",
                quality_model="vision-model",
                quality_enabled=True,
            )
        )
