import base64
import asyncio

import pytest

import image_generator
from image_generator import (
    ImageGenerationError,
    extract_openrouter_image_usage,
)


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
            captured["timeout"] = timeout

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
            purpose="marketplace",
            prompt="black Therapy rashguard cotton fitted",
        ),
        image_generator.ImageBatchConcept(
            image_index=2,
            purpose="marketplace",
            prompt="black Therapy rashguard cotton fitted",
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
    assert "Сгенерируй 2 отдельных изображения данного товара." in prompt_text
    assert "black Therapy rashguard cotton fitted" in prompt_text
    assert "Установить соотношение сторон 3:4." in prompt_text
    assert "message.images" not in prompt_text
    assert "коллаж" not in prompt_text
    assert "сетк" not in prompt_text
    assert "Required outputs" not in prompt_text
    assert "Image 1" not in prompt_text
    assert captured["timeout"] >= 420
    assert [item.image_bytes for item in result] == [b"one", b"two"]
    assert [item.usage.model for item in result] == ["model-version", "model-version"]
    assert [item.usage.cost_usd for item in result] == [0.2, 0.2]


def test_generate_batch_images_uses_available_outputs_when_count_differs(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "model": "model-version",
                "usage": {"cost": 0.6},
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
                                {
                                    "image_url": {
                                        "url": "data:image/png;base64,"
                                        + base64.b64encode(b"extra").decode("ascii")
                                    }
                                },
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

    result = asyncio.run(
        image_generator.generate_batch_image_results(
            concepts=concepts,
            reference_photo_bytes=[b"photo"],
            api_key="key",
            model="model",
        )
    )

    assert [item.image_bytes for item in result] == [b"one", b"two"]
    assert [item.usage.cost_usd for item in result] == [0.3, 0.3]


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
