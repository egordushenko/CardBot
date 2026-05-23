import asyncio

from bot import (
    FEEDBACK_MESSAGE,
    GENERATE_PROMPT,
    IMAGE_DESCRIPTION_PROMPT,
    IMAGE_PHOTO_PROMPT,
    MARKETPLACE_PROMPT,
    MODE_PROMPT,
    NEW_TEMPLATE_TEXT_PROMPT,
    REPEAT_CHANGES_PROMPT,
    REPEAT_PHOTOS_PROMPT,
    TEMPLATE_NAME_PROMPT,
    TECHNICAL_WORKS_MESSAGE,
    classify_generation_error,
    generation_error_message,
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
    build_image_progress_message,
    build_image_packages_keyboard,
    build_image_photo_keyboard,
    build_persistent_main_keyboard,
    build_text_packages_keyboard,
    build_photo_received_message,
    build_marketplace_keyboard,
    build_main_menu,
    build_start_message,
    build_repeat_photos_keyboard,
    _aggregate_image_generation_cost,
    build_template_delete_confirm_keyboard,
    build_template_details_keyboard,
    build_templates_keyboard,
    combine_repeat_description,
    classify_reply_action,
    extract_image_file_id,
    format_template_description_preview,
    format_template_mode,
    handle_callback,
    _handle_image_description,
    should_generate_text_with_images,
    _handle_new_template_text,
    _handle_new_template_name,
    is_allowed_image_count,
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

    assert len(messages) == 3
    assert messages[0].startswith("📌 НАЗВАНИЕ:")
    assert messages[1].startswith("📝 ОПИСАНИЕ:")
    assert messages[2].startswith("📋 ХАРАКТЕРИСТИКИ:")


def test_marketplace_keyboard_contains_wb_and_ozon_choices():
    keyboard = build_marketplace_keyboard()

    assert len(keyboard.inline_keyboard) == 2
    assert keyboard.inline_keyboard[0][0].text == "Wildberries"
    assert keyboard.inline_keyboard[0][0].callback_data == "marketplace:wb"
    assert keyboard.inline_keyboard[0][1].text == "Ozon"
    assert keyboard.inline_keyboard[0][1].callback_data == "marketplace:ozon"
    assert keyboard.inline_keyboard[-1][0].callback_data == "action:home"


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
        "action:feedback",
        "action:home",
    ]
    assert image_callbacks == [
        "action:generate",
        "action:save_template",
        "action:repeat_edit",
        "action:buy_images",
        "action:feedback",
        "action:home",
    ]
    assert text_keyboard.inline_keyboard[0][0].text.startswith("⚡")
    assert "Не понравился результат" in text_keyboard.inline_keyboard[-2][0].text
    assert "@alterega" in FEEDBACK_MESSAGE
    assert "Контакт: @alterega" in FEEDBACK_MESSAGE


def test_classify_generation_error_returns_safe_reasons():
    class RateLimit(Exception):
        status_code = 429

    class PaymentRequired(Exception):
        status_code = 402

    assert classify_generation_error(Exception("LLM returned empty response")) == "empty_response"
    assert classify_generation_error(RateLimit("too many")) == "429"
    assert classify_generation_error(PaymentRequired("insufficient credits")) == "api_balance"
    assert classify_generation_error(Exception("No auth credentials found")) == "api_balance"
    assert classify_generation_error(Exception("LLM returned invalid JSON")) == "parse_error"
    assert classify_generation_error(Exception("missing required field: title")) == "parse_error"
    assert classify_generation_error(Exception("other")) == "unknown"


def test_generation_error_message_uses_technical_works_for_api_balance():
    assert "технические работы" in TECHNICAL_WORKS_MESSAGE.casefold()
    assert generation_error_message("api_balance") == TECHNICAL_WORKS_MESSAGE
    assert generation_error_message("429") == TECHNICAL_WORKS_MESSAGE
    assert "Генерация не списана" in generation_error_message("parse_error")


def test_aggregate_image_generation_cost_counts_failed_images():
    summary = _aggregate_image_generation_cost(
        [
            {"model": "openai/gpt-5.4-image-2", "cost_usd": 0.2},
            {"model": "openai/gpt-5.4-image-2", "cost_usd": 0.198001},
        ],
        requested_count=3,
        fallback_model="fallback",
    )

    assert summary == {
        "model": "openai/gpt-5.4-image-2",
        "cost_usd": 0.398001,
        "image_count": 2,
        "failed_count": 1,
    }


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
    assert "template_new" in list_callbacks
    assert "templates_page:1" in list_callbacks
    assert "templates_delete:0" in list_callbacks
    assert details_callbacks == ["template_run:11", "template_edit:11", "template_delete:11", "action:home"]
    assert delete_callbacks == ["template_delete_confirm:11", "template_delete_cancel:11", "action:home"]
    assert repeat_callbacks == ["repeat:same_photos", "repeat:new_photos", "action:home"]


def test_template_helpers_truncate_and_combine_description():
    long_name = "x" * 80

    assert truncate_template_name(long_name) == "x" * 50
    assert combine_repeat_description("old", "new color") == "old\n\nИзменения: new color"
    assert format_template_description_preview("a" * 130, limit=20) == ("a" * 20) + "..."


class _FakeMessage:
    def __init__(self):
        self.replies = []

    async def reply_text(self, text, **kwargs):
        self.replies.append((text, kwargs))


class _FakeUpdate:
    def __init__(self, text):
        self.effective_message = _FakeMessage()
        self.effective_message.text = text


class _FakeTemplateDb:
    def __init__(self, count=0):
        self.count = count
        self.saved = []

    async def get_templates_count(self, user_id):
        return self.count

    async def save_template(self, **kwargs):
        self.saved.append(kwargs)
        return 42


class _FakeTemplateApplication:
    def __init__(self, db):
        self.bot_data = {"db": db}


class _FakeTemplateContext:
    def __init__(self, db):
        self.user_data = {}
        self.application = _FakeTemplateApplication(db)


def test_new_template_flow_collects_name_then_saves_text_without_generation():
    async def run_flow():
        db = _FakeTemplateDb()
        context = _FakeTemplateContext(db)
        context.user_data["awaiting_new_template_name"] = True

        name_update = _FakeUpdate("Зимняя шапка")
        handled_name = await _handle_new_template_name(name_update, context, user_id=123, user_input="Зимняя шапка")

        assert handled_name is True
        assert context.user_data["new_template_name"] == "Зимняя шапка"
        assert context.user_data["awaiting_new_template_text"] is True
        assert "текст шаблона" in name_update.effective_message.replies[0][0].casefold()

        text_update = _FakeUpdate("Шапка, цвет {цвет}, размер {размер}")
        handled_text = await _handle_new_template_text(
            text_update,
            context,
            user_id=123,
            user_input="Шапка, цвет {цвет}, размер {размер}",
        )

        assert handled_text is True
        assert db.saved == [
            {
                "user_id": 123,
                "name": "Зимняя шапка",
                "marketplace": "wb",
                "mode": "text_only",
                "description": "Шапка, цвет {цвет}, размер {размер}",
                "photo_file_ids": [],
                "images_count": None,
            }
        ]
        assert "Найдёте его в «Мои шаблоны»" in text_update.effective_message.replies[0][0]
        assert "awaiting_new_template_text" not in context.user_data
        assert "new_template_name" not in context.user_data

    asyncio.run(run_flow())

def test_generation_mode_keyboard_offers_text_combined_and_image_only_modes():
    keyboard = build_generation_mode_keyboard()

    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert callbacks == [
        "mode:text_only",
        "mode:text_and_images",
        "mode:images_only",
        "action:generate",
        "action:home",
    ]


def test_generation_mode_prompt_separates_options_visually():
    assert MODE_PROMPT == (
        "Что сгенерировать?\n\n"
        "📝 «Только текст»\n"
        "Название, описание, ключевые слова, характеристики.\n"
        "Тратит 1 текстовую генерацию.\n\n"
        "🖼 «Текст + изображения»\n"
        "Всё выше плюс изображения для карточки.\n"
        "Тратит 1 текстовую генерацию + N изображений.\n\n"
        "🖼 «Только изображения»\n"
        "Изображения для карточки по описанию и фото товара.\n"
        "Тратит только изображения."
    )


def test_images_only_mode_is_named_for_templates():
    assert format_template_mode("images_only") == "Только изображения"


def test_generation_dispatch_separates_image_only_from_combined_mode():
    assert should_generate_text_with_images("text_and_images") is True
    assert should_generate_text_with_images("images_only") is False
    assert should_generate_text_with_images("text_only") is False


def test_primary_prompts_use_clear_visual_blocks():
    assert GENERATE_PROMPT == (
        "📝 Опишите товар\n\n"
        "Минимум — название.\n"
        "Можно добавить: материал, размер, цвет, особенности.\n"
        "Чем подробнее описание, тем точнее карточка."
    )
    assert IMAGE_DESCRIPTION_PROMPT == (
        "📝 Опишите товар\n\n"
        "Укажите название, материал, размер, цвет и главные преимущества.\n"
        "После этого бот попросит загрузить фото товара."
    )
    assert IMAGE_PHOTO_PROMPT == (
        "📸 Загрузите от 1 до 7 фото товара с разных ракурсов.\n\n"
        "Когда все фото загружены, нажмите ✅ Готово"
    )
    assert TEMPLATE_NAME_PROMPT.startswith("📋 Введите название шаблона")
    assert NEW_TEMPLATE_TEXT_PROMPT.startswith("✍️ Введите текст шаблона")
    assert REPEAT_CHANGES_PROMPT.startswith("🔄 Что изменить?")
    assert REPEAT_PHOTOS_PROMPT == "📸 Какие фото использовать?"
    assert MARKETPLACE_PROMPT == "🛒 Выберите маркетплейс:"
    assert TECHNICAL_WORKS_MESSAGE.startswith("⚙️")


def test_start_help_and_balance_messages_are_scannable():
    assert build_start_message("Егор") == (
        "Здравствуйте, Егор.\n\n"
        "🛒 Я помогу подготовить карточку товара для Wildberries и Ozon.\n\n"
        "На старте доступно 3 бесплатные текстовые генерации."
    )

    help_text = build_help_message()
    balance_text = build_balance_message(trial_used=1, balance=7, image_balance=4)

    assert "📝 Как пользоваться" in help_text
    assert "💳 Оплата и поддержка" in help_text
    assert balance_text.startswith("📊 Баланс")
    assert "📝 Текстовые генерации:" in balance_text
    assert "🖼 Изображения:" in balance_text


def test_image_keyboards_follow_spec_callbacks():
    photo_keyboard = build_image_photo_keyboard(photos_count=2)
    count_keyboard = build_image_count_keyboard(image_balance=5)
    full_count_keyboard = build_image_count_keyboard(image_balance=20)
    packages_keyboard = build_image_packages_keyboard()
    after_keyboard = build_after_image_generation_keyboard()

    assert photo_keyboard.inline_keyboard[0][0].callback_data == "img_photos_done"
    assert photo_keyboard.inline_keyboard[0][1].callback_data == "img_add_more"
    assert len(build_image_photo_keyboard(photos_count=7).inline_keyboard[0]) == 1
    assert build_image_photo_keyboard(photos_count=7).inline_keyboard[-1][0].callback_data == "action:home"
    count_callbacks = [button.callback_data for row in count_keyboard.inline_keyboard for button in row]
    assert [callback for callback in count_callbacks if callback.startswith("img_count:")] == [
        "img_count:1",
        "img_count:3",
        "img_count:5",
    ]
    assert "action:home" in count_callbacks
    assert "img_count:7" not in count_callbacks
    full_count_callbacks = [
        button.callback_data for row in full_count_keyboard.inline_keyboard for button in row
    ]
    assert [callback for callback in full_count_callbacks if callback.startswith("img_count:")] == [
        "img_count:1",
        "img_count:3",
        "img_count:5",
        "img_count:7",
    ]
    assert "img_count:9" not in full_count_callbacks
    assert is_allowed_image_count(7) is True
    assert is_allowed_image_count(9) is False
    assert packages_keyboard.inline_keyboard[0][0].callback_data == "buy:addon_img_20"
    assert after_keyboard.inline_keyboard[0][0].callback_data == "action:generate"


class _FakeCallbackQuery:
    def __init__(self, data):
        self.data = data
        self.message = _FakeMessage()
        self.answers = []

    async def answer(self, *args, **kwargs):
        self.answers.append((args, kwargs))


class _FakeUser:
    id = 123
    username = "seller"
    first_name = "Егор"


class _FakeCallbackUpdate:
    def __init__(self, data):
        self.callback_query = _FakeCallbackQuery(data)
        self.effective_user = _FakeUser()
        self.effective_message = self.callback_query.message


class _FakeImageModeDb:
    async def upsert_user(self, *args, **kwargs):
        return None

    async def get_image_balance(self, user_id):
        return 3


class _FakeImageModeApplication:
    def __init__(self, db):
        self.bot_data = {"db": db}


class _FakeImageModeContext:
    def __init__(self, db):
        self.user_data = {"marketplace": "wb", "generation_step": "mode"}
        self.application = _FakeImageModeApplication(db)


def test_images_only_mode_routes_to_description_without_text_generation():
    async def run_flow():
        context = _FakeImageModeContext(_FakeImageModeDb())
        update = _FakeCallbackUpdate("mode:images_only")

        await handle_callback(update, context)

        assert context.user_data["mode"] == "images_only"
        assert context.user_data["generation_step"] == "description"
        assert update.callback_query.message.replies[-1][0] == IMAGE_DESCRIPTION_PROMPT

    asyncio.run(run_flow())


def test_images_only_description_step_moves_to_photo_upload():
    async def run_flow():
        context = _FakeTemplateContext(_FakeTemplateDb())
        context.user_data["generation_step"] = "description"
        context.user_data["mode"] = "images_only"
        update = _FakeUpdate("Часы песочные, черное основание")

        handled = await _handle_image_description(
            update,
            context,
            "Часы песочные, черное основание",
        )

        assert handled is True
        assert context.user_data["img_description"] == "Часы песочные, черное основание"
        assert context.user_data["generation_step"] == "photos"
        assert update.effective_message.replies[-1][0] == IMAGE_PHOTO_PROMPT

    asyncio.run(run_flow())


def test_image_count_prompt_shows_current_balance():
    assert "5" in build_image_count_prompt(image_balance=5)


def test_image_progress_message_uses_single_ready_counter():
    text = build_image_progress_message(total_count=7, generated_count=3, sent_count=2)

    assert "Готово: 2 из 7" in text
    assert "Сгенерировано:" not in text
    assert "Отправлено:" not in text


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
    assert "Всего: 3/7" in build_photo_received_message(added_count=3, total_count=3)
    assert "от 1 до 7 фото" in IMAGE_PHOTO_PROMPT


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

    assert callbacks == ["action:buy_combo", "action:buy_text", "action:buy_images", "action:home"]
    assert keyboard.inline_keyboard[0][0].text.startswith("💳")


def test_help_message_contains_contact_and_offer_link_button():
    text = build_help_message()
    keyboard = build_help_keyboard("https://alterega.ru/cardbot/offer")

    assert "alterega@list.ru" in text
    assert "Самозанятый Дущенко Егор Владимирович" in text
    assert "ИНН: 615422982815" in text
    assert "публичная оферта" in text.lower()
    assert keyboard.inline_keyboard[0][0].text == "Публичная оферта"
    assert keyboard.inline_keyboard[0][0].url == "https://alterega.ru/cardbot/offer"


def test_buy_keyboard_starts_with_package_categories():
    keyboard = build_buy_keyboard(show_first_image_promo=True)
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert callbacks == ["action:buy_combo", "action:buy_text", "action:buy_images", "action:home"]
    assert keyboard.inline_keyboard[0][0].text.startswith("💳")
    assert all(not callback.startswith("buy:") for callback in callbacks)


def test_text_package_buttons_are_short_enough_for_mobile():
    keyboard = build_text_packages_keyboard()
    labels = [row[0].text for row in keyboard.inline_keyboard if row[0].callback_data.startswith("buy:")]

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

    assert callbacks == ["action:buy_combo", "action:buy_text", "action:buy_images", "action:home"]


def test_combo_card_count_keyboard_is_short_and_staged():
    keyboard = build_combo_card_count_keyboard()
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert callbacks == ["combo_cards:10", "combo_cards:30", "combo_cards:100", "buy_back:root", "action:home"]


def test_combo_photo_count_keyboard_uses_short_final_payment_labels():
    keyboard = build_combo_photo_count_keyboard(10)
    labels = [button.text for row in keyboard.inline_keyboard for button in row if button.callback_data.startswith("buy:")]
    callbacks = [button.callback_data for row in keyboard.inline_keyboard for button in row]

    assert labels == [
        "Без фото — 490 ₽",
        "3 фото на карточку — 1 990 ₽",
        "5 фото на карточку — 2 990 ₽",
        "7 фото на карточку — 3 990 ₽",
    ]
    assert callbacks == [
        "buy:text_start_x0",
        "buy:text_start_x3",
        "buy:text_start_x5",
        "buy:text_start_x7",
        "buy_back:combo",
        "action:home",
    ]
    assert all("Старт" not in label for label in labels)
    assert all(len(label) <= 28 for label in labels)



def test_persistent_reply_keyboard_routes_primary_actions():
    keyboard = build_persistent_main_keyboard()
    labels = [label for row in keyboard.keyboard for label in row]
    texts = [getattr(label, "text", label) for label in labels]

    assert classify_reply_action(labels[0]) == "generate"
    assert "🕐 История" in texts
    assert "\U0001f3e0 \u0413\u043b\u0430\u0432\u043d\u0430\u044f" not in texts
    assert classify_reply_action("\u0413\u043b\u0430\u0432\u043d\u0430\u044f") == "home"
    assert classify_reply_action("\U0001f3e0 \u0413\u043b\u0430\u0432\u043d\u0430\u044f") == "home"
    assert classify_reply_action("🕐 История") == "history"
    assert classify_reply_action("\u043e\u0431\u044b\u0447\u043d\u044b\u0439 \u0442\u043e\u0432\u0430\u0440") is None
