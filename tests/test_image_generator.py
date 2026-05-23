import base64
import asyncio

import pytest

import image_generator
from image_generator import (
    ImageGenerationError,
    extract_openrouter_image_bytes,
    extract_openrouter_image_usage,
)


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


def test_extract_openrouter_image_bytes_list_reads_all_message_images():
    first = b"first"
    second = b"second"
    payload = {
        "choices": [
            {
                "message": {
                    "images": [
                        {
                            "image_url": {
                                "url": "data:image/png;base64,"
                                + base64.b64encode(first).decode("ascii")
                            }
                        },
                        {
                            "image_url": {
                                "url": "data:image/png;base64,"
                                + base64.b64encode(second).decode("ascii")
                            }
                        },
                    ]
                }
            }
        ]
    }

    assert image_generator.extract_openrouter_image_bytes_list(payload) == [first, second]


def test_extract_openrouter_image_usage_reads_model_and_cost():
    payload = {
        "model": "openai/gpt-5.4-image-2-20260421",
        "usage": 0.200231,
    }

    usage = extract_openrouter_image_usage(payload, fallback_model="fallback")

    assert usage.model == "openai/gpt-5.4-image-2-20260421"
    assert usage.cost_usd == 0.200231


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
    assert sent_text == "Original prompt"
    assert "STRICT PRODUCT PRESERVATION RULES" not in sent_text


def test_generate_batch_images_sends_all_reference_photos_and_concepts(monkeypatch):
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "model": "model-version",
                "usage": {"cost": 0.4},
                "choices": [
                    {
                        "message": {
                            "images": [
                                {
                                    "image_url": {
                                        "url": "data:image/png;base64,"
                                        + base64.b64encode(b"one").decode("ascii")
                                    }
                                },
                                {
                                    "image_url": {
                                        "url": "data:image/png;base64,"
                                        + base64.b64encode(b"two").decode("ascii")
                                    }
                                },
                            ]
                        }
                    }
                ],
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

    concepts = [
        image_generator.ImageBatchConcept(
            image_index=1,
            purpose="hero",
            prompt="Hero prompt",
        ),
        image_generator.ImageBatchConcept(
            image_index=2,
            purpose="back",
            prompt="Back prompt",
        ),
    ]

    result = asyncio.run(
        image_generator.generate_batch_image_results(
            concepts=concepts,
            reference_photo_bytes=[b"photo-a", b"photo-b"],
            api_key="key",
            model="model",
        )
    )

    content = captured["payload"]["messages"][0]["content"]
    image_items = [item for item in content if item["type"] == "image_url"]
    prompt_text = content[-1]["text"]

    assert len(image_items) == 2
    assert "Generate exactly 2 separate marketplace-ready output images" in prompt_text
    assert "Image 1 (hero): Hero prompt" in prompt_text
    assert "Image 2 (back): Back prompt" in prompt_text
    assert [item.image_bytes for item in result] == [b"one", b"two"]
    assert [item.usage.model for item in result] == ["model-version", "model-version"]
    assert [item.usage.cost_usd for item in result] == [0.2, 0.2]


def test_generate_batch_images_rejects_wrong_output_count(monkeypatch):
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
                                        + base64.b64encode(b"one").decode("ascii")
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
            return FakeResponse()

    monkeypatch.setattr(image_generator.httpx, "AsyncClient", FakeClient)

    concepts = [
        image_generator.ImageBatchConcept(1, "hero", "Hero prompt"),
        image_generator.ImageBatchConcept(2, "back", "Back prompt"),
    ]

    with pytest.raises(ImageGenerationError, match="expected 2 images, got 1"):
        asyncio.run(
            image_generator.generate_batch_image_results(
                concepts=concepts,
                reference_photo_bytes=[b"photo"],
                api_key="key",
                model="model",
            )
        )


def test_generate_batch_images_rejects_corrupted_prompt_before_paid_request(monkeypatch):
    class FakeClient:
        def __init__(self, timeout):
            self.timeout = timeout

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def post(self, url, headers, json):
            raise AssertionError("request must not be sent")

    monkeypatch.setattr(image_generator.httpx, "AsyncClient", FakeClient)

    with pytest.raises(ImageGenerationError, match="question marks"):
        asyncio.run(
            image_generator.generate_batch_image_results(
                concepts=[
                    image_generator.ImageBatchConcept(
                        1,
                        "hero",
                        "?????????? 3 ????????? ???????????",
                    )
                ],
                reference_photo_bytes=[b"photo"],
                api_key="key",
                model="model",
            )
        )
