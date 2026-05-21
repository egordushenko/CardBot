from __future__ import annotations

from core.field_resolver import resolve_fields


def test_missing_brand_is_skipped():
    resolved = resolve_fields({}, "Одежда", "ozon", has_photo=False)

    assert "Бренд" not in resolved
    assert "brand" not in resolved


def test_missing_article_is_skipped():
    resolved = resolve_fields({}, "Одежда", "ozon", has_photo=False)

    assert "Артикул" not in resolved
    assert "article" not in resolved


def test_missing_color_with_photo_adds_image_extraction_instruction():
    resolved = resolve_fields({}, "Одежда", "ozon", has_photo=True)

    assert "Цвет" not in resolved
    assert any("извлеки цвет из изображения" in item.lower() for item in resolved["__prompt_instructions"])


def test_missing_color_without_photo_adds_placeholder():
    resolved = resolve_fields({}, "Одежда", "ozon", has_photo=False)

    assert resolved["Цвет"] == "[укажите цвет]"


def test_missing_composition_for_mens_wb_uses_category_default():
    resolved = resolve_fields({}, "Мужская одежда", "wb", has_photo=False)

    assert resolved["Состав"] == "хлопок 92%; эластан 8%"


def test_womens_clothes_infer_gender_from_category():
    resolved = resolve_fields({}, "Женская одежда", "wb", has_photo=False)

    assert resolved["Пол"] == "Женский"
