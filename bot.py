from __future__ import annotations

import logging
import asyncio
import json
from contextlib import suppress
from io import BytesIO
from dataclasses import dataclass
from typing import Any

from config import Settings, load_settings
from db import Database, UsageMode
from image_generator import generate_marketplace_image
from llm import CardGeneration, ImageConcept, generate_card, generate_image_prompts, normalize_marketplace
from payments import (
    IMAGE_ADDON_CODES,
    MAIN_PACKAGE_CODES,
    PACKAGES as PAYMENT_PACKAGES,
    PROMO_PACKAGE_CODE,
    TEXT_ADDON_CODES,
    build_payment_url,
    calculate_package_counts,
    generate_inv_id,
)
from webhook_server import start_webhook_server


PAYMENT_UNAVAILABLE_MESSAGE = "💳 Оплата временно недоступна, скоро откроем!"
GENERATE_PROMPT = (
    "Отправьте описание товара. Минимум — название. "
    "Можно добавить материал, размер, цвет и особенности."
)
MARKETPLACE_PROMPT = "Выберите маркетплейс:"
MODE_PROMPT = (
    "Что сгенерировать?\n\n"
    "«Только текст» — название, описание, ключевые слова, характеристики. Тратит 1 текстовую генерацию.\n"
    "«Текст + изображения» — всё выше плюс изображения для карточки. Тратит 1 текстовую генерацию + N изображений."
)
IMAGE_DESCRIPTION_PROMPT = (
    "Опишите товар: название, материал, размер, цвет, ключевые преимущества. "
    "Чем подробнее — тем лучше результат. После этого бот попросит загрузить фото товара."
)
IMAGE_PHOTO_PROMPT = (
    "Загрузите от 1 до 5 фото товара с разных ракурсов. "
    "Когда загрузите все — нажмите ✅ Готово"
)
TEMPLATE_NAME_PROMPT = (
    "Введите название шаблона.\n"
    "Например: \"Лампа спиральная\" или \"Коврик ЭВА\""
)
REPEAT_CHANGES_PROMPT = (
    "Напишите только что изменилось.\n"
    "Например: \"цвет чёрный\" или \"размер XL, вес 2 кг\"\n\n"
    "Всё остальное останется как в предыдущей карточке."
)
REPEAT_PHOTOS_PROMPT = "Использовать те же фото или загрузить новые?"
TEMPLATES_PAGE_SIZE = 5
TEMPLATES_LIMIT = 10


@dataclass(frozen=True)
class KeyboardButton:
    text: str
    callback_data: str
    url: str | None = None


@dataclass(frozen=True)
class KeyboardMarkup:
    inline_keyboard: list[list[KeyboardButton]]


def _button(text: str, callback_data: str) -> Any:
    try:
        from telegram import InlineKeyboardButton

        return InlineKeyboardButton(text, callback_data=callback_data)
    except ImportError:
        return KeyboardButton(text=text, callback_data=callback_data)


def _url_button(text: str, url: str) -> Any:
    try:
        from telegram import InlineKeyboardButton

        return InlineKeyboardButton(text, url=url)
    except ImportError:
        return KeyboardButton(text=text, callback_data="", url=url)


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
                _button("📋 Мои шаблоны", "action:templates"),
                _button("📋 История", "action:history"),
            ],
            [
                _button("❓ Помощь", "action:help"),
            ],
        ]
    )


def _payment_button(package_code: str) -> Any:
    package = PAYMENT_PACKAGES[package_code]
    if package_code.startswith("addon_text_"):
        label = f"{package.text_count} карточек за {package.price_rub:,} ₽"
    elif package_code.startswith("addon_img_") or package_code == "promo_img_10":
        label = f"{package.images_count} изображений за {package.price_rub:,} ₽"
    else:
        label = f"{package.title} — {package.description} за {package.price_rub:,} ₽"
    return _button(
        label.replace(",", " "),
        f"buy:{package_code}",
    )


def _combo_package_code(text_count: int, images_per_card: int) -> str:
    for code in MAIN_PACKAGE_CODES:
        package = PAYMENT_PACKAGES[code]
        if package.text_count == text_count and package.images_per_card == images_per_card:
            return code
    raise ValueError(f"Unknown combo package: {text_count=} {images_per_card=}")


def _combo_payment_button(text_count: int, images_per_card: int) -> Any:
    code = _combo_package_code(text_count, images_per_card)
    package = PAYMENT_PACKAGES[code]
    if images_per_card == 0:
        label = f"Без фото — {package.price_rub:,} ₽"
    else:
        label = f"{images_per_card} фото/карточка — {package.price_rub:,} ₽"
    return _button(label.replace(",", " "), f"buy:{code}")


def build_buy_keyboard(show_first_image_promo: bool = False) -> Any:
    return _keyboard(
        [
            [_button("Комбо: карточки + изображения", "action:buy_combo")],
            [_button("Только карточки", "action:buy_text")],
            [_button("Только изображения", "action:buy_images")],
        ]
    )


def build_combined_buy_keyboard(show_first_image_promo: bool = False) -> Any:
    return build_buy_keyboard(show_first_image_promo=show_first_image_promo)


def build_combo_card_count_keyboard() -> Any:
    counts = sorted({PAYMENT_PACKAGES[code].text_count for code in MAIN_PACKAGE_CODES})
    rows = [[_button(f"{count} карточек", f"combo_cards:{count}")] for count in counts]
    rows.append([_button("⬅️ Назад", "buy_back:root")])
    return _keyboard(rows)


def build_combo_photo_count_keyboard(text_count: int) -> Any:
    photo_counts = sorted(
        PAYMENT_PACKAGES[code].images_per_card
        for code in MAIN_PACKAGE_CODES
        if PAYMENT_PACKAGES[code].text_count == text_count
    )
    rows = [[_combo_payment_button(text_count, photo_count)] for photo_count in photo_counts]
    rows.append([_button("⬅️ Назад", "buy_back:combo")])
    return _keyboard(rows)


def build_balance_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("💳 Купить текстовые", "action:buy_text"),
                _button("💳 Купить изображения", "action:buy_images"),
            ]
        ]
    )


def build_image_packages_keyboard(show_first_image_promo: bool = False) -> Any:
    rows = [[_payment_button(code)] for code in IMAGE_ADDON_CODES]
    if show_first_image_promo:
        rows.insert(0, [_payment_button(PROMO_PACKAGE_CODE)])
    return _keyboard(rows)


def build_text_packages_keyboard() -> Any:
    return _keyboard([[_payment_button(code)] for code in TEXT_ADDON_CODES])


def build_payment_link_keyboard(payment_url: str) -> Any:
    return _keyboard([[_url_button("Перейти к оплате", payment_url)]])


def build_marketplace_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("Wildberries", "marketplace:wb"),
                _button("Ozon", "marketplace:ozon"),
            ]
        ]
    )


def build_generation_mode_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("📝 Только текст", "mode:text_only"),
                _button("📝🖼 Текст + изображения", "mode:text_and_images"),
            ]
        ]
    )


def build_no_image_balance_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("💳 Купить изображения", "action:buy_images"),
                _button("📝 Только текст", "mode:text_only"),
            ]
        ]
    )


def build_payment_stub_keyboard(data: str) -> Any:
    if data == "action:buy_images" or data.startswith("img_buy:"):
        return build_image_packages_keyboard()
    if data == "action:buy_text" or data.startswith("buy:"):
        return build_buy_keyboard()
    return build_combined_buy_keyboard()


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


def is_supported_image_document(document: Any) -> bool:
    mime_type = str(getattr(document, "mime_type", "") or "").lower()
    return mime_type.startswith("image/")


def extract_image_file_id(message: Any) -> str | None:
    photos = list(getattr(message, "photo", None) or [])
    if photos:
        return photos[-1].file_id

    document = getattr(message, "document", None)
    if is_supported_image_document(document):
        return document.file_id

    return None


def build_photo_received_message(added_count: int, total_count: int) -> str:
    return f"Фото {added_count} получено ✓\nВсего: {total_count}/5"


def build_image_progress_message(
    total_count: int,
    generated_count: int,
    sent_count: int,
    *,
    still_working: bool = False,
) -> str:
    suffix = "\nЗапрос еще выполняется, это может занять пару минут." if still_working else ""
    return (
        "🎨 Генерирую изображения...\n"
        f"Сгенерировано: {generated_count}/{total_count}\n"
        f"Отправлено: {sent_count}/{total_count}"
        f"{suffix}"
    )


def build_image_count_keyboard(image_balance: int | None = None) -> Any:
    counts = [1, 3, 5, 7, 9]
    if image_balance is not None:
        counts = [count for count in counts if count <= image_balance]
    if not counts:
        return _keyboard([[_button("💳 Купить изображения", "action:buy_images")]])
    rows = [[_button(str(count), f"img_count:{count}") for count in counts[:3]]]
    if len(counts) > 3:
        rows.append([_button(str(count), f"img_count:{count}") for count in counts[3:]])
    return _keyboard(rows)


def build_image_count_prompt(image_balance: int) -> str:
    return (
        "Сколько изображений сгенерировать?\n\n"
        f"На вашем балансе: {image_balance} изображений"
    )


def build_after_generation_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("🔄 Сгенерировать ещё", "action:generate"),
                _button("💾 Сохранить как шаблон", "action:save_template"),
            ],
            [
                _button("🔄 Изменить и повторить", "action:repeat_edit"),
                _button("💳 Пополнить баланс", "action:buy"),
            ],
        ]
    )


def build_after_image_generation_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("⚡ Сгенерировать ещё", "action:generate"),
                _button("💾 Сохранить как шаблон", "action:save_template"),
            ],
            [
                _button("🔄 Изменить и повторить", "action:repeat_edit"),
                _button("💳 Пополнить баланс", "action:buy_images"),
            ],
        ]
    )


def truncate_template_name(name: str) -> str:
    return (name or "").strip()[:50] or "Шаблон"


def combine_repeat_description(previous_description: str, user_changes: str) -> str:
    return f"{previous_description.strip()}\n\nИзменения: {user_changes.strip()}"


def format_marketplace(marketplace: str) -> str:
    return "Wildberries" if marketplace == "wb" else "Ozon"


def format_template_mode(mode: str) -> str:
    return "Текст + изображения" if mode == "text_and_images" else "Только текст"


def format_template_description_preview(description: str, limit: int = 100) -> str:
    normalized = " ".join((description or "").split())
    if len(normalized) <= limit:
        return normalized
    return normalized[:limit] + "..."


def build_repeat_photos_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("📎 Те же фото", "repeat:same_photos"),
                _button("🖼 Загрузить новые", "repeat:new_photos"),
            ]
        ]
    )


def build_templates_keyboard(
    templates: list[dict[str, Any]],
    page: int,
    total: int,
) -> Any:
    rows = [[_button(template["name"], f"template_use:{template['id']}")] for template in templates]
    nav_row: list[Any] = []
    if page > 0:
        nav_row.append(_button("← Назад", f"templates_page:{page - 1}"))
    if (page + 1) * TEMPLATES_PAGE_SIZE < total:
        nav_row.append(_button("Вперёд →", f"templates_page:{page + 1}"))
    if nav_row:
        rows.append(nav_row)
    rows.append([_button("🗑 Удалить шаблон", f"templates_delete:{page}")])
    return _keyboard(rows)


def build_templates_delete_keyboard(
    templates: list[dict[str, Any]],
    page: int,
    total: int,
) -> Any:
    rows = [[_button(template["name"], f"template_delete:{template['id']}")] for template in templates]
    nav_row: list[Any] = []
    if page > 0:
        nav_row.append(_button("← Назад", f"templates_delete:{page - 1}"))
    if (page + 1) * TEMPLATES_PAGE_SIZE < total:
        nav_row.append(_button("Вперёд →", f"templates_delete:{page + 1}"))
    if nav_row:
        rows.append(nav_row)
    rows.append([_button("❌ Отмена", f"templates_page:{page}")])
    return _keyboard(rows)


def build_template_details_keyboard(template_id: int) -> Any:
    return _keyboard(
        [
            [_button("⚡ Использовать как есть", f"template_run:{template_id}")],
            [_button("✏️ Изменить и использовать", f"template_edit:{template_id}")],
            [_button("🗑 Удалить шаблон", f"template_delete:{template_id}")],
        ]
    )


def build_template_delete_confirm_keyboard(template_id: int) -> Any:
    return _keyboard(
        [
            [
                _button("✅ Да, удалить", f"template_delete_confirm:{template_id}"),
                _button("❌ Отмена", f"template_delete_cancel:{template_id}"),
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
    text_balance = free_left + balance
    return (
        "📊 Ваш баланс:\n\n"
        f"📝 Текстовых генераций: {text_balance}\n"
        f"🖼 Изображений: {image_balance}"
    )


def build_help_message() -> str:
    return (
        "CardBot генерирует SEO-карточки товаров для Wildberries и Ozon.\n\n"
        "Просто отправьте описание товара одним сообщением. "
        "Бот вернёт название, описание, ключевые слова и характеристики.\n\n"
        "Контакт для вопросов по оплате и работе сервиса: alterega@list.ru\n"
        "Условия оказания услуги: публичная оферта.\n\n"
        "/generate — создать карточку\n"
        "/balance — баланс\n"
        "/templates — мои шаблоны\n"
        "/history — последние генерации\n"
        "/buy — пакеты генераций"
    )


def build_help_keyboard(offer_url: str) -> Any:
    return _keyboard([[_url_button("Публичная оферта", offer_url)]])


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
        "mode",
        "generation_step",
        "marketplace",
        "img_marketplace",
        "img_description",
        "img_photos",
        "img_count",
        "img_media_groups",
        "repeat_pending_generation",
        "repeat_mode",
        "repeat_images_count",
    ):
        context.user_data.pop(key, None)


def _store_last_generation(
    context: Any,
    *,
    marketplace: str,
    mode: str,
    description: str,
    photo_file_ids: list[str] | None = None,
    images_count: int | None = None,
) -> None:
    context.user_data["last_generation"] = {
        "marketplace": marketplace,
        "mode": mode,
        "description": description,
        "photo_file_ids": list(photo_file_ids or []),
        "images_count": images_count,
    }


def _template_to_last_generation(template: dict[str, Any]) -> dict[str, Any]:
    return {
        "marketplace": template["marketplace"],
        "mode": template["mode"],
        "description": template["description"],
        "photo_file_ids": _parse_photo_file_ids(template.get("photo_file_ids")),
        "images_count": template.get("images_count"),
    }


def _parse_photo_file_ids(raw_value: Any) -> list[str]:
    if not raw_value:
        return []
    if isinstance(raw_value, list):
        return [str(value) for value in raw_value]
    try:
        value = json.loads(str(raw_value))
    except json.JSONDecodeError:
        return []
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


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
    _clear_image_session(context)
    context.user_data["generation_step"] = "marketplace"
    await update.effective_message.reply_text(
        MARKETPLACE_PROMPT,
        reply_markup=build_marketplace_keyboard(),
    )


async def images_command(update: Any, context: Any) -> None:
    await generate_command(update, context)


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
        ),
        reply_markup=build_balance_keyboard(),
    )


async def buy_command(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None:
        return
    await _show_buy_menu(update.effective_message, context, user_id, kind="all")


async def _show_buy_menu(message: Any, context: Any, user_id: int, kind: str = "all") -> None:
    first_image_purchase = await _get_db(context).is_first_image_purchase(user_id)
    if kind == "combo":
        await message.reply_text(
            "Сколько карточек нужно в комбо-пакете?",
            reply_markup=build_combo_card_count_keyboard(),
        )
        return
    if kind == "text":
        await message.reply_text(
            "Выберите пакет текстовых карточек:",
            reply_markup=build_text_packages_keyboard(),
        )
        return
    if kind == "images":
        await message.reply_text(
            "Выберите пакет изображений:",
            reply_markup=build_image_packages_keyboard(show_first_image_promo=first_image_purchase),
        )
        return
    await message.reply_text(
        "Что хотите купить?",
        reply_markup=build_combined_buy_keyboard(show_first_image_promo=first_image_purchase),
    )


async def _send_payment_link(message: Any, context: Any, user_id: int, package_code: str) -> None:
    if package_code not in PAYMENT_PACKAGES:
        await message.reply_text("Пакет не найден. Откройте /buy и выберите пакет заново.")
        return

    db = _get_db(context)
    if package_code == PROMO_PACKAGE_CODE and not await db.is_first_image_purchase(user_id):
        await message.reply_text("Акция первой покупки уже использована.")
        return

    settings = _get_settings(context)
    if not settings.robokassa_login or not settings.robokassa_password1:
        await message.reply_text(PAYMENT_UNAVAILABLE_MESSAGE)
        return

    package = PAYMENT_PACKAGES[package_code]
    text_count, images_count = calculate_package_counts(package_code)
    inv_id = generate_inv_id()
    await db.create_pending_payment(
        inv_id=inv_id,
        user_id=user_id,
        package_code=package_code,
        amount_rub=package.price_rub,
        text_count=text_count,
        images_count=images_count,
    )
    payment_url = build_payment_url(
        settings=settings,
        inv_id=inv_id,
        user_id=user_id,
        package_code=package_code,
    )
    await message.reply_text(
        f"💳 Оплата пакета \"{package.title}\"\n"
        f"Сумма: {package.price_rub:,} ₽\n\n"
        f"После оплаты баланс пополнится автоматически.".replace(",", " "),
        reply_markup=build_payment_link_keyboard(payment_url),
    )


async def help_command(update: Any, context: Any) -> None:
    await _ensure_user(update, context)
    settings = _get_settings(context)
    await update.effective_message.reply_text(
        build_help_message(),
        reply_markup=build_help_keyboard(settings.cardbot_offer_url),
    )


async def templates_command(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None:
        return
    await _show_templates(update.effective_message, context, user_id, page=0)


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


async def _show_templates(message: Any, context: Any, user_id: int, page: int = 0) -> None:
    page = max(page, 0)
    db = _get_db(context)
    total = await db.get_templates_count(user_id)
    templates = await db.get_templates(
        user_id,
        offset=page * TEMPLATES_PAGE_SIZE,
        limit=TEMPLATES_PAGE_SIZE,
    )
    context.user_data["template_page"] = page
    if not templates:
        await message.reply_text("📋 У вас пока нет шаблонов.")
        return

    lines = [f"📋 Ваши шаблоны ({total} из {TEMPLATES_LIMIT}):", ""]
    for index, template in enumerate(templates, start=page * TEMPLATES_PAGE_SIZE + 1):
        marketplace = format_marketplace(template["marketplace"])
        mode = format_template_mode(template["mode"]).lower()
        lines.append(f"{index}. {template['name']} ({marketplace}, {mode})")
    await message.reply_text(
        "\n".join(lines),
        reply_markup=build_templates_keyboard(templates, page=page, total=total),
    )


async def _show_templates_delete_list(message: Any, context: Any, user_id: int, page: int = 0) -> None:
    page = max(page, 0)
    db = _get_db(context)
    total = await db.get_templates_count(user_id)
    templates = await db.get_templates(
        user_id,
        offset=page * TEMPLATES_PAGE_SIZE,
        limit=TEMPLATES_PAGE_SIZE,
    )
    if not templates:
        await message.reply_text("📋 У вас пока нет шаблонов.")
        return

    await message.reply_text(
        "Выберите шаблон для удаления:",
        reply_markup=build_templates_delete_keyboard(templates, page=page, total=total),
    )


def build_template_details_message(template: dict[str, Any]) -> str:
    return (
        f"📋 Шаблон: \"{template['name']}\"\n"
        f"Маркетплейс: {format_marketplace(template['marketplace'])}\n"
        f"Режим: {format_template_mode(template['mode'])}\n"
        f"Описание: {format_template_description_preview(template['description'])}\n\n"
        "Что сделать?"
    )


async def _start_image_flow(message: Any, context: Any, user_id: int) -> None:
    _clear_image_session(context)
    context.user_data["generation_step"] = "marketplace"
    await message.reply_text(
        MARKETPLACE_PROMPT,
        reply_markup=build_marketplace_keyboard(),
    )


async def _handle_image_description(update: Any, context: Any, user_input: str) -> bool:
    if context.user_data.get("generation_step") != "description":
        return False
    if context.user_data.get("mode") != "text_and_images":
        return False

    if len(user_input) < 3:
        await update.effective_message.reply_text(
            "Добавьте хотя бы название или категорию товара."
        )
        return True

    context.user_data["img_description"] = user_input
    context.user_data["generation_step"] = "photos"
    context.user_data["img_photos"] = []
    await update.effective_message.reply_text(IMAGE_PHOTO_PROMPT)
    return True


async def handle_photo(update: Any, context: Any) -> None:
    await _handle_image_upload(update, context)


async def handle_document(update: Any, context: Any) -> None:
    await _handle_image_upload(update, context)


async def _handle_image_upload(update: Any, context: Any) -> None:
    await _ensure_user(update, context)
    if context.user_data.get("generation_step") != "photos":
        return

    message = update.effective_message
    photos = list(context.user_data.get("img_photos") or [])
    if len(photos) >= 5:
        await message.reply_text(
            "Максимум 5 фото. Нажмите ✅ Готово",
            reply_markup=build_image_photo_keyboard(len(photos)),
        )
        return

    file_id = extract_image_file_id(message)
    if not file_id:
        await message.reply_text(
            "Пришлите фото товара или изображение файлом.",
            reply_markup=build_image_photo_keyboard(len(photos)),
        )
        return

    photos.append(file_id)
    context.user_data["img_photos"] = photos

    media_group_id = getattr(message, "media_group_id", None)
    if media_group_id:
        _schedule_media_group_ack(
            context=context,
            chat_id=message.chat_id,
            media_group_id=str(media_group_id),
            total_count=len(photos),
        )
        return

    await message.reply_text(
        build_photo_received_message(added_count=1, total_count=len(photos)),
        reply_markup=build_image_photo_keyboard(len(photos)),
    )


def _schedule_media_group_ack(context: Any, chat_id: int, media_group_id: str, total_count: int) -> None:
    groups = context.user_data.setdefault("img_media_groups", {})
    group = groups.setdefault(
        media_group_id,
        {
            "added_count": 0,
            "chat_id": chat_id,
            "total_count": total_count,
            "scheduled": False,
        },
    )
    group["added_count"] += 1
    group["total_count"] = total_count
    if group["scheduled"]:
        return

    group["scheduled"] = True
    context.application.create_task(_flush_media_group_ack(context, media_group_id))


async def _flush_media_group_ack(context: Any, media_group_id: str) -> None:
    await asyncio.sleep(1.2)
    group = (context.user_data.get("img_media_groups") or {}).pop(media_group_id, None)
    if not group:
        return

    total_count = int(group["total_count"])
    await context.bot.send_message(
        chat_id=group["chat_id"],
        text=build_photo_received_message(
            added_count=int(group["added_count"]),
            total_count=total_count,
        ),
        reply_markup=build_image_photo_keyboard(total_count),
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
    marketplace = context.user_data.get("marketplace") or context.user_data.get("img_marketplace")
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

    generated = await _generate_and_send_image_concepts(
        message=message,
        context=context,
        concepts=concepts,
        photo_file_ids=photo_file_ids,
        settings=settings,
    )

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


async def _generate_text_and_images_for_user(
    update: Any,
    context: Any,
    user_id: int,
    images_count: int,
) -> None:
    message = update.callback_query.message
    settings = _get_settings(context)
    db = _get_db(context)
    marketplace = context.user_data.get("marketplace")
    product_description = context.user_data.get("img_description")
    photo_file_ids = list(context.user_data.get("img_photos") or [])

    if not marketplace or not product_description or not photo_file_ids:
        await message.reply_text(
            "Сессия генерации устарела. Начните заново.",
            reply_markup=build_after_image_generation_keyboard(),
        )
        _clear_image_session(context)
        return

    usage_mode = await db.get_usage_mode(user_id, trial_generations=settings.trial_generations)
    if usage_mode is UsageMode.BLOCKED:
        await message.reply_text(
            "Бесплатные генерации закончились.",
            reply_markup=build_buy_keyboard(),
        )
        return

    current_image_balance = await db.get_image_balance(user_id)
    if current_image_balance < images_count:
        await message.reply_text(
            f"Не хватает {images_count - current_image_balance} изображений на балансе.",
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

    await message.reply_text("⏳ Генерирую карточку...")
    card_task = asyncio.create_task(
        generate_card(
            product_description,
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            site_url=settings.site_url,
            marketplace=marketplace,
        )
    )
    concepts_task = asyncio.create_task(
        generate_image_prompts(
            product_description=product_description,
            marketplace=marketplace,
            photos_count=len(photo_file_ids),
            images_count=images_count,
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            site_url=settings.site_url,
        )
    )

    try:
        card = await card_task
    except Exception:
        await _cancel_task(concepts_task)
        await db.set_image_session_status(session_id, "failed")
        logging.exception("LLM generation failed")
        await message.reply_text(
            "Произошла ошибка, попробуйте ещё раз. Генерация не списана."
        )
        return

    try:
        await db.save_successful_generation(
            user_id,
            product_description,
            card,
            usage_mode,
            trial_generations=settings.trial_generations,
        )
    except Exception:
        await _cancel_task(concepts_task)
        await db.set_image_session_status(session_id, "failed")
        logging.exception("Failed to save generation")
        await message.reply_text(
            "Карточка создана, но не удалось сохранить историю. Баланс изображений не списан."
        )
        return

    await message.reply_text("✅ Текстовая карточка готова:")
    for text in build_generation_messages(card):
        await message.reply_text(text)
    await message.reply_text("🖼 Изображения генерируются... подождите ~1-2 минуты")

    try:
        concepts = await concepts_task
        await db.update_image_session_prompts(
            session_id,
            _serialize_image_concepts(concepts),
            status="generating",
        )
    except Exception:
        logging.exception("Image prompt generation failed")
        await db.set_image_session_status(session_id, "failed")
        balance = await db.get_balance(user_id)
        text_left = max(settings.trial_generations - balance.trial_used, 0) + balance.balance
        await message.reply_text(
            "Не удалось разработать концепцию изображений. Списана только текстовая генерация.\n"
            f"Остаток: {text_left} текстовых / {balance.image_balance} изображений",
            reply_markup=build_after_image_generation_keyboard(),
        )
        _clear_image_session(context)
        return

    generated = await _generate_and_send_image_concepts(
        message=message,
        context=context,
        concepts=concepts,
        photo_file_ids=photo_file_ids,
        settings=settings,
    )

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
            "Изображения отправлены, но не удалось сохранить историю. Баланс изображений не списан."
        )
        return

    balance = await db.get_balance(user_id)
    text_left = max(settings.trial_generations - balance.trial_used, 0) + balance.balance
    await message.reply_text(
        f"✅ Все изображения готовы!\n"
        f"Потрачено: 1 текстовая генерация + {len(generated)} изображений\n"
        f"Остаток: {text_left} текстовых / {image_balance} изображений",
        reply_markup=build_after_image_generation_keyboard(),
    )
    _store_last_generation(
        context,
        marketplace=marketplace,
        mode="text_and_images",
        description=product_description,
        photo_file_ids=photo_file_ids,
        images_count=images_count,
    )
    _clear_image_session(context)


async def _cancel_task(task: asyncio.Task[Any]) -> None:
    if task.done():
        with suppress(Exception):
            task.result()
        return
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


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


async def _generate_and_send_image_concepts(
    message: Any,
    context: Any,
    concepts: list[ImageConcept],
    photo_file_ids: list[str],
    settings: Settings,
) -> list[dict[str, Any]]:
    total_count = len(concepts)
    status_message = await message.reply_text(build_image_progress_message(total_count, 0, 0))
    generated: list[dict[str, Any]] = []
    tasks = [
        _generate_single_image_result(
            context=context,
            concept=concept,
            photo_file_ids=photo_file_ids,
            settings=settings,
        )
        for concept in concepts
    ]
    generated_count = 0
    sent_count = 0
    next_to_send = 1
    ready: dict[int, dict[str, Any]] = {}
    failed: set[int] = set()
    stop_progress = asyncio.Event()
    progress_task = asyncio.create_task(
        _image_generation_heartbeat(
            status_message=status_message,
            total_count=total_count,
            get_counts=lambda: (generated_count, sent_count),
            stop_event=stop_progress,
        )
    )

    try:
        for task in asyncio.as_completed(tasks):
            result = await task
            generated_count += 1
            image_index = int(result["image_index"])

            if result.get("ok"):
                ready[image_index] = result
            else:
                failed.add(image_index)
                logging.warning("Image %s generation failed: %s", image_index, result.get("error"))

            while next_to_send in ready or next_to_send in failed:
                if next_to_send in failed:
                    await message.reply_text(
                        f"Изображение {next_to_send}/{total_count} не удалось сгенерировать."
                    )
                    next_to_send += 1
                    continue

                image_record = await _send_generated_image_result(message, ready.pop(next_to_send))
                generated.append(image_record)
                sent_count += 1
                await _safe_edit_message_text(
                    status_message,
                    build_image_progress_message(total_count, generated_count, sent_count),
                )
                next_to_send += 1
    finally:
        stop_progress.set()
        await progress_task

    return generated


async def _image_generation_heartbeat(
    status_message: Any,
    total_count: int,
    get_counts: Any,
    stop_event: asyncio.Event,
) -> None:
    while not stop_event.is_set():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=30)
        except asyncio.TimeoutError:
            generated_count, sent_count = get_counts()
            await _safe_edit_message_text(
                status_message,
                build_image_progress_message(
                    total_count,
                    generated_count,
                    sent_count,
                    still_working=True,
                ),
            )


async def _safe_edit_message_text(message: Any, text: str) -> None:
    try:
        await message.edit_text(text)
    except Exception:
        logging.debug("Failed to edit image progress message", exc_info=True)


async def _generate_single_image_result(
    context: Any,
    concept: ImageConcept,
    photo_file_ids: list[str],
    settings: Settings,
) -> dict[str, Any]:
    photo_index = min(concept.photo_index, len(photo_file_ids) - 1)
    try:
        image_bytes = await asyncio.wait_for(
            generate_marketplace_image(
                prompt=concept.prompt,
                reference_photo_file_id=photo_file_ids[photo_index],
                bot=context.bot,
                api_key=settings.openrouter_api_key,
                model=settings.gpt_image_model,
                site_url=settings.site_url,
            ),
            timeout=180,
        )
    except Exception as exc:
        return {
            "ok": False,
            "image_index": concept.image_index,
            "error": str(exc),
        }

    return {
        "ok": True,
        "image_index": concept.image_index,
        "purpose": concept.purpose,
        "prompt_used": concept.prompt,
        "image_bytes": image_bytes,
    }


async def _send_generated_image_result(message: Any, result: dict[str, Any]) -> dict[str, Any]:
    buffer = BytesIO(result["image_bytes"])
    buffer.name = f"cardbot-image-{result['image_index']}.png"
    sent_message = await message.reply_photo(
        photo=buffer,
        caption=f"Изображение {result['image_index']}: {result['purpose']}",
    )
    telegram_file_id = ""
    if getattr(sent_message, "photo", None):
        telegram_file_id = sent_message.photo[-1].file_id
    return {
        "image_index": result["image_index"],
        "prompt_used": result["prompt_used"],
        "telegram_file_id": telegram_file_id,
    }


async def _generate_and_send_text_card(
    message: Any,
    context: Any,
    user_id: int,
    user_input: str,
    marketplace: str,
    *,
    final_markup: Any | None = None,
    intro_text: str = "⏳ Генерирую карточку...",
    mode: str = "text_only",
    photo_file_ids: list[str] | None = None,
    images_count: int | None = None,
) -> CardGeneration | None:
    settings = _get_settings(context)
    db = _get_db(context)
    usage_mode = await db.get_usage_mode(
        user_id, trial_generations=settings.trial_generations
    )
    if usage_mode is UsageMode.BLOCKED:
        await message.reply_text(
            "Бесплатные генерации закончились.",
            reply_markup=build_buy_keyboard(),
        )
        return None

    if intro_text:
        await message.reply_text(intro_text)

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
        await message.reply_text(
            "Произошла ошибка, попробуйте ещё раз. Генерация не списана."
        )
        return None

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
        await message.reply_text(
            "Карточка создана, но не удалось сохранить историю. Попробуйте позже."
        )
        return None

    messages = build_generation_messages(card)
    for text in messages[:-1]:
        await message.reply_text(text)
    await message.reply_text(
        messages[-1],
        reply_markup=final_markup,
    )
    _store_last_generation(
        context,
        marketplace=marketplace,
        mode=mode,
        description=user_input,
        photo_file_ids=photo_file_ids,
        images_count=images_count,
    )
    return card


async def _handle_template_name(update: Any, context: Any, user_id: int, user_input: str) -> bool:
    if not context.user_data.get("awaiting_template_name"):
        return False

    context.user_data.pop("awaiting_template_name", None)
    last_generation = context.user_data.get("last_generation")
    if not last_generation:
        await update.effective_message.reply_text("Нет данных последней генерации для сохранения.")
        return True

    count = await _get_db(context).get_templates_count(user_id)
    if count >= TEMPLATES_LIMIT:
        await update.effective_message.reply_text(
            "У вас уже 10 шаблонов — максимум. Удалите старый шаблон чтобы сохранить новый."
        )
        return True

    name = truncate_template_name(user_input)
    await _get_db(context).save_template(
        user_id=user_id,
        name=name,
        marketplace=last_generation["marketplace"],
        mode=last_generation["mode"],
        description=last_generation["description"],
        photo_file_ids=last_generation.get("photo_file_ids") or [],
        images_count=last_generation.get("images_count"),
    )
    await update.effective_message.reply_text(
        f"✅ Шаблон \"{name}\" сохранён.\nНайти его можно через /templates"
    )
    return True


async def _handle_repeat_changes(update: Any, context: Any, user_id: int, user_input: str) -> bool:
    if not context.user_data.get("awaiting_repeat_changes"):
        return False

    context.user_data.pop("awaiting_repeat_changes", None)
    previous = context.user_data.get("last_generation")
    if not previous:
        await update.effective_message.reply_text("Нет предыдущей генерации для повтора.")
        return True

    combined_description = combine_repeat_description(previous["description"], user_input)
    marketplace = previous["marketplace"]
    if previous["mode"] == "text_and_images":
        context.user_data["repeat_pending_generation"] = {
            "marketplace": marketplace,
            "mode": "text_and_images",
            "description": combined_description,
            "photo_file_ids": list(previous.get("photo_file_ids") or []),
            "images_count": previous.get("images_count") or 1,
        }
        await update.effective_message.reply_text(
            REPEAT_PHOTOS_PROMPT,
            reply_markup=build_repeat_photos_keyboard(),
        )
        return True

    await _generate_and_send_text_card(
        update.effective_message,
        context,
        user_id,
        combined_description,
        marketplace,
        final_markup=build_after_generation_keyboard(),
    )
    _clear_image_session(context)
    return True


async def _run_last_generation_with_images(
    update: Any,
    context: Any,
    user_id: int,
    generation: dict[str, Any],
) -> None:
    photo_file_ids = list(generation.get("photo_file_ids") or [])
    images_count = int(generation.get("images_count") or 1)
    if not photo_file_ids:
        await update.callback_query.message.reply_text(
            "В шаблоне нет сохранённых фото. Загрузите новые фото для генерации."
        )
        context.user_data["marketplace"] = generation["marketplace"]
        context.user_data["mode"] = "text_and_images"
        context.user_data["img_description"] = generation["description"]
        context.user_data["img_photos"] = []
        context.user_data["generation_step"] = "photos"
        context.user_data["repeat_images_count"] = images_count
        await update.callback_query.message.reply_text(IMAGE_PHOTO_PROMPT)
        return

    context.user_data["marketplace"] = generation["marketplace"]
    context.user_data["mode"] = "text_and_images"
    context.user_data["img_description"] = generation["description"]
    context.user_data["img_photos"] = photo_file_ids
    context.user_data["img_count"] = images_count
    await _generate_text_and_images_for_user(update, context, user_id, images_count)


async def _run_saved_generation(
    update: Any,
    context: Any,
    user_id: int,
    generation: dict[str, Any],
) -> None:
    if generation["mode"] == "text_and_images":
        await _run_last_generation_with_images(update, context, user_id, generation)
        return

    await _generate_and_send_text_card(
        update.callback_query.message,
        context,
        user_id,
        generation["description"],
        generation["marketplace"],
        final_markup=build_after_generation_keyboard(),
    )
    _clear_image_session(context)


async def handle_text(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None or update.effective_message is None:
        return

    user_input = (update.effective_message.text or "").strip()
    if await _handle_template_name(update, context, user_id, user_input):
        return
    if await _handle_repeat_changes(update, context, user_id, user_input):
        return
    if await _handle_image_description(update, context, user_input):
        return

    if context.user_data.get("generation_step") == "mode":
        await update.effective_message.reply_text(
            MODE_PROMPT,
            reply_markup=build_generation_mode_keyboard(),
        )
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

    await _generate_and_send_text_card(
        update.effective_message,
        context,
        user_id,
        user_input,
        marketplace,
        final_markup=build_after_generation_keyboard(),
    )
    _clear_image_session(context)


async def handle_callback(update: Any, context: Any) -> None:
    query = update.callback_query
    user_id = await _ensure_user(update, context)

    data = query.data or ""
    if data != "action:save_template":
        await query.answer()
    if data == "action:generate":
        _clear_image_session(context)
        context.user_data["generation_step"] = "marketplace"
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
        context.user_data["generation_step"] = "mode"
        await query.message.reply_text(
            MODE_PROMPT,
            reply_markup=build_generation_mode_keyboard(),
        )
    elif data.startswith("mode:"):
        mode = data.split(":", 1)[1]
        if mode not in {"text_only", "text_and_images"}:
            await query.message.reply_text(
                MODE_PROMPT,
                reply_markup=build_generation_mode_keyboard(),
            )
            return
        context.user_data["mode"] = mode
        if mode == "text_and_images":
            user = update.effective_user
            if user is None:
                return
            image_balance = await _get_db(context).get_image_balance(user.id)
            if image_balance <= 0:
                await query.message.reply_text(
                    "У вас нет изображений на балансе.\n"
                    "Купите пакет изображений чтобы использовать этот режим.",
                    reply_markup=build_no_image_balance_keyboard(),
                )
                return
            context.user_data["generation_step"] = "description"
            await query.message.reply_text(IMAGE_DESCRIPTION_PROMPT)
            return

        context.user_data["generation_step"] = "description"
        await query.message.reply_text(GENERATE_PROMPT)
    elif data.startswith("img_marketplace:"):
        try:
            marketplace = normalize_marketplace(data.split(":", 1)[1])
            context.user_data["marketplace"] = marketplace
            context.user_data["img_marketplace"] = marketplace
        except Exception:
            await query.message.reply_text(
                MARKETPLACE_PROMPT,
                reply_markup=build_image_marketplace_keyboard(),
            )
            return
        context.user_data["mode"] = "text_and_images"
        context.user_data["generation_step"] = "description"
        await query.message.reply_text(IMAGE_DESCRIPTION_PROMPT)
    elif data == "img_add_more":
        await query.message.reply_text(IMAGE_PHOTO_PROMPT)
    elif data == "img_photos_done":
        photos = list(context.user_data.get("img_photos") or [])
        if not photos:
            await query.message.reply_text(IMAGE_PHOTO_PROMPT)
            return
        if context.user_data.get("repeat_images_count"):
            user = update.effective_user
            if user is None:
                return
            images_count = int(context.user_data.pop("repeat_images_count"))
            context.user_data["img_count"] = images_count
            await _generate_text_and_images_for_user(update, context, user.id, images_count)
            return
        context.user_data["generation_step"] = "count"
        user = update.effective_user
        image_balance = await _get_db(context).get_image_balance(user.id) if user is not None else 0
        await query.message.reply_text(
            build_image_count_prompt(image_balance),
            reply_markup=build_image_count_keyboard(image_balance=image_balance),
        )
    elif data.startswith("img_count:"):
        user = update.effective_user
        if user is None:
            return
        try:
            images_count = int(data.split(":", 1)[1])
        except ValueError:
            image_balance = await _get_db(context).get_image_balance(user.id)
            await query.message.reply_text(
                build_image_count_prompt(image_balance),
                reply_markup=build_image_count_keyboard(image_balance=image_balance),
            )
            return
        if images_count < 1 or images_count > 9:
            image_balance = await _get_db(context).get_image_balance(user.id)
            await query.message.reply_text(
                build_image_count_prompt(image_balance),
                reply_markup=build_image_count_keyboard(image_balance=image_balance),
            )
            return
        image_balance = await _get_db(context).get_image_balance(user.id)
        if images_count > image_balance:
            await query.message.reply_text(
                build_image_count_prompt(image_balance),
                reply_markup=build_image_count_keyboard(image_balance=image_balance),
            )
            return
        context.user_data["img_count"] = images_count
        if context.user_data.get("mode") == "text_and_images":
            await _generate_text_and_images_for_user(update, context, user.id, images_count)
        else:
            await _generate_images_for_user(update, context, user.id, images_count)
    elif data == "action:balance":
        await balance_command(update, context)
    elif data == "action:buy":
        if user_id is not None:
            await _show_buy_menu(query.message, context, user_id, kind="all")
    elif data == "action:buy_combo":
        if user_id is not None:
            await _show_buy_menu(query.message, context, user_id, kind="combo")
    elif data == "action:buy_text":
        if user_id is not None:
            await _show_buy_menu(query.message, context, user_id, kind="text")
    elif data == "action:buy_images":
        if user_id is not None:
            await _show_buy_menu(query.message, context, user_id, kind="images")
    elif data == "action:templates":
        if user_id is not None:
            await _show_templates(query.message, context, user_id, page=0)
    elif data == "action:history":
        await history_command(update, context)
    elif data == "action:help":
        settings = _get_settings(context)
        await query.message.reply_text(
            build_help_message(),
            reply_markup=build_help_keyboard(settings.cardbot_offer_url),
        )
    elif data == "action:save_template":
        if user_id is None:
            await query.answer()
            return
        if not context.user_data.get("last_generation"):
            await query.answer()
            await query.message.reply_text("Нет данных последней генерации для сохранения.")
            return
        count = await _get_db(context).get_templates_count(user_id)
        if count >= TEMPLATES_LIMIT:
            await query.answer(
                "У вас уже 10 шаблонов — максимум. Удалите старый шаблон чтобы сохранить новый.",
                show_alert=True,
            )
            return
        await query.answer()
        context.user_data["awaiting_template_name"] = True
        await query.message.reply_text(TEMPLATE_NAME_PROMPT)
    elif data == "action:repeat_edit":
        if not context.user_data.get("last_generation"):
            await query.message.reply_text("Нет предыдущей генерации для повтора.")
            return
        context.user_data["awaiting_repeat_changes"] = True
        await query.message.reply_text(REPEAT_CHANGES_PROMPT)
    elif data.startswith("repeat:"):
        if user_id is None:
            return
        pending = context.user_data.get("repeat_pending_generation")
        if not pending:
            await query.message.reply_text("Сессия повтора устарела. Начните заново.")
            return
        repeat_mode = data.split(":", 1)[1]
        context.user_data["repeat_mode"] = repeat_mode
        if repeat_mode == "same_photos":
            await _run_last_generation_with_images(update, context, user_id, pending)
            return
        if repeat_mode == "new_photos":
            context.user_data["marketplace"] = pending["marketplace"]
            context.user_data["mode"] = "text_and_images"
            context.user_data["img_description"] = pending["description"]
            context.user_data["img_photos"] = []
            context.user_data["generation_step"] = "photos"
            context.user_data["repeat_images_count"] = int(pending.get("images_count") or 1)
            await query.message.reply_text(IMAGE_PHOTO_PROMPT)
            return
        await query.message.reply_text(REPEAT_PHOTOS_PROMPT, reply_markup=build_repeat_photos_keyboard())
    elif data.startswith("templates_page:"):
        if user_id is None:
            return
        try:
            page = int(data.split(":", 1)[1])
        except ValueError:
            page = 0
        await _show_templates(query.message, context, user_id, page=page)
    elif data.startswith("templates_delete:"):
        if user_id is None:
            return
        try:
            page = int(data.split(":", 1)[1])
        except ValueError:
            page = 0
        await _show_templates_delete_list(query.message, context, user_id, page=page)
    elif data.startswith("template_use:"):
        if user_id is None:
            return
        try:
            template_id = int(data.split(":", 1)[1])
        except ValueError:
            return
        template = await _get_db(context).get_template(template_id, user_id)
        if not template:
            await query.message.reply_text("Шаблон не найден.")
            return
        await query.message.reply_text(
            build_template_details_message(template),
            reply_markup=build_template_details_keyboard(template_id),
        )
    elif data.startswith("template_run:"):
        if user_id is None:
            return
        try:
            template_id = int(data.split(":", 1)[1])
        except ValueError:
            return
        template = await _get_db(context).get_template(template_id, user_id)
        if not template:
            await query.message.reply_text("Шаблон не найден.")
            return
        await _run_saved_generation(update, context, user_id, _template_to_last_generation(template))
    elif data.startswith("template_edit:"):
        if user_id is None:
            return
        try:
            template_id = int(data.split(":", 1)[1])
        except ValueError:
            return
        template = await _get_db(context).get_template(template_id, user_id)
        if not template:
            await query.message.reply_text("Шаблон не найден.")
            return
        context.user_data["last_generation"] = _template_to_last_generation(template)
        context.user_data["awaiting_repeat_changes"] = True
        await query.message.reply_text(REPEAT_CHANGES_PROMPT)
    elif data.startswith("template_delete:"):
        if user_id is None:
            return
        try:
            template_id = int(data.split(":", 1)[1])
        except ValueError:
            return
        template = await _get_db(context).get_template(template_id, user_id)
        if not template:
            await query.message.reply_text("Шаблон не найден.")
            return
        await query.message.reply_text(
            f"Удалить шаблон \"{template['name']}\"?",
            reply_markup=build_template_delete_confirm_keyboard(template_id),
        )
    elif data.startswith("template_delete_confirm:"):
        if user_id is None:
            return
        try:
            template_id = int(data.split(":", 1)[1])
        except ValueError:
            return
        await _get_db(context).delete_template(template_id, user_id)
        await query.message.reply_text("🗑 Шаблон удалён.")
    elif data.startswith("template_delete_cancel:"):
        await query.message.reply_text("Удаление отменено.")
    elif data == "buy_back:root":
        if user_id is not None:
            await _show_buy_menu(query.message, context, user_id, kind="all")
    elif data == "buy_back:combo":
        if user_id is not None:
            await _show_buy_menu(query.message, context, user_id, kind="combo")
    elif data.startswith("combo_cards:"):
        try:
            text_count = int(data.split(":", 1)[1])
        except ValueError:
            return
        await query.message.reply_text(
            f"{text_count} карточек: выберите количество фото",
            reply_markup=build_combo_photo_count_keyboard(text_count),
        )
    elif data.startswith(("buy:", "img_buy:")):
        if user_id is None:
            return
        package_code = data.split(":", 1)[1]
        await _send_payment_link(query.message, context, user_id, package_code)


async def post_init(application: Any) -> None:
    db: Database = application.bot_data["db"]
    settings: Settings = application.bot_data["settings"]
    await db.connect()
    await db.init_db()
    application.bot_data["webhook_runner"] = await start_webhook_server(
        bot=application.bot,
        db=db,
        robokassa_password2=settings.robokassa_password2,
        port=settings.cardbot_webhook_port,
    )
    await application.bot.set_my_commands(
        [
            ("start", "Главное меню"),
            ("generate", "Сгенерировать карточку"),
            ("balance", "Показать баланс"),
            ("templates", "Мои шаблоны"),
            ("history", "Последние 5 генераций"),
            ("buy", "Купить генерации"),
            ("help", "Помощь"),
        ]
    )


async def post_shutdown(application: Any) -> None:
    webhook_runner = application.bot_data.get("webhook_runner")
    if webhook_runner is not None:
        await webhook_runner.cleanup()
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
    application.add_handler(CommandHandler("templates", templates_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("buy", buy_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.IMAGE, handle_document))
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
