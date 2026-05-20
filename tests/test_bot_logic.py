from bot import (
    build_after_generation_keyboard,
    build_after_image_generation_keyboard,
    build_balance_keyboard,
    build_balance_message,
    build_buy_keyboard,
    build_combo_card_count_keyboard,
    build_combo_photo_count_keyboard,
    build_combined_buy_keyboard,
    build_generation_messages,
    build_generation_mode_keyboard,
    build_help_keyboard,
    build_help_message,
    build_image_count_keyboard,
    build_image_count_prompt,
    build_image_packages_keyboard,
    build_image_photo_keyboard,
    build_text_packages_keyboard,
    build_photo_received_message,
    build_marketplace_keyboard,
    build_main_menu,
    build_repeat_photos_keyboard,
    build_template_delete_confirm_keyboard,
    build_template_details_keyboard,
    build_templates_keyboard,
    combine_repeat_description,
    extract_image_file_id,
    format_template_description_preview,
    is_supported_image_document,
    truncate_template_name,
)
from db import TRIAL_GENERATIONS
from llm import CardGeneration


def test_build_generation_messages_returns_four_copyable_blocks():
    card = CardGeneration(
        title="SEO title",
        description="SEO description",
        keywords="keyword one, keyword two",
        characteristics="Материал: хлопок",
        tokens_used=123,
    )

    messages = build_generation_messages(card)

    assert len(messages) == 4
    assert messages[0].startswith("📌 НАЗВАНИЕ:")
    assert messages[1].startswith("📝 ОПИСАНИЕ:")
    assert messages[2].startswith("🔑 КЛЮЧЕВЫЕ СЛОВА:")
    assert messages[3].startswith("📋 ХАРАКТЕРИСТИКИ:")


def test_marketplace_keyboard_contains_wb_and_ozon_choices():
    keyboard = build_marketplace_keyboard()

    assert len(keyboard.inline_keyboard) == 1
    assert keyboard.inline_keyboard[0][0].text == "Wildberries"
    assert keyboard.inline_keyboard[0][0].callback_data == "marketplace:wb"
    assert keyboard.inline_keyboard[0][1].text == "Ozon"
    assert keyboard.inline_keyboard[0][1].callback_data == "marketplace:ozon"


def test_main_menu_uses_single_generation_entrypoint():
    keyboard = build_main_menu()

    flattened = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert "action:generate" in flattened
    assert "action:templates" in flattened
    assert "action:images" not in flattened


def test_after_generation_keyboard_offers_template_and_repeat_actions():
    text_keyboard = build_after_generation_keyboard()
    image_keyboard = build_after_image_generation_keyboard()

    text_callbacks = [button.callback_data for row in text_keyboard.inline_keyboard for button in row]
    image_callbacks = [button.callback_data for row in image_keyboard.inline_keyboard for button in row]

    assert text_callbacks == [
        "action:generate",
        "action:save_template",
        "action:repeat_edit",
        "action:buy",
    ]
    assert image_callbacks == [
        "action:generate",
        "action:save_template",
        "action:repeat_edit",
        "action:buy_images",
    ]


def test_template_keyboards_use_owner_safe_callbacks():
    templates = [
        {"id": 11, "name": "Lamp", "marketplace": "wb", "mode": "text_and_images"},
        {"id": 12, "name": "Mat", "marketplace": "ozon", "mode": "text_only"},
    ]

    list_keyboard = build_templates_keyboard(templates, page=0, total=8)
    details_keyboard = build_template_details_keyboard(11)
    delete_keyboard = build_template_delete_confirm_keyboard(11)
    repeat_keyboard = build_repeat_photos_keyboard()

    list_callbacks = [button.callback_data for row in list_keyboard.inline_keyboard for button in row]
    details_callbacks = [button.callback_data for row in details_keyboard.inline_keyboard for button in row]
    delete_callbacks = [button.callback_data for row in delete_keyboard.inline_keyboard for button in row]
    repeat_callbacks = [button.callback_data for row in repeat_keyboard.inline_keyboard for button in row]

    assert "template_use:11" in list_callbacks
    assert "template_use:12" in list_callbacks
    assert "templates_page:1" in list_callbacks
    assert "templates_delete:0" in list_callbacks
    assert details_callbacks == ["template_run:11", "template_edit:11", "template_delete:11"]
    assert delete_callbacks == ["template_delete_confirm:11", "template_delete_cancel:11"]
    assert repeat_callbacks == ["repeat:same_photos", "repeat:new_photos"]


def test_template_helpers_truncate_and_combine_description():
    long_name = "x" * 80

    assert truncate_template_name(long_name) == "x" * 50
    assert combine_repeat_description("old", "new color") == "old\n\nИзменения: new color"
    assert format_template_description_preview("a" * 130, limit=20) == ("a" * 20) + "..."


def test_generation_mode_keyboard_offers_text_and_combined_modes():
    keyboard = build_generation_mode_keyboard()

    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert callbacks == ["mode:text_only", "mode:text_and_images"]


def test_image_keyboards_follow_spec_callbacks():
    photo_keyboard = build_image_photo_keyboard(photos_count=2)
    count_keyboard = build_image_count_keyboard(image_balance=5)
    packages_keyboard = build_image_packages_keyboard()
    after_keyboard = build_after_image_generation_keyboard()

    assert photo_keyboard.inline_keyboard[0][0].callback_data == "img_photos_done"
    assert photo_keyboard.inline_keyboard[0][1].callback_data == "img_add_more"
    count_callbacks = [button.callback_data for row in count_keyboard.inline_keyboard for button in row]
    assert count_callbacks == [
        "img_count:1",
        "img_count:3",
        "img_count:5",
    ]
    assert "img_count:7" not in count_callbacks
    assert packages_keyboard.inline_keyboard[0][0].callback_data == "buy:addon_img_20"
    assert after_keyboard.inline_keyboard[0][0].callback_data == "action:generate"


def test_image_count_prompt_shows_current_balance():
    assert "5" in build_image_count_prompt(image_balance=5)


def test_extract_image_file_id_accepts_photo_and_image_document():
    class Photo:
        def __init__(self, file_id):
            self.file_id = file_id

    class Document:
        file_id = "document-file-id"
        mime_type = "image/png"

    class PhotoMessage:
        photo = [Photo("small"), Photo("large")]
        document = None

    class DocumentMessage:
        photo = []
        document = Document()

    assert extract_image_file_id(PhotoMessage()) == "large"
    assert extract_image_file_id(DocumentMessage()) == "document-file-id"
    assert is_supported_image_document(Document()) is True


def test_build_photo_received_message_groups_album_count():
    assert build_photo_received_message(added_count=3, total_count=3).startswith("Фото 3 получено")
    assert "Всего: 3/5" in build_photo_received_message(added_count=3, total_count=3)


def test_generation_messages_use_hashtags_label_for_ozon():
    card = CardGeneration(
        title="SEO title",
        description="SEO description",
        keywords="#tag #other",
        characteristics="Материал: хлопок",
        marketplace="ozon",
    )

    messages = build_generation_messages(card)

    assert messages[2].startswith("🔖 ХЭШТЕГИ:")
    assert "#tag #other" in messages[2]


def test_build_balance_message_shows_trial_paid_and_image_balance():
    text = build_balance_message(trial_used=1, balance=7, image_balance=4)

    assert str(TRIAL_GENERATIONS - 1 + 7) in text
    assert "4" in text


def test_balance_keyboard_offers_both_package_types():
    keyboard = build_balance_keyboard()
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert callbacks == ["action:buy_text", "action:buy_images"]


def test_help_message_contains_contact_and_offer_link_button():
    text = build_help_message()
    keyboard = build_help_keyboard("https://alterega.ru/cardbot/offer")

    assert "alterega@list.ru" in text
    assert "публичная оферта" in text.lower()
    assert keyboard.inline_keyboard[0][0].text == "Публичная оферта"
    assert keyboard.inline_keyboard[0][0].url == "https://alterega.ru/cardbot/offer"


def test_buy_keyboard_starts_with_package_categories():
    keyboard = build_buy_keyboard(show_first_image_promo=True)
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert callbacks == ["action:buy_combo", "action:buy_text", "action:buy_images"]
    assert all(not callback.startswith("buy:") for callback in callbacks)


def test_text_package_buttons_are_short_enough_for_mobile():
    keyboard = build_text_packages_keyboard()
    labels = [row[0].text for row in keyboard.inline_keyboard]

    assert labels == [
        "10 карточек за 560 ₽",
        "30 карточек за 1 370 ₽",
        "100 карточек за 3 440 ₽",
    ]
    assert all("—" not in label for label in labels)
    assert all("Докупить" not in label for label in labels)


def test_combined_buy_keyboard_includes_text_and_image_packages():
    keyboard = build_combined_buy_keyboard(show_first_image_promo=False)
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert callbacks == ["action:buy_combo", "action:buy_text", "action:buy_images"]


def test_combo_card_count_keyboard_is_short_and_staged():
    keyboard = build_combo_card_count_keyboard()
    labels = [button.text for row in keyboard.inline_keyboard for button in row]
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert labels == ["10 карточек", "30 карточек", "100 карточек", "⬅️ Назад"]
    assert callbacks == ["combo_cards:10", "combo_cards:30", "combo_cards:100", "buy_back:root"]


def test_combo_photo_count_keyboard_uses_short_final_payment_labels():
    keyboard = build_combo_photo_count_keyboard(10)
    labels = [button.text for row in keyboard.inline_keyboard for button in row]
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert labels == [
        "Без фото — 490 ₽",
        "3 фото/карточка — 1 990 ₽",
        "5 фото/карточка — 2 990 ₽",
        "7 фото/карточка — 3 990 ₽",
        "⬅️ Назад",
    ]
    assert callbacks == [
        "buy:text_start_x0",
        "buy:text_start_x3",
        "buy:text_start_x5",
        "buy:text_start_x7",
        "buy_back:combo",
    ]
    assert all("Старт" not in label for label in labels)
    assert all(len(label) <= 28 for label in labels)
