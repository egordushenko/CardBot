import base64

import pytest

from image_generator import ImageGenerationError, extract_openrouter_image_bytes


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
