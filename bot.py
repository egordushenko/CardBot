from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from config import Settings, load_settings
from db import PACKAGES, Database, UsageMode
from llm import CardGeneration, generate_card, normalize_marketplace


PAYMENT_UNAVAILABLE_MESSAGE = "💳 Оплата временно недоступна, скоро откроем!"
GENERATE_PROMPT = (
    "Отправьте описание товара. Минимум — название. "
    "Можно добавить материал, размер, цвет и особенности."
)
MARKETPLACE_PROMPT = "Выберите маркетплейс:"


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


def build_marketplace_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("Wildberries", "marketplace:wb"),
                _button("Ozon", "marketplace:ozon"),
            ]
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


def build_generation_messages(card: CardGeneration) -> list[str]:
    search_label = "🔖 ХЭШТЕГИ" if card.marketplace == "ozon" else "🔑 КЛЮЧЕВЫЕ СЛОВА"
    return [
        f"📌 НАЗВАНИЕ:\n{card.title}",
        f"📝 ОПИСАНИЕ:\n{card.description}",
        f"{search_label}:\n{card.keywords}",
        f"📋 ХАРАКТЕРИСТИКИ:\n{card.characteristics}",
    ]


def build_balance_message(trial_used: int, balance: int, trial_generations: int = 3) -> str:
    free_left = max(trial_generations - trial_used, 0)
    return (
        "📊 Ваш баланс\n\n"
        f"Бесплатно осталось: {free_left}\n"
        f"Платных генераций: {balance}"
    )


def build_help_message() -> str:
    return (
        "CardBot генерирует SEO-карточки товаров для Wildberries и Ozon.\n\n"
        "Просто отправьте описание товара одним сообщением. "
        "Бот вернёт название, описание, ключевые слова и характеристики.\n\n"
        "/generate — создать карточку\n"
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


async def handle_text(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None or update.effective_message is None:
        return

    user_input = (update.effective_message.text or "").strip()
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
    elif data == "action:balance":
        await balance_command(update, context)
    elif data == "action:history":
        await history_command(update, context)
    elif data == "action:help":
        await query.message.reply_text(build_help_message(), reply_markup=build_main_menu())
    elif data == "action:buy" or data.startswith("buy:"):
        await query.message.reply_text(
            PAYMENT_UNAVAILABLE_MESSAGE,
            reply_markup=build_buy_keyboard(),
        )


async def post_init(application: Any) -> None:
    db: Database = application.bot_data["db"]
    await db.connect()
    await db.init_db()
    await application.bot.set_my_commands(
        [
            ("start", "Главное меню"),
            ("generate", "Сгенерировать карточку"),
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
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("buy", buy_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
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
