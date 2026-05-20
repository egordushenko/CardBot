from bot import (
    PAYMENT_UNAVAILABLE_MESSAGE,
    build_after_image_generation_keyboard,
    build_balance_keyboard,
    build_balance_message,
    build_buy_keyboard,
    build_combined_buy_keyboard,
    build_generation_messages,
    build_generation_mode_keyboard,
    build_image_count_keyboard,
    build_image_count_prompt,
    build_image_packages_keyboard,
    build_image_photo_keyboard,
    build_photo_received_message,
    build_marketplace_keyboard,
    build_main_menu,
    extract_image_file_id,
    is_supported_image_document,
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
    assert "action:images" not in flattened


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
    assert packages_keyboard.inline_keyboard[0][0].callback_data == "img_buy:img_mini"
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


def test_buy_keyboard_contains_package_buttons_but_runtime_uses_stub_message():
    keyboard = build_buy_keyboard()

    assert PAYMENT_UNAVAILABLE_MESSAGE == "💳 Оплата временно недоступна, скоро откроем!"
    assert len(keyboard.inline_keyboard) == 3
    assert keyboard.inline_keyboard[0][0].callback_data == "buy:starter"


def test_combined_buy_keyboard_includes_text_and_image_packages():
    keyboard = build_combined_buy_keyboard()
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert "buy:starter" in callbacks
    assert "img_buy:img_mini" in callbacks
