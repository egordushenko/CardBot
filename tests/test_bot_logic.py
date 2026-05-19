from bot import (
    PAYMENT_UNAVAILABLE_MESSAGE,
    build_after_image_generation_keyboard,
    build_balance_message,
    build_buy_keyboard,
    build_generation_messages,
    build_image_count_keyboard,
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


def test_main_menu_contains_image_generation_entrypoint():
    keyboard = build_main_menu()

    flattened = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert "action:images" in flattened


def test_image_keyboards_follow_spec_callbacks():
    photo_keyboard = build_image_photo_keyboard(photos_count=2)
    count_keyboard = build_image_count_keyboard()
    packages_keyboard = build_image_packages_keyboard()
    after_keyboard = build_after_image_generation_keyboard()

    assert photo_keyboard.inline_keyboard[0][0].callback_data == "img_photos_done"
    assert photo_keyboard.inline_keyboard[0][1].callback_data == "img_add_more"
    assert [button.callback_data for row in count_keyboard.inline_keyboard for button in row] == [
        "img_count:1",
        "img_count:3",
        "img_count:5",
        "img_count:7",
        "img_count:9",
    ]
    assert packages_keyboard.inline_keyboard[0][0].callback_data == "img_buy:img_mini"
    assert after_keyboard.inline_keyboard[0][0].callback_data == "action:images"


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

    assert f"Бесплатно осталось: {TRIAL_GENERATIONS - 1}" in text
    assert "Платных генераций: 7" in text
    assert "Изображений: 4" in text


def test_buy_keyboard_contains_package_buttons_but_runtime_uses_stub_message():
    keyboard = build_buy_keyboard()

    assert PAYMENT_UNAVAILABLE_MESSAGE == "💳 Оплата временно недоступна, скоро откроем!"
    assert len(keyboard.inline_keyboard) == 3
    assert keyboard.inline_keyboard[0][0].callback_data == "buy:starter"
