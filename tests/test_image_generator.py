import asyncio
import base64
from io import BytesIO

import pytest
from PIL import Image

import image_generator
from image_generator import (
    ImageGenerationError,
    build_reference_photo_collage,
    extract_openrouter_image_usage,
)


def _png_bytes(color: str, size: tuple[int, int] = (64, 48)) -> bytes:
    image = Image.new("RGB", size, color)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


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


def test_build_reference_photo_collage_combines_input_angles_into_one_image():
    collage_bytes = build_reference_photo_collage(
        [
            _png_bytes("red", size=(80, 40)),
            _png_bytes("green", size=(40, 80)),
            _png_bytes("blue", size=(60, 60)),
        ],
        canvas_size=(512, 512),
    )

    collage = Image.open(BytesIO(collage_bytes))

    assert collage.size == (512, 512)
    assert collage.mode == "RGB"


def test_build_reference_photo_collage_packs_five_images_as_two_plus_three_rows():
    collage_bytes = build_reference_photo_collage(
        [
            _png_bytes("red"),
            _png_bytes("green"),
            _png_bytes("blue"),
            _png_bytes("yellow"),
            _png_bytes("purple"),
        ],
        canvas_size=(512, 512),
    )

    collage = Image.open(BytesIO(collage_bytes)).convert("RGB")

    assert collage.getpixel((80, 380)) != (246, 246, 244)
    assert collage.getpixel((256, 380)) != (246, 246, 244)
    assert collage.getpixel((430, 380)) != (246, 246, 244)


def test_generate_batch_images_sends_collage_once_per_concept(monkeypatch):
    captured = {"payloads": []}

    class FakeResponse:
        def __init__(self, image_bytes, cost):
            self.image_bytes = image_bytes
            self.cost = cost

        def raise_for_status(self):
            return None

        def json(self):
            return {
                "model": "model-version",
                "usage": {"cost": self.cost},
                "choices": [
                    {
                        "message": {
                            "images": [
                                {
                                    "image_url": {
                                        "url": "data:image/png;base64,"
                                        + base64.b64encode(self.image_bytes).decode("ascii")
                                    }
                                },
                            ]
                        }
                    }
                ],
            }

    class FakeClient:
        def __init__(self, timeout):
            captured["timeout"] = timeout

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def post(self, url, headers, json):
            captured["payloads"].append(json)
            response_index = len(captured["payloads"])
            return FakeResponse(f"image-{response_index}".encode("ascii"), 0.2)

    monkeypatch.setattr(image_generator.httpx, "AsyncClient", FakeClient)

    concepts = [
        image_generator.ImageBatchConcept(
            image_index=1,
            purpose="marketplace",
            prompt="black hourglass white sand wooden base",
        ),
        image_generator.ImageBatchConcept(
            image_index=2,
            purpose="marketplace",
            prompt="black hourglass white sand wooden base",
        ),
    ]

    result = asyncio.run(
        image_generator.generate_batch_image_results(
            concepts=concepts,
            reference_photo_bytes=[
                _png_bytes("red"),
                _png_bytes("green"),
                _png_bytes("blue"),
            ],
            api_key="key",
            model="model",
        )
    )

    assert len(captured["payloads"]) == 2
    for payload in captured["payloads"]:
        content = payload["messages"][0]["content"]
        image_items = [item for item in content if item["type"] == "image_url"]
        assert len(image_items) == 1
        assert content[1]["text"] == "Input reference collage"
        assert payload["image_config"]["aspect_ratio"] == "3:4"

    prompt_texts = [payload["messages"][0]["content"][-1]["text"] for payload in captured["payloads"]]
    assert all("black hourglass white sand wooden base" in text for text in prompt_texts)
    assert all("collage" in text for text in prompt_texts)
    assert all("one image" in text for text in prompt_texts)
    assert all("Reference:" in text for text in prompt_texts)
    assert all("Product facts:" in text for text in prompt_texts)
    assert all("Shot goal:" in text for text in prompt_texts)
    assert all("Preserve:" in text for text in prompt_texts)
    assert all("Avoid:" in text for text in prompt_texts)
    assert all("Image 1 of 2" not in text for text in prompt_texts)
    assert captured["timeout"] >= 420
    assert [item.image_bytes for item in result] == [b"image-1", b"image-2"]
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
                                        + base64.b64encode(b"extra").decode("ascii")
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
            return FakeResponse()

    monkeypatch.setattr(image_generator.httpx, "AsyncClient", FakeClient)

    result = asyncio.run(
        image_generator.generate_batch_image_results(
            concepts=[image_generator.ImageBatchConcept(1, "hero", "Hero prompt")],
            reference_photo_bytes=[_png_bytes("red")],
            api_key="key",
            model="model",
        )
    )

    assert [item.image_bytes for item in result] == [b"one"]
    assert [item.usage.cost_usd for item in result] == [0.6]


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
                reference_photo_bytes=[_png_bytes("red")],
                api_key="key",
                model="model",
            )
        )
