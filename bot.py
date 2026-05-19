from __future__ import annotations

import logging
from asyncio import as_completed
from io import BytesIO
from dataclasses import dataclass
from typing import Any

from config import Settings, load_settings
from db import IMAGE_PACKAGES, PACKAGES, Database, UsageMode
from image_generator import generate_marketplace_image
from llm import CardGeneration, ImageConcept, generate_card, generate_image_prompts, normalize_marketplace


PAYMENT_UNAVAILABLE_MESSAGE = "💳 Оплата временно недоступна, скоро откроем!"
GENERATE_PROMPT = (
    "Отправьте описание товара. Минимум — название. "
    "Можно добавить материал, размер, цвет и особенности."
)
MARKETPLACE_PROMPT = "Выберите маркетплейс:"
IMAGE_DESCRIPTION_PROMPT = (
    "Опишите товар: название, материал, размер, цвет, ключевые преимущества. "
    "Чем подробнее — тем лучше результат."
)
IMAGE_PHOTO_PROMPT = (
    "Загрузите от 1 до 5 фото товара с разных ракурсов. "
    "Когда загрузите все — нажмите ✅ Готово"
)
IMAGE_COUNT_PROMPT = "Сколько изображений сгенерировать для карточки?"


@dataclass(frozen=True)
class KeyboardButton:
    text: str
    callback_data: str


@dataclass(frozen=True)
class KeyboardMarkup:
    inline_keyboard: list[list[KeyboardButton]]


def _button(text: str, callback_data: str) -> Any:
    try:
        from telegram import InlineKeyboardButton

        return InlineKeyboardButton(text, callback_data=callback_data)
    except ImportError:
        return KeyboardButton(text=text, callback_data=callback_data)


def _keyboard(rows: list[list[Any]]) -> Any:
    try:
        from telegram import InlineKeyboardMarkup

        return InlineKeyboardMarkup(rows)
    except ImportError:
        return KeyboardMarkup(rows)


def build_main_menu() -> Any:
    return _keyboard(
        [
            [_button("⚡ Сгенерировать карточку", "action:generate")],
            [_button("🖼 Создать изображения", "action:images")],
            [
                _button("💳 Купить генерации", "action:buy"),
                _button("📊 Мой баланс", "action:balance"),
            ],
            [
                _button("📋 История", "action:history"),
                _button("❓ Помощь", "action:help"),
            ],
        ]
    )


def build_buy_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button(
                    f"{package['name']} — {package['generations']} за {package['price_rub']} ₽",
                    f"buy:{code}",
                )
            ]
            for code, package in PACKAGES.items()
        ]
    )


def build_image_packages_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button(
                    f"{package['name']} — {package['images']} за {package['price_rub']} ₽",
                    f"img_buy:{code}",
                )
            ]
            for code, package in IMAGE_PACKAGES.items()
        ]
    )


def build_marketplace_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("Wildberries", "marketplace:wb"),
                _button("Ozon", "marketplace:ozon"),
            ]
        ]
    )


def build_image_marketplace_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("Wildberries", "img_marketplace:wb"),
                _button("Ozon", "img_marketplace:ozon"),
            ]
        ]
    )


def build_image_photo_keyboard(photos_count: int) -> Any:
    row = [_button("✅ Готово", "img_photos_done")]
    if photos_count < 5:
        row.append(_button(f"📎 Ещё ({photos_count}/5)", "img_add_more"))
    return _keyboard([row])


def build_image_count_keyboard() -> Any:
    return _keyboard(
        [
            [_button("1", "img_count:1"), _button("3", "img_count:3"), _button("5", "img_count:5")],
            [_button("7", "img_count:7"), _button("9", "img_count:9")],
        ]
    )


def build_after_generation_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("🔄 Сгенерировать ещё", "action:generate"),
                _button("💳 Купить генерации", "action:buy"),
            ]
        ]
    )


def build_after_image_generation_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("🔄 Сгенерировать ещё", "action:images"),
                _button("💳 Пополнить баланс", "action:buy_images"),
            ]
        ]
    )


def build_generation_messages(card: CardGeneration) -> list[str]:
    search_label = "🔖 ХЭШТЕГИ" if card.marketplace == "ozon" else "🔑 КЛЮЧЕВЫЕ СЛОВА"
    return [
        f"📌 НАЗВАНИЕ:\n{card.title}",
        f"📝 ОПИСАНИЕ:\n{card.description}",
        f"{search_label}:\n{card.keywords}",
        f"📋 ХАРАКТЕРИСТИКИ:\n{card.characteristics}",
    ]


def build_balance_message(
    trial_used: int,
    balance: int,
    image_balance: int = 0,
    trial_generations: int = 3,
) -> str:
    free_left = max(trial_generations - trial_used, 0)
    return (
        "📊 Ваш баланс\n\n"
        f"Бесплатно осталось: {free_left}\n"
        f"Платных генераций: {balance}\n"
        f"Изображений: {image_balance}"
    )


def build_help_message() -> str:
    return (
        "CardBot генерирует SEO-карточки товаров для Wildberries и Ozon.\n\n"
        "Просто отправьте описание товара одним сообщением. "
        "Бот вернёт название, описание, ключевые слова и характеристики.\n\n"
        "/generate — создать карточку\n"
        "/images — создать изображения карточки\n"
        "/balance — баланс\n"
        "/history — последние генерации\n"
        "/buy — пакеты генераций"
    )


def build_start_message(first_name: str | None) -> str:
    name = f", {first_name}" if first_name else ""
    return (
        f"Здравствуйте{name}.\n\n"
        "Я помогу быстро подготовить карточку товара для WB и Ozon. "
        "У вас есть 3 бесплатные генерации."
    )


def _get_db(context: Any) -> Database:
    return context.application.bot_data["db"]


def _get_settings(context: Any) -> Settings:
    return context.application.bot_data["settings"]


def _clear_image_session(context: Any) -> None:
    for key in (
        "img_marketplace",
        "img_description",
        "img_photos",
        "img_count",
        "img_waiting_description",
        "img_waiting_photos",
    ):
        context.user_data.pop(key, None)


async def _ensure_user(update: Any, context: Any) -> int | None:
    user = update.effective_user
    if user is None:
        return None
    await _get_db(context).upsert_user(user.id, user.username, user.first_name)
    return user.id


async def start(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None:
        return
    user = update.effective_user
    await update.effective_message.reply_text(
        build_start_message(user.first_name if user else None),
        reply_markup=build_main_menu(),
    )


async def generate_command(update: Any, context: Any) -> None:
    await _ensure_user(update, context)
    context.user_data.pop("marketplace", None)
    await update.effective_message.reply_text(
        MARKETPLACE_PROMPT,
        reply_markup=build_marketplace_keyboard(),
    )


async def images_command(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None:
        return
    await _start_image_flow(update.effective_message, context, user_id)


async def balance_command(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None:
        return
    settings = _get_settings(context)
    balance = await _get_db(context).get_balance(user_id)
    await update.effective_message.reply_text(
        build_balance_message(
            balance.trial_used,
            balance.balance,
            image_balance=balance.image_balance,
            trial_generations=settings.trial_generations,
        )
    )


async def buy_command(update: Any, context: Any) -> None:
    await _ensure_user(update, context)
    await update.effective_message.reply_text(
        PAYMENT_UNAVAILABLE_MESSAGE,
        reply_markup=build_buy_keyboard(),
    )


async def help_command(update: Any, context: Any) -> None:
    await _ensure_user(update, context)
    await update.effective_message.reply_text(build_help_message(), reply_markup=build_main_menu())


async def history_command(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None:
        return

    generations = await _get_db(context).get_recent_generations(user_id, limit=5)
    if not generations:
        await update.effective_message.reply_text("История пока пустая.")
        return

    for index, generation in enumerate(generations, start=1):
        created_at = generation["created_at"].strftime("%d.%m.%Y %H:%M")
        text = (
            f"📋 История #{index} — {created_at}\n\n"
            f"Запрос: {generation['input_text']}\n\n"
            f"📌 {generation['output_title']}\n\n"
            f"📝 {generation['output_description']}\n\n"
            f"🔑 {generation['output_keywords']}\n\n"
            f"📋 {generation['output_characteristics']}"
        )
        await update.effective_message.reply_text(text)


async def _start_image_flow(message: Any, context: Any, user_id: int) -> None:
    _clear_image_session(context)
    image_balance = await _get_db(context).get_image_balance(user_id)
    if image_balance <= 0:
        await message.reply_text(
            "Баланс изображений пуст. Выберите пакет изображений:",
            reply_markup=build_image_packages_keyboard(),
        )
        return

    await message.reply_text(
        MARKETPLACE_PROMPT,
        reply_markup=build_image_marketplace_keyboard(),
    )


async def _handle_image_description(update: Any, context: Any, user_input: str) -> bool:
    if not context.user_data.get("img_waiting_description"):
        return False

    if len(user_input) < 3:
        await update.effective_message.reply_text(
            "Добавьте хотя бы название или категорию товара."
        )
        return True

    context.user_data["img_description"] = user_input
    context.user_data["img_waiting_description"] = False
    context.user_data["img_waiting_photos"] = True
    context.user_data["img_photos"] = []
    await update.effective_message.reply_text(IMAGE_PHOTO_PROMPT)
    return True


async def handle_photo(update: Any, context: Any) -> None:
    await _ensure_user(update, context)
    if not context.user_data.get("img_waiting_photos"):
        return

    message = update.effective_message
    photos = list(context.user_data.get("img_photos") or [])
    if len(photos) >= 5:
        await message.reply_text(
            "Максимум 5 фото. Нажмите ✅ Готово",
            reply_markup=build_image_photo_keyboard(len(photos)),
        )
        return

    if not message.photo:
        return

    photos.append(message.photo[-1].file_id)
    context.user_data["img_photos"] = photos
    await message.reply_text(
        f"Фото {len(photos)} получено ✓",
        reply_markup=build_image_photo_keyboard(len(photos)),
    )


async def _generate_images_for_user(
    update: Any,
    context: Any,
    user_id: int,
    images_count: int,
) -> None:
    message = update.callback_query.message
    settings = _get_settings(context)
    db = _get_db(context)
    marketplace = context.user_data.get("img_marketplace")
    product_description = context.user_data.get("img_description")
    photo_file_ids = list(context.user_data.get("img_photos") or [])

    if not marketplace or not product_description or not photo_file_ids:
        await message.reply_text(
            "Сессия генерации изображений устарела. Начните заново.",
            reply_markup=build_after_image_generation_keyboard(),
        )
        _clear_image_session(context)
        return

    current_balance = await db.get_image_balance(user_id)
    if current_balance < images_count:
        missing = images_count - current_balance
        await message.reply_text(
            f"Не хватает {missing} изображений на балансе. Пополните баланс:",
            reply_markup=build_image_packages_keyboard(),
        )
        return

    session_id = await db.create_image_session(
        user_id=user_id,
        product_description=product_description,
        marketplace=marketplace,
        photos_count=len(photo_file_ids),
        images_requested=images_count,
    )

    await message.reply_text("⏳ Разрабатываю концепцию изображений...")
    try:
        concepts = await generate_image_prompts(
            product_description=product_description,
            marketplace=marketplace,
            photos_count=len(photo_file_ids),
            images_count=images_count,
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            site_url=settings.site_url,
        )
        await db.update_image_session_prompts(
            session_id,
            _serialize_image_concepts(concepts),
            status="generating",
        )
    except Exception:
        logging.exception("Image prompt generation failed")
        await db.set_image_session_status(session_id, "failed")
        await message.reply_text(
            "Не удалось разработать концепцию изображений. Баланс не списан."
        )
        return

    await message.reply_text(f"🎨 Генерирую изображения... (0/{images_count})")
    generated: list[dict[str, Any]] = []
    tasks = [
        _generate_and_send_single_image(
            message=message,
            context=context,
            concept=concept,
            photo_file_ids=photo_file_ids,
            settings=settings,
        )
        for concept in concepts
    ]
    completed = 0
    for task in as_completed(tasks):
        completed += 1
        try:
            image_record = await task
        except Exception:
            logging.exception("Single image generation failed")
            await message.reply_text(
                f"Изображение {completed}/{images_count} не удалось сгенерировать."
            )
            continue
        generated.append(image_record)
        await message.reply_text(f"Готово {completed}/{images_count}")

    try:
        image_balance = await db.save_generated_images_and_consume_balance(
            session_id=session_id,
            user_id=user_id,
            generated_images=generated,
        )
    except Exception:
        logging.exception("Failed to save generated images")
        await db.set_image_session_status(session_id, "failed")
        await message.reply_text(
            "Изображения отправлены, но не удалось сохранить историю. Баланс не списан."
        )
        return

    await message.reply_text(
        f"✅ Готово! Сгенерировано {len(generated)} изображений для карточки.\n"
        f"Остаток: {image_balance} изображений",
        reply_markup=build_after_image_generation_keyboard(),
    )
    _clear_image_session(context)


def _serialize_image_concepts(concepts: list[ImageConcept]) -> str:
    import json

    return json.dumps(
        {
            "concepts": [
                {
                    "image_index": concept.image_index,
                    "purpose": concept.purpose,
                    "photo_index": concept.photo_index,
                    "prompt": concept.prompt,
                }
                for concept in concepts
            ]
        },
        ensure_ascii=False,
    )


async def _generate_and_send_single_image(
    message: Any,
    context: Any,
    concept: ImageConcept,
    photo_file_ids: list[str],
    settings: Settings,
) -> dict[str, Any]:
    photo_index = min(concept.photo_index, len(photo_file_ids) - 1)
    image_bytes = await generate_marketplace_image(
        prompt=concept.prompt,
        reference_photo_file_id=photo_file_ids[photo_index],
        bot=context.bot,
        api_key=settings.openrouter_api_key,
        model=settings.gpt_image_model,
        site_url=settings.site_url,
    )
    buffer = BytesIO(image_bytes)
    buffer.name = f"cardbot-image-{concept.image_index}.png"
    sent_message = await message.reply_photo(
        photo=buffer,
        caption=f"Изображение {concept.image_index}: {concept.purpose}",
    )
    telegram_file_id = ""
    if getattr(sent_message, "photo", None):
        telegram_file_id = sent_message.photo[-1].file_id
    return {
        "image_index": concept.image_index,
        "prompt_used": concept.prompt,
        "telegram_file_id": telegram_file_id,
    }


async def handle_text(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None or update.effective_message is None:
        return

    user_input = (update.effective_message.text or "").strip()
    if await _handle_image_description(update, context, user_input):
        return

    if len(user_input) < 3:
        await update.effective_message.reply_text(
            "Добавьте хотя бы название или категорию товара."
        )
        return

    marketplace = context.user_data.get("marketplace")
    if not marketplace:
        await update.effective_message.reply_text(
            MARKETPLACE_PROMPT,
            reply_markup=build_marketplace_keyboard(),
        )
        return

    settings = _get_settings(context)
    db = _get_db(context)
    usage_mode = await db.get_usage_mode(
        user_id, trial_generations=settings.trial_generations
    )
    if usage_mode is UsageMode.BLOCKED:
        await update.effective_message.reply_text(
            "Бесплатные генерации закончились.",
            reply_markup=build_buy_keyboard(),
        )
        return

    await update.effective_message.reply_text("⏳ Генерирую карточку...")

    try:
        card = await generate_card(
            user_input,
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            site_url=settings.site_url,
            marketplace=marketplace,
        )
    except Exception:
        logging.exception("LLM generation failed")
        await update.effective_message.reply_text(
            "Произошла ошибка, попробуйте ещё раз. Генерация не списана."
        )
        return

    try:
        await db.save_successful_generation(
            user_id,
            user_input,
            card,
            usage_mode,
            trial_generations=settings.trial_generations,
        )
    except Exception:
        logging.exception("Failed to save generation")
        await update.effective_message.reply_text(
            "Карточка создана, но не удалось сохранить историю. Попробуйте позже."
        )
        return

    messages = build_generation_messages(card)
    for text in messages[:-1]:
        await update.effective_message.reply_text(text)
    await update.effective_message.reply_text(
        messages[-1],
        reply_markup=build_after_generation_keyboard(),
    )
    context.user_data.pop("marketplace", None)


async def handle_callback(update: Any, context: Any) -> None:
    query = update.callback_query
    await query.answer()
    await _ensure_user(update, context)

    data = query.data or ""
    if data == "action:generate":
        context.user_data.pop("marketplace", None)
        await query.message.reply_text(
            MARKETPLACE_PROMPT,
            reply_markup=build_marketplace_keyboard(),
        )
    elif data == "action:images":
        user = update.effective_user
        if user is not None:
            await _start_image_flow(query.message, context, user.id)
    elif data.startswith("marketplace:"):
        try:
            context.user_data["marketplace"] = normalize_marketplace(data.split(":", 1)[1])
        except Exception:
            await query.message.reply_text(
                MARKETPLACE_PROMPT,
                reply_markup=build_marketplace_keyboard(),
            )
            return
        await query.message.reply_text(GENERATE_PROMPT)
    elif data.startswith("img_marketplace:"):
        try:
            context.user_data["img_marketplace"] = normalize_marketplace(data.split(":", 1)[1])
        except Exception:
            await query.message.reply_text(
                MARKETPLACE_PROMPT,
                reply_markup=build_image_marketplace_keyboard(),
            )
            return
        context.user_data["img_waiting_description"] = True
        await query.message.reply_text(IMAGE_DESCRIPTION_PROMPT)
    elif data == "img_add_more":
        await query.message.reply_text(IMAGE_PHOTO_PROMPT)
    elif data == "img_photos_done":
        photos = list(context.user_data.get("img_photos") or [])
        if not photos:
            await query.message.reply_text(IMAGE_PHOTO_PROMPT)
            return
        context.user_data["img_waiting_photos"] = False
        await query.message.reply_text(
            IMAGE_COUNT_PROMPT,
            reply_markup=build_image_count_keyboard(),
        )
    elif data.startswith("img_count:"):
        user = update.effective_user
        if user is None:
            return
        try:
            images_count = int(data.split(":", 1)[1])
        except ValueError:
            await query.message.reply_text(
                IMAGE_COUNT_PROMPT,
                reply_markup=build_image_count_keyboard(),
            )
            return
        if images_count < 1 or images_count > 9:
            await query.message.reply_text(
                IMAGE_COUNT_PROMPT,
                reply_markup=build_image_count_keyboard(),
            )
            return
        context.user_data["img_count"] = images_count
        await _generate_images_for_user(update, context, user.id, images_count)
    elif data == "action:balance":
        await balance_command(update, context)
    elif data == "action:history":
        await history_command(update, context)
    elif data == "action:help":
        await query.message.reply_text(build_help_message(), reply_markup=build_main_menu())
    elif data in {"action:buy", "action:buy_images"} or data.startswith(("buy:", "img_buy:")):
        await query.message.reply_text(
            PAYMENT_UNAVAILABLE_MESSAGE,
            reply_markup=build_image_packages_keyboard() if data.startswith("img_buy:") or data == "action:buy_images" else build_buy_keyboard(),
        )


async def post_init(application: Any) -> None:
    db: Database = application.bot_data["db"]
    await db.connect()
    await db.init_db()
    await application.bot.set_my_commands(
        [
            ("start", "Главное меню"),
            ("generate", "Сгенерировать карточку"),
            ("images", "Создать изображения карточки"),
            ("balance", "Показать баланс"),
            ("history", "Последние 5 генераций"),
            ("buy", "Купить генерации"),
            ("help", "Помощь"),
        ]
    )


async def post_shutdown(application: Any) -> None:
    await application.bot_data["db"].close()


def create_application(settings: Settings) -> Any:
    from telegram.ext import (
        ApplicationBuilder,
        CallbackQueryHandler,
        CommandHandler,
        MessageHandler,
        filters,
    )

    application = (
        ApplicationBuilder()
        .token(settings.bot_token)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )
    application.bot_data["settings"] = settings
    application.bot_data["db"] = Database(settings.cardbot_db_url)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate_command))
    application.add_handler(CommandHandler("images", images_command))
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("buy", buy_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    return application


def main() -> None:
    logging.basicConfig(
        filename="cardbot.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    settings = load_settings()
    application = create_application(settings)
    application.run_polling()


if __name__ == "__main__":
    main()
