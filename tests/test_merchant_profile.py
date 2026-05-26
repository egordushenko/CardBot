from merchant_profile import (
    build_merchant_profile_image_guidance,
    build_merchant_profile_prompt_block,
    format_merchant_profile_message,
    merge_merchant_profile_image_guidance,
    normalize_profile_value,
)


def test_merchant_profile_prompt_block_includes_only_filled_fields():
    block = build_merchant_profile_prompt_block(
        {
            "visual_style_default": "clean premium",
            "text_tone": "friendly expert",
            "preferred_card_formats": "",
            "banned_words": "best, cheap",
            "typical_product_segment": None,
        }
    )

    assert "Профиль магазина пользователя" in block
    assert "clean premium" in block
    assert "friendly expert" in block
    assert "best, cheap" in block
    assert "Формат карточек" not in block
    assert "текущей генерации имеют приоритет" in block


def test_merge_merchant_profile_image_guidance_keeps_explicit_guidance_first():
    merged = merge_merchant_profile_image_guidance(
        "use a white background",
        {
            "visual_style_default": "dark premium",
            "preferred_card_formats": "hero plus detail frames",
            "banned_words": "sale",
        },
    )

    assert merged.startswith("use a white background")
    assert "Профиль магазина" in merged
    assert "dark premium" in merged
    assert merged.index("use a white background") < merged.index("dark premium")
    assert "strict grid layout" in merged
    assert "technical infographic" in merged
    assert "minimal decoration" in merged
    assert "one clear CTA" in merged


def test_image_guidance_is_empty_when_profile_has_no_values():
    assert build_merchant_profile_image_guidance({}) == ""
    assert merge_merchant_profile_image_guidance("", {}) == ""


def test_format_merchant_profile_message_marks_empty_and_filled_values():
    empty = format_merchant_profile_message(None)
    filled = format_merchant_profile_message({"visual_style_default": "clean premium"})

    assert "Профиль магазина" in empty
    assert "не заполнен" in empty.casefold()
    assert "clean premium" in filled


def test_normalize_profile_value_collapses_whitespace_and_limits_length():
    value = normalize_profile_value("  clean\n\npremium\tstyle  ", limit=12)

    assert value == "clean premiu"


def test_normalize_profile_value_treats_em_dash_as_empty():
    assert normalize_profile_value("—") == ""
    assert normalize_profile_value(" – ") == ""
