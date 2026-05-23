import pytest

from llm import ImageConcept
from visual_pipeline import (
    ImageQualityReport,
    PhotoAnalysis,
    build_image_concepts_from_plan,
    build_slide_plan,
    detect_visual_profile,
    parse_image_quality_payload,
    parse_photo_analysis_payload,
)


def test_parse_photo_analysis_payload_extracts_tags_text_defects_and_usage():
    result = parse_photo_analysis_payload(
        """
        {
          "photos": [
            {
              "photo_index": 1,
              "tags": ["back", "on_model", "label", "noise"],
              "visible_text": ["THERAPY FOR YOU", "M", "100% COTTON"],
              "defects": ["home lighting", "wrinkles"],
              "usable_for": ["back_on_model", "print_reference"],
              "summary": "Back view on a model with visible print."
            }
          ]
        }
        """,
        photos_count=3,
    )

    assert result == [
        PhotoAnalysis(
            photo_index=1,
            tags=("back", "on_model", "label"),
            visible_text=("THERAPY FOR YOU", "M", "100% COTTON"),
            defects=("home lighting", "wrinkles"),
            usable_for=("back_on_model", "print_reference"),
            summary="Back view on a model with visible print.",
        )
    ]


def test_detect_visual_profile_covers_required_profiles():
    assert detect_visual_profile("black cotton rashguard") == "clothing"
    assert detect_visual_profile("baby winter jacket") == "kids"
    assert detect_visual_profile("hourglass timer wooden base") == "home_decor"
    assert detect_visual_profile("wireless bluetooth headphones") == "electronics"
    assert detect_visual_profile("moisturizing face cream serum") == "cosmetics"
    assert detect_visual_profile("city backpack laptop pocket") == "bags"
    assert detect_visual_profile("protein bar chocolate") == "food"
    assert detect_visual_profile("yoga mat fitness workout") == "sports"


def test_detect_visual_profile_supports_russian_product_descriptions():
    assert detect_visual_profile("Рашгард therapy черный размер M") == "clothing"
    assert detect_visual_profile("Часы песочные высота 15 см") == "home_decor"
    assert detect_visual_profile("Сыворотка для лица с ниацинамидом") == "cosmetics"
    assert detect_visual_profile("Наушники беспроводные Bluetooth") == "electronics"
    assert detect_visual_profile("Органайзер для ванной комнаты") == "home_decor"
    assert detect_visual_profile("Настольная лампа LED спиральная USB") == "home_decor"


def test_build_slide_plan_uses_clothing_five_image_sequence_and_photo_analysis():
    analyses = [
        PhotoAnalysis(0, ("back", "on_model"), ("THERAPY FOR YOU",), (), ("back_on_model", "print_reference")),
        PhotoAnalysis(1, ("closeup", "label"), ("100% COTTON",), (), ("closeup", "label_reference")),
        PhotoAnalysis(2, ("front", "on_model"), (), (), ("front_on_model",)),
        PhotoAnalysis(3, ("flatlay", "front"), (), ("home background",), ("hero", "flatlay")),
    ]

    plan = build_slide_plan(
        product_description="black Therapy rashguard, cotton, fitted",
        marketplace="wb",
        images_count=5,
        photo_analyses=analyses,
    )

    assert [slide.role for slide in plan] == [
        "hero",
        "closeup",
        "lifestyle_back",
        "lifestyle_front",
        "lifestyle_three_quarter",
    ]
    assert [slide.source_photo_index for slide in plan] == [3, 1, 0, 2, 2]
    assert "front view" in plan[3].composition
    assert "three-quarter" in plan[4].composition
    assert any("Do NOT put clothing size" in item for item in plan[1].negative_constraints)


def test_build_slide_plan_uses_hourglass_profile_and_contextual_backgrounds():
    plan = build_slide_plan(
        product_description="hourglass 15 cm black wooden base white sand 5 minutes",
        marketplace="ozon",
        images_count=5,
        photo_analyses=[],
    )

    assert [slide.role for slide in plan] == [
        "hero",
        "facts",
        "closeup",
        "interior",
        "scenario",
    ]
    assert "desk" in plan[0].background
    assert "not a pure white empty background" in plan[0].background
    assert "shelf" in plan[3].background
    assert "kitchen" in plan[4].composition


def test_build_image_concepts_from_plan_uses_role_templates_and_constraints():
    analyses = [
        PhotoAnalysis(0, ("back", "on_model"), ("THERAPY FOR YOU",), (), ("back_on_model", "print_reference")),
    ]
    concepts = build_image_concepts_from_plan(
        product_description="black Therapy rashguard",
        marketplace="wb",
        images_count=1,
        photo_analyses=analyses,
    )

    assert concepts == [
        ImageConcept(
            image_index=1,
            purpose="hero",
            photo_index=0,
            prompt=concepts[0].prompt,
        )
    ]
    prompt = concepts[0].prompt
    assert "SLIDE ROLE: hero" in prompt
    assert "REFERENCE PHOTO: use only photo 0" in prompt
    assert "Do NOT use a pure white empty background" in prompt
    assert "large readable modern sans-serif" in prompt
    assert "Do NOT place text in random corners" in prompt
    assert "Do NOT use meaningless headings" in prompt
    assert "Preserve printed logos and text exactly" in prompt


def test_generated_prompts_use_russian_marketplace_overlay_copy():
    concepts = build_image_concepts_from_plan(
        product_description="Часы песочные высота 15 см, цикл 5 минут, черное деревянное основание",
        marketplace="ozon",
        images_count=3,
        photo_analyses=[],
    )

    prompts = "\n".join(concept.prompt for concept in concepts)
    assert "TEXT OVERLAY: Made for everyday use" not in prompts
    assert "TEXT OVERLAY: Key features" not in prompts
    assert "TEXT OVERLAY: Reliable details" not in prompts
    assert "5 минут" in prompts
    assert "Наглядный таймер" in prompts


def test_clothing_overlay_copy_does_not_expose_size_or_generic_english_labels():
    concepts = build_image_concepts_from_plan(
        product_description="Рашгард Therapy черный размер M, 100% хлопок, облегающий, принт Therapy на спине",
        marketplace="wb",
        images_count=5,
        photo_analyses=[],
    )

    prompts = "\n".join(concept.prompt for concept in concepts)
    assert "TEXT OVERLAY: Clean product view" not in prompts
    assert "TEXT OVERLAY: Fabric and print detail" not in prompts
    assert "размер M" not in prompts
    assert "Размер: M" not in prompts
    assert "Свобода движений" in prompts
    assert "Принт на спине" in prompts


def test_home_decor_organizer_does_not_use_hourglass_copy():
    concepts = build_image_concepts_from_plan(
        product_description="Органайзер для ванной комнаты белый, 3 секции, для косметики и зубных щеток",
        marketplace="ozon",
        images_count=4,
        photo_analyses=[],
    )

    prompts = "\n".join(concept.prompt for concept in concepts)
    assert "5 минут" not in prompts
    assert "Наглядный таймер" not in prompts
    assert "Деревянная основа" not in prompts
    assert "Белый песок" not in prompts
    assert "Порядок в ванной" in prompts
    assert "ванной" in prompts.casefold()


def test_home_decor_bath_mat_does_not_use_hourglass_copy():
    concepts = build_image_concepts_from_plan(
        product_description="Коврик для ванной серый 50 на 80 см, мягкий ворс, нескользящее основание",
        marketplace="ozon",
        images_count=4,
        photo_analyses=[],
    )

    prompts = "\n".join(concept.prompt for concept in concepts)
    assert "5 минут" not in prompts
    assert "Наглядный таймер" not in prompts
    assert "Деревянная основа" not in prompts
    assert "Белый песок" not in prompts
    assert "Мягкий ворс" in prompts
    assert "ванной" in prompts.casefold()


def test_home_decor_subtypes_have_five_distinct_slide_roles():
    organizer = build_slide_plan(
        product_description="Органайзер для ванной комнаты белый, 3 секции",
        marketplace="ozon",
        images_count=5,
        photo_analyses=[],
    )
    bath_mat = build_slide_plan(
        product_description="Коврик для ванной серый, мягкий ворс, нескользящее основание",
        marketplace="ozon",
        images_count=5,
        photo_analyses=[],
    )
    lamp = build_slide_plan(
        product_description="Настольная лампа LED белая USB, регулировка яркости",
        marketplace="ozon",
        images_count=5,
        photo_analyses=[],
    )

    assert [slide.role for slide in organizer] == ["hero", "facts", "closeup", "scenario", "interior"]
    assert [slide.role for slide in bath_mat] == ["hero", "facts", "closeup", "scenario", "interior"]
    assert [slide.role for slide in lamp] == ["hero", "facts", "closeup", "scenario", "interior"]


def test_electronics_and_cosmetics_prompts_do_not_use_generic_placeholder_copy():
    electronics = build_image_concepts_from_plan(
        product_description="Наушники беспроводные Bluetooth, микрофон, шумоподавление, до 6 часов работы",
        marketplace="ozon",
        images_count=4,
        photo_analyses=[],
    )
    cosmetics = build_image_concepts_from_plan(
        product_description="Сыворотка для лица с ниацинамидом 30 мл, увлажнение, выравнивает тон",
        marketplace="wb",
        images_count=4,
        photo_analyses=[],
    )

    prompts = "\n".join(concept.prompt for concept in electronics + cosmetics)
    assert "TEXT OVERLAY: Главное фото" not in prompts
    assert "TEXT OVERLAY: Ключевые преимущества" not in prompts
    assert "TEXT OVERLAY: Сценарий применения" not in prompts
    assert "Чистый звук" in prompts
    assert "Уход каждый день" in prompts


def test_parse_image_quality_payload_flags_failed_generated_image():
    report = parse_image_quality_payload(
        """
        {
          "passed": false,
          "issues": ["pure_white_background", "small_text", "print_mismatch"],
          "summary": "Text is too small and product print changed."
        }
        """
    )

    assert report == ImageQualityReport(
        passed=False,
        issues=("pure_white_background", "small_text", "print_mismatch"),
        summary="Text is too small and product print changed.",
    )


def test_parse_image_quality_payload_rejects_unknown_issue_names():
    report = parse_image_quality_payload(
        '{"passed": false, "issues": ["pure_white_background", "unknown"], "summary": "bad"}'
    )

    assert report.issues == ("pure_white_background",)
