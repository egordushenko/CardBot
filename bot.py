from __future__ import annotations

import logging
import asyncio
import json
from contextlib import suppress
from io import BytesIO
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from config import Settings, load_settings
from category_detector import detect_category
from category_profiles import (
    detect_ozon_category_profile,
    detect_wb_category_profile,
    get_category_profile,
    load_category_profiles,
    load_ozon_categories,
    load_wb_category_profiles,
)
from core.field_resolver import resolve_fields
from db import Database, UsageMode
from image_generator import (
    ImageBatchConcept,
    generate_marketplace_batch_image_results,
)
from llm import (
    CardGeneration,
    ImageConcept,
    ImagePromptPlan,
    generate_card,
    generate_image_prompts,
    normalize_image_style_custom,
    normalize_image_style_preset,
    normalize_image_text_mode,
    normalize_marketplace,
)
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


PAYMENT_UNAVAILABLE_MESSAGE = "💳 Оплата временно недоступна.\nПопробуйте немного позже."
TECHNICAL_WORKS_MESSAGE = (
    "⚙️ В сервисе временные технические работы.\n"
    "Попробуйте немного позже. Генерация не списана."
)
GENERATE_PROMPT = (
    "📝 Опишите товар\n\n"
    "Минимум — название.\n"
    "Можно добавить: материал, размер, цвет, особенности.\n"
    "Чем подробнее описание, тем точнее карточка."
)
FEEDBACK_MESSAGE = (
    "💬 Не понравился результат?\n\n"
    "Напишите, что нужно исправить: название, описание, хэштеги или характеристики.\n\n"
    "Контакт: @alterega"
)
MARKETPLACE_PROMPT = "🛒 Выберите маркетплейс:"
MODE_PROMPT = (
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
IMAGE_DESCRIPTION_PROMPT = (
    "📝 Опишите товар\n\n"
    "Укажите название, материал, размер, цвет и главные преимущества.\n"
    "После этого бот попросит загрузить фото товара."
)
IMAGE_PHOTO_PROMPT = (
    "📸 Загрузите от 1 до 7 фото товара с разных ракурсов.\n\n"
    "Когда все фото загружены, нажмите ✅ Готово"
)
IMAGE_GUIDANCE_PROMPT = (
    "🎨 Пожелания к изображениям\n\n"
    "Можно написать стиль, фон, ракурсы, роли для каждого кадра, текст на картинках или общую концепцию.\n"
    "Это необязательно: если пожеланий нет, нажмите «Пропустить»."
)
IMAGE_TEXT_MODE_PROMPT = (
    "Текст на изображениях\n\n"
    "Выберите режим: без текста, минимум текста или инфографика."
)
IMAGE_STYLE_PROMPT = (
    "Стиль изображений\n\n"
    "Выберите пресет или задайте свой стиль. Этот шаг необязательный."
)
IMAGE_STYLE_CUSTOM_PROMPT = (
    "Напишите свой стиль\n\n"
    "Например: luxury studio, dark premium, sporty dynamic, warm eco."
)
TEMPLATE_NAME_PROMPT = (
    "📋 Введите название шаблона\n\n"
    "Например: \"Лампа спиральная\" или \"Коврик ЭВА\""
)
NEW_TEMPLATE_TEXT_PROMPT = (
    "✍️ Введите текст шаблона\n\n"
    "Например: \"Название товара, цвет {цвет}, размер {размер}, материал {материал}\""
)
REPEAT_CHANGES_PROMPT = (
    "🔄 Что изменить?\n\n"
    "Напишите только то, что поменялось.\n"
    "Например: \"цвет чёрный\" или \"размер XL, вес 2 кг\"\n\n"
    "Остальное останется как в предыдущей карточке."
)
REPEAT_PHOTOS_PROMPT = "📸 Какие фото использовать?"
TEMPLATES_PAGE_SIZE = 5
TEMPLATES_LIMIT = 10
MAX_REFERENCE_PHOTOS = 7
IMAGE_COUNT_OPTIONS = (1, 3, 5, 7)
HOME_CALLBACK = "action:home"
HOME_BUTTON_TEXT = "🏠 Главная"
BACK_BUTTON_TEXT = "⬅️ Назад"
COMBO_PACKAGE_BUTTON_TEXT = "💳 Комбо: карточки + изображения"
REPLY_ACTIONS = {
    "⚡ Сгенерировать карточку": "generate",
    "💳 Купить генерации": "buy",
    "📊 Мой баланс": "balance",
    "📋 Мои шаблоны": "templates",
    "🕐 История": "history",
    "❓ Помощь": "help",
    HOME_BUTTON_TEXT: "home",
    "Главная": "home",
}


@dataclass(frozen=True)
class KeyboardButton:
    text: str
    callback_data: str
    url: str | None = None


@dataclass(frozen=True)
class KeyboardMarkup:
    inline_keyboard: list[list[KeyboardButton]]


@dataclass(frozen=True)
class ReplyKeyboardMarkupFallback:
    keyboard: list[list[str]]
    resize_keyboard: bool = True


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


def _home_button() -> Any:
    return _button(HOME_BUTTON_TEXT, HOME_CALLBACK)


def _nav_row(back_callback: str | None = None) -> list[Any]:
    row: list[Any] = []
    if back_callback:
        row.append(_button(BACK_BUTTON_TEXT, back_callback))
    row.append(_home_button())
    return row


def classify_reply_action(text: Any | None) -> str | None:
    value = getattr(text, "text", text)
    return REPLY_ACTIONS.get(str(value or "").strip())


def build_persistent_main_keyboard() -> Any:
    rows = [
        ["⚡ Сгенерировать карточку"],
        ["💳 Купить генерации", "📊 Мой баланс"],
        ["📋 Мои шаблоны", "🕐 История"],
        ["❓ Помощь"],
    ]
    try:
        from telegram import ReplyKeyboardMarkup

        return ReplyKeyboardMarkup(rows, resize_keyboard=True)
    except ImportError:
        return ReplyKeyboardMarkupFallback(rows)


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
                _button("🕐 История", "action:history"),
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
        label = f"{images_per_card} фото на карточку — {package.price_rub:,} ₽"
    return _button(label.replace(",", " "), f"buy:{code}")


def build_buy_keyboard(show_first_image_promo: bool = False) -> Any:
    return _keyboard(
        [
            [_button(COMBO_PACKAGE_BUTTON_TEXT, "action:buy_combo")],
            [_button("Только карточки", "action:buy_text")],
            [_button("Только изображения", "action:buy_images")],
            [_home_button()],
        ]
    )


def build_combined_buy_keyboard(show_first_image_promo: bool = False) -> Any:
    return build_buy_keyboard(show_first_image_promo=show_first_image_promo)


def build_combo_card_count_keyboard() -> Any:
    counts = sorted({PAYMENT_PACKAGES[code].text_count for code in MAIN_PACKAGE_CODES})
    rows = [[_button(f"{count} карточек", f"combo_cards:{count}")] for count in counts]
    rows.append(_nav_row("buy_back:root"))
    return _keyboard(rows)


def build_combo_photo_count_keyboard(text_count: int) -> Any:
    photo_counts = sorted(
        PAYMENT_PACKAGES[code].images_per_card
        for code in MAIN_PACKAGE_CODES
        if PAYMENT_PACKAGES[code].text_count == text_count
    )
    rows = [[_combo_payment_button(text_count, photo_count)] for photo_count in photo_counts]
    rows.append(_nav_row("buy_back:combo"))
    return _keyboard(rows)


def build_balance_keyboard() -> Any:
    return _keyboard(
        [
            [_button(COMBO_PACKAGE_BUTTON_TEXT, "action:buy_combo")],
            [
                _button("💳 Купить текстовые", "action:buy_text"),
                _button("💳 Купить изображения", "action:buy_images"),
            ],
            [_home_button()],
        ]
    )


def build_image_packages_keyboard(show_first_image_promo: bool = False) -> Any:
    rows = [[_payment_button(code)] for code in IMAGE_ADDON_CODES]
    if show_first_image_promo:
        rows.insert(0, [_payment_button(PROMO_PACKAGE_CODE)])
    rows.append(_nav_row("buy_back:root"))
    return _keyboard(rows)


def build_text_packages_keyboard() -> Any:
    rows = [[_payment_button(code)] for code in TEXT_ADDON_CODES]
    rows.append(_nav_row("buy_back:root"))
    return _keyboard(rows)


def build_payment_link_keyboard(payment_url: str) -> Any:
    return _keyboard([[_url_button("Перейти к оплате", payment_url)], [_home_button()]])


def build_marketplace_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("Wildberries", "marketplace:wb"),
                _button("Ozon", "marketplace:ozon"),
            ],
            [_home_button()],
        ]
    )


def build_generation_mode_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("📝 Только текст", "mode:text_only"),
                _button("📝🖼 Текст + изображения", "mode:text_and_images"),
            ],
            [_button("🖼 Только изображения", "mode:images_only")],
            _nav_row("action:generate"),
        ]
    )


def build_no_image_balance_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("💳 Купить изображения", "action:buy_images"),
                _button("📝 Только текст", "mode:text_only"),
            ],
            [_home_button()],
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
            ],
            [_home_button()],
        ]
    )


def build_image_photo_keyboard(photos_count: int) -> Any:
    row = [_button("✅ Готово", "img_photos_done")]
    if photos_count < MAX_REFERENCE_PHOTOS:
        row.append(_button(f"📎 Ещё ({photos_count}/{MAX_REFERENCE_PHOTOS})", "img_add_more"))
    return _keyboard([row, [_home_button()]])


def build_image_guidance_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("✍️ Написать пожелания", "img_guidance_write"),
                _button("Пропустить", "img_guidance_skip"),
            ],
            [_home_button()],
        ]
    )


def build_image_text_mode_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("Без текста", "img_text_mode:no_text"),
                _button("Минимум текста", "img_text_mode:minimal"),
            ],
            [_button("Инфографика", "img_text_mode:infographic")],
            [_button("Пропустить", "img_text_mode:skip")],
            [_home_button()],
        ]
    )


def build_image_style_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("Минимализм", "img_style:minimalism"),
                _button("Luxury", "img_style:luxury"),
            ],
            [
                _button("Спорт", "img_style:sport"),
                _button("Темный премиум", "img_style:dark_premium"),
            ],
            [
                _button("Светлый", "img_style:light_wb"),
                _button("Детский", "img_style:kids"),
            ],
            [
                _button("Натуральный", "img_style:eco"),
                _button("Свой стиль", "img_style:custom"),
            ],
            [_button("Пропустить", "img_style:skip")],
            [_home_button()],
        ]
    )


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
    return f"Фото {added_count} получено ✓\nВсего: {total_count}/{MAX_REFERENCE_PHOTOS}"


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
        f"Готово: {sent_count} из {total_count}"
        f"{suffix}"
    )


def build_image_count_keyboard(image_balance: int | None = None) -> Any:
    counts = list(IMAGE_COUNT_OPTIONS)
    if image_balance is not None:
        counts = [count for count in counts if count <= image_balance]
    if not counts:
        return _keyboard([[_button("💳 Купить изображения", "action:buy_images")], [_home_button()]])
    rows = [[_button(str(count), f"img_count:{count}") for count in counts[:3]]]
    if len(counts) > 3:
        rows.append([_button(str(count), f"img_count:{count}") for count in counts[3:]])
    rows.append([_home_button()])
    return _keyboard(rows)

def build_image_count_prompt(image_balance: int) -> str:
    return (
        "Сколько изображений сгенерировать?\n\n"
        f"На вашем балансе: {image_balance} изображений"
    )


def is_allowed_image_count(images_count: int) -> bool:
    return images_count in IMAGE_COUNT_OPTIONS


def should_generate_text_with_images(mode: str | None) -> bool:
    return mode == "text_and_images"


def build_after_generation_keyboard() -> Any:
    return _keyboard(
        [
            [
                _button("⚡ Сгенерировать ещё", "action:generate"),
                _button("💾 Сохранить как шаблон", "action:save_template"),
            ],
            [
                _button("🔄 Изменить и повторить", "action:repeat_edit"),
                _button("💳 Пополнить баланс", "action:buy"),
            ],
            [_button("💬 Не понравился результат?", "action:feedback")],
            [_home_button()],
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
            [_button("💬 Не понравился результат?", "action:feedback")],
            [_home_button()],
        ]
    )

def truncate_template_name(name: str) -> str:
    return (name or "").strip()[:50] or "Шаблон"


def combine_repeat_description(previous_description: str, user_changes: str) -> str:
    return f"{previous_description.strip()}\n\nИзменения: {user_changes.strip()}"


def format_marketplace(marketplace: str) -> str:
    return "Wildberries" if marketplace == "wb" else "Ozon"


def format_template_mode(mode: str) -> str:
    if mode == "text_and_images":
        return "Текст + изображения"
    if mode == "images_only":
        return "Только изображения"
    return "Только текст"


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
            ],
            [_home_button()],
        ]
    )

def build_templates_keyboard(
    templates: list[dict[str, Any]],
    page: int,
    total: int,
) -> Any:
    rows = [[_button("➕ Создать новый шаблон", "template_new")]]
    rows.extend([[_button(template["name"], f"template_use:{template['id']}")] for template in templates])
    nav_row: list[Any] = []
    if page > 0:
        nav_row.append(_button("← Назад", f"templates_page:{page - 1}"))
    if (page + 1) * TEMPLATES_PAGE_SIZE < total:
        nav_row.append(_button("Вперёд →", f"templates_page:{page + 1}"))
    if nav_row:
        rows.append(nav_row)
    rows.append([_button("🗑 Удалить шаблон", f"templates_delete:{page}")])
    rows.append([_home_button()])
    return _keyboard(rows)


def build_empty_templates_keyboard() -> Any:
    return _keyboard([[_button("➕ Создать новый шаблон", "template_new")], [_home_button()]])

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
    rows.append([_home_button()])
    return _keyboard(rows)

def build_template_details_keyboard(template_id: int) -> Any:
    return _keyboard(
        [
            [_button("⚡ Использовать как есть", f"template_run:{template_id}")],
            [_button("✏️ Изменить и использовать", f"template_edit:{template_id}")],
            [_button("🗑 Удалить шаблон", f"template_delete:{template_id}")],
            [_home_button()],
        ]
    )

def build_template_delete_confirm_keyboard(template_id: int) -> Any:
    return _keyboard(
        [
            [
                _button("✅ Да, удалить", f"template_delete_confirm:{template_id}"),
                _button("❌ Отмена", f"template_delete_cancel:{template_id}"),
            ],
            [_home_button()],
        ]
    )

def build_generation_messages(card: CardGeneration) -> list[str]:
    messages = [
        f"📌 НАЗВАНИЕ:\n{card.title}",
        f"📝 ОПИСАНИЕ:\n{card.description}",
        f"📋 ХАРАКТЕРИСТИКИ:\n{card.characteristics}",
    ]
    if card.marketplace == "ozon":
        messages.insert(2, f"🔖 ХЭШТЕГИ:\n{card.keywords}")
    return messages


def classify_generation_error(exc: Exception) -> str:
    status_code = getattr(exc, "status_code", None)
    if status_code in {402, 403}:
        return "api_balance"
    if status_code == 429:
        return "429"
    message = str(exc).casefold()
    if any(
        marker in message
        for marker in (
            "insufficient credits",
            "insufficient balance",
            "not enough credits",
            "no auth credentials",
            "quota exceeded",
            "payment required",
        )
    ):
        return "api_balance"
    if "empty response" in message:
        return "empty_response"
    if "invalid json" in message or "missing required field" in message:
        return "parse_error"
    return "unknown"


def generation_error_message(reason: str) -> str:
    if reason in {"api_balance", "429"}:
        return TECHNICAL_WORKS_MESSAGE
    return "⚠️ Не удалось сгенерировать карточку.\nПопробуйте ещё раз. Генерация не списана."


def log_generation_error(
    exc: Exception,
    *,
    marketplace: str,
    mode: str,
    reason: str | None = None,
) -> None:
    logging.exception(
        "generation_error reason=%s marketplace=%s mode=%s",
        reason or classify_generation_error(exc),
        marketplace,
        mode,
    )


def build_balance_message(
    trial_used: int,
    balance: int,
    image_balance: int = 0,
    trial_generations: int = 3,
) -> str:
    free_left = max(trial_generations - trial_used, 0)
    text_balance = free_left + balance
    return (
        "📊 Баланс\n\n"
        f"📝 Текстовые генерации: {text_balance}\n"
        f"🖼 Изображения: {image_balance}"
    )


def build_help_message() -> str:
    return (
        "CardBot генерирует SEO-карточки товаров для Wildberries и Ozon.\n\n"
        "📝 Как пользоваться\n"
        "Отправьте описание товара одним сообщением. "
        "Бот вернёт название, описание, ключевые слова и характеристики.\n\n"
        "💳 Оплата и поддержка\n"
        "Контакт для вопросов по оплате и работе сервиса: alterega@list.ru\n\n"
        "📄 Реквизиты\n"
        "Самозанятый Дущенко Егор Владимирович\n"
        "ИНН: 615422982815\n"
        "Условия оказания услуги: публичная оферта.\n\n"
        "⌨️ Команды\n"
        "/generate — создать карточку\n"
        "/balance — баланс\n"
        "/templates — мои шаблоны\n"
        "/history — последние генерации\n"
        "/buy — пакеты генераций"
    )


def build_help_keyboard(offer_url: str) -> Any:
    return _keyboard([[_url_button("Публичная оферта", offer_url)], [_home_button()]])

def build_start_message(first_name: str | None) -> str:
    name = f", {first_name}" if first_name else ""
    return (
        f"Здравствуйте{name}.\n\n"
        "🛒 Я помогу подготовить карточку товара для Wildberries и Ozon.\n\n"
        "На старте доступно 3 бесплатные текстовые генерации."
    )


def _get_db(context: Any) -> Database:
    return context.application.bot_data["db"]


def _get_settings(context: Any) -> Settings:
    return context.application.bot_data["settings"]


def _infer_wb_field_category(product_description: str) -> str:
    text = product_description.casefold()
    if any(marker in text for marker in ("женск", "платье", "юбка", "блузка")):
        return "Женская одежда"
    if any(marker in text for marker in ("мужск", "брюки", "рубашка", "поло")):
        return "Мужская одежда"
    if any(marker in text for marker in ("детск", "ребен", "мальчик", "девочк")):
        return "Детская одежда"
    return "Одежда"


async def _resolve_generation_enrichment(
    context: Any,
    product_description: str,
    marketplace: str,
    *,
    has_photo: bool,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    normalized_marketplace = normalize_marketplace(marketplace)
    category_profile: dict[str, Any] | None = None

    if normalized_marketplace == "ozon":
        profiles = context.application.bot_data.get("category_profiles")
        if profiles is None:
            profiles = load_category_profiles()
            context.application.bot_data["category_profiles"] = profiles
        ozon_categories = context.application.bot_data.get("ozon_categories")
        if ozon_categories is None:
            ozon_categories = load_ozon_categories()
            context.application.bot_data["ozon_categories"] = ozon_categories

        category_profile = detect_ozon_category_profile(profiles, product_description, ozon_categories)
        if category_profile:
            category = str(category_profile.get("category") or category_profile.get("parent_category") or "")
        else:
            try:
                category = await asyncio.to_thread(detect_category, product_description)
            except Exception:
                logging.exception("Ozon category detection failed")
                category = "??????"

            category_profile = get_category_profile(profiles, category)
        if not category_profile:
            logging.warning("Ozon category profile not found: %s", category)
    else:
        profiles = context.application.bot_data.get("wb_category_profiles")
        if profiles is None:
            profiles = load_wb_category_profiles()
            context.application.bot_data["wb_category_profiles"] = profiles
        category_profile = detect_wb_category_profile(profiles, product_description)
        if category_profile:
            category = str(category_profile.get("category") or category_profile.get("parent_category") or "")
        else:
            category = _infer_wb_field_category(product_description)

    resolved_fields = resolve_fields(
        {"description": product_description},
        category=category,
        marketplace=normalized_marketplace,
        has_photo=has_photo,
    )
    return category_profile, resolved_fields


def _clear_image_session(context: Any) -> None:
    for key in (
        "mode",
        "generation_step",
        "marketplace",
        "img_marketplace",
        "img_description",
        "img_photos",
        "img_guidance",
        "img_count",
        "img_text_mode",
        "img_style_preset",
        "img_style_custom",
        "img_media_groups",
        "repeat_pending_generation",
        "repeat_mode",
        "repeat_images_count",
        "awaiting_image_style_custom",
    ):
        context.user_data.pop(key, None)


def _reset_navigation_state(context: Any) -> None:
    _clear_image_session(context)
    for key in (
        "awaiting_template_name",
        "awaiting_repeat_changes",
        "awaiting_new_template_name",
        "awaiting_new_template_text",
        "new_template_name",
    ):
        context.user_data.pop(key, None)


async def _show_home(message: Any, context: Any, first_name: str | None = None) -> None:
    _reset_navigation_state(context)
    await message.reply_text(
        build_start_message(first_name),
        reply_markup=build_main_menu(),
    )


def _store_last_generation(
    context: Any,
    *,
    marketplace: str,
    mode: str,
    description: str,
    photo_file_ids: list[str] | None = None,
    images_count: int | None = None,
    image_guidance: str | None = None,
    image_text_mode: str | None = None,
    image_style_preset: str | None = None,
    image_style_custom: str | None = None,
) -> None:
    context.user_data["last_generation"] = {
        "marketplace": marketplace,
        "mode": mode,
        "description": description,
        "photo_file_ids": list(photo_file_ids or []),
        "images_count": images_count,
        "image_guidance": image_guidance or "",
        "image_text_mode": normalize_image_text_mode(image_text_mode),
        "image_style_preset": normalize_image_style_preset(image_style_preset),
        "image_style_custom": normalize_image_style_custom(image_style_custom),
    }


def _template_to_last_generation(template: dict[str, Any]) -> dict[str, Any]:
    return {
        "marketplace": template["marketplace"],
        "mode": template["mode"],
        "description": template["description"],
        "photo_file_ids": _parse_photo_file_ids(template.get("photo_file_ids")),
        "images_count": template.get("images_count"),
        "image_guidance": template.get("image_guidance") or "",
        "image_text_mode": normalize_image_text_mode(template.get("image_text_mode")),
        "image_style_preset": normalize_image_style_preset(template.get("image_style_preset")),
        "image_style_custom": normalize_image_style_custom(template.get("image_style_custom")),
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
        reply_markup=build_persistent_main_keyboard(),
    )
    await update.effective_message.reply_text(
        "Выберите действие:",
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
            "💳 Сколько карточек нужно в комбо-пакете?",
            reply_markup=build_combo_card_count_keyboard(),
        )
        return
    if kind == "text":
        await message.reply_text(
            "📝 Выберите пакет текстовых карточек:",
            reply_markup=build_text_packages_keyboard(),
        )
        return
    if kind == "images":
        await message.reply_text(
            "🖼 Выберите пакет изображений:",
            reply_markup=build_image_packages_keyboard(show_first_image_promo=first_image_purchase),
        )
        return
    await message.reply_text(
        "💳 Что хотите купить?",
        reply_markup=build_combined_buy_keyboard(show_first_image_promo=first_image_purchase),
    )


async def _send_payment_link(message: Any, context: Any, user_id: int, package_code: str) -> None:
    if package_code not in PAYMENT_PACKAGES:
        await message.reply_text("⚠️ Пакет не найден.\nОткройте /buy и выберите пакет заново.")
        return

    db = _get_db(context)
    if package_code == PROMO_PACKAGE_CODE and not await db.is_first_image_purchase(user_id):
        await message.reply_text("⚠️ Акция первой покупки уже использована.")
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
        await update.effective_message.reply_text("🕐 История пока пустая.")
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
        await message.reply_text(
            "📋 У вас пока нет шаблонов.\nСоздайте новый шаблон или сохраните готовую карточку.",
            reply_markup=build_empty_templates_keyboard(),
        )
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
        "🗑 Выберите шаблон для удаления:",
        reply_markup=build_templates_delete_keyboard(templates, page=page, total=total),
    )


def build_template_details_message(template: dict[str, Any]) -> str:
    return (
        f"📋 Шаблон: \"{template['name']}\"\n\n"
        f"🛒 Маркетплейс: {format_marketplace(template['marketplace'])}\n"
        f"⚙️ Режим: {format_template_mode(template['mode'])}\n\n"
        f"📝 Текст: {format_template_description_preview(template['description'])}\n\n"
        "Что сделать?"
    )


async def _start_image_flow(message: Any, context: Any, user_id: int) -> None:
    _clear_image_session(context)
    context.user_data["generation_step"] = "marketplace"
    await message.reply_text(
        MARKETPLACE_PROMPT,
        reply_markup=build_marketplace_keyboard(),
    )


async def _start_new_template_flow(message: Any, context: Any) -> None:
    _clear_image_session(context)
    context.user_data["awaiting_new_template_name"] = True
    await message.reply_text(TEMPLATE_NAME_PROMPT)


async def _handle_image_description(update: Any, context: Any, user_input: str) -> bool:
    if context.user_data.get("generation_step") != "description":
        return False
    if context.user_data.get("mode") not in {"text_and_images", "images_only"}:
        return False

    if len(user_input) < 3:
        await update.effective_message.reply_text(
            "⚠️ Добавьте хотя бы название или категорию товара."
        )
        return True

    context.user_data["img_description"] = user_input
    context.user_data["generation_step"] = "photos"
    context.user_data["img_photos"] = []
    await update.effective_message.reply_text(IMAGE_PHOTO_PROMPT)
    return True


def _normalize_image_guidance_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(str(value).split())[:1200]


def _image_text_mode_label(value: str | None) -> str:
    mapping = {
        "no_text": "no_text",
        "minimal": "minimal",
        "infographic": "infographic",
    }
    return mapping.get(normalize_image_text_mode(value), "minimal")


def _serialize_image_report(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False)


def _build_image_report_base(
    *,
    generation_mode: str,
    marketplace: str,
    product_description: str,
    photo_file_ids: list[str],
    images_count: int,
    image_guidance: str,
    image_text_mode: str,
    image_style_preset: str,
    image_style_custom: str,
) -> dict[str, Any]:
    return {
        "generation_mode": generation_mode,
        "image_pipeline": "batch",
        "marketplace": marketplace,
        "product_description": product_description,
        "photo_file_ids": list(photo_file_ids),
        "photos_count": len(photo_file_ids),
        "images_requested": images_count,
        "image_guidance": image_guidance,
        "image_text_mode": normalize_image_text_mode(image_text_mode),
        "image_style_preset": normalize_image_style_preset(image_style_preset),
        "image_style_custom": normalize_image_style_custom(image_style_custom),
        "director_source": "pending",
        "director_model": "",
        "concepts": [],
        "status": "pending",
    }


def _apply_prompt_plan_to_report(report: dict[str, Any], plan: ImagePromptPlan) -> None:
    report["director_source"] = plan.source
    report["director_model"] = plan.director_model
    report["concepts"] = [
        {
            "image_index": concept.image_index,
            "purpose": concept.purpose,
            "photo_index": concept.photo_index,
            "prompt": concept.prompt,
        }
        for concept in plan.concepts
    ]
    report["status"] = "generating"


def _apply_generation_summary_to_report(
    report: dict[str, Any],
    *,
    generated: list[dict[str, Any]],
    requested_count: int,
    fallback_model: str,
) -> dict[str, Any]:
    summary = _aggregate_image_generation_cost(
        generated,
        requested_count=requested_count,
        fallback_model=fallback_model,
    )
    report["generation_model"] = summary["model"]
    report["cost_usd"] = summary["cost_usd"]
    report["generated_count"] = summary["image_count"]
    report["failed_count"] = summary["failed_count"]
    report["generated_images"] = [
        {
            "image_index": item["image_index"],
            "prompt_used": item["prompt_used"],
            "telegram_file_id": item["telegram_file_id"],
            "model": item.get("model"),
            "cost_usd": item.get("cost_usd", 0),
        }
        for item in generated
    ]
    report["status"] = "done" if summary["image_count"] else "failed"
    return summary


async def _save_image_report(
    db: Database,
    *,
    session_id: int,
    report: dict[str, Any],
) -> None:
    await db.update_image_session_report(session_id, _serialize_image_report(report))


async def _show_image_count_step(message: Any, context: Any, user_id: int) -> None:
    context.user_data["generation_step"] = "count"
    image_balance = await _get_db(context).get_image_balance(user_id)
    await message.reply_text(
        build_image_count_prompt(image_balance),
        reply_markup=build_image_count_keyboard(image_balance=image_balance),
    )


async def _show_image_guidance_step(message: Any, context: Any) -> None:
    context.user_data["generation_step"] = "image_guidance"
    await message.reply_text(
        IMAGE_GUIDANCE_PROMPT,
        reply_markup=build_image_guidance_keyboard(),
    )


async def _show_image_text_mode_step(message: Any, context: Any) -> None:
    context.user_data["generation_step"] = "image_text_mode"
    await message.reply_text(
        IMAGE_TEXT_MODE_PROMPT,
        reply_markup=build_image_text_mode_keyboard(),
    )


async def _show_image_style_step(message: Any, context: Any) -> None:
    context.user_data["generation_step"] = "image_style"
    await message.reply_text(
        IMAGE_STYLE_PROMPT,
        reply_markup=build_image_style_keyboard(),
    )


async def _continue_after_image_guidance(update: Any, context: Any, user_id: int) -> None:
    await _show_image_text_mode_step(update.effective_message, context)


async def _continue_after_image_text_mode(update: Any, context: Any, user_id: int) -> None:
    await _show_image_style_step(update.effective_message, context)


async def _continue_after_image_style(update: Any, context: Any, user_id: int) -> None:
    query = getattr(update, "callback_query", None)
    if context.user_data.get("repeat_images_count"):
        images_count = int(context.user_data.pop("repeat_images_count"))
        if not is_allowed_image_count(images_count):
            await _show_image_count_step(update.effective_message, context, user_id)
            return
        context.user_data["img_count"] = images_count
        generation_update = update
        if query is None:
            generation_update = SimpleNamespace(
                callback_query=SimpleNamespace(message=update.effective_message),
                effective_message=update.effective_message,
            )
        if should_generate_text_with_images(context.user_data.get("mode")):
            await _generate_text_and_images_for_user(generation_update, context, user_id, images_count)
        else:
            await _generate_images_for_user(generation_update, context, user_id, images_count)
        return
    images_count = int(context.user_data.get("img_count") or 0)
    if not is_allowed_image_count(images_count):
        await _show_image_count_step(update.effective_message, context, user_id)
        return
    if should_generate_text_with_images(context.user_data.get("mode")):
        await _generate_text_and_images_for_user(update, context, user_id, images_count)
    else:
        await _generate_images_for_user(update, context, user_id, images_count)


async def _handle_image_guidance(update: Any, context: Any, user_id: int, user_input: str) -> bool:
    if context.user_data.get("generation_step") != "image_guidance":
        return False
    if context.user_data.get("mode") not in {"text_and_images", "images_only"}:
        return False

    guidance = _normalize_image_guidance_text(user_input)
    if len(guidance) < 3:
        await update.effective_message.reply_text(
            IMAGE_GUIDANCE_PROMPT,
            reply_markup=build_image_guidance_keyboard(),
        )
        return True

    context.user_data["img_guidance"] = guidance
    await _continue_after_image_guidance(update, context, user_id)
    return True


async def _handle_image_style_custom(update: Any, context: Any, user_id: int, user_input: str) -> bool:
    if not context.user_data.get("awaiting_image_style_custom"):
        return False
    if context.user_data.get("mode") not in {"text_and_images", "images_only"}:
        return False

    style = normalize_image_style_custom(user_input)
    if len(style) < 3:
        await update.effective_message.reply_text(IMAGE_STYLE_CUSTOM_PROMPT)
        return True

    context.user_data.pop("awaiting_image_style_custom", None)
    context.user_data["img_style_preset"] = ""
    context.user_data["img_style_custom"] = style
    await _continue_after_image_style(update, context, user_id)
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
    if len(photos) >= MAX_REFERENCE_PHOTOS:
        await message.reply_text(
            f"📸 Максимум {MAX_REFERENCE_PHOTOS} фото.\nНажмите ✅ Готово",
            reply_markup=build_image_photo_keyboard(len(photos)),
        )
        return

    file_id = extract_image_file_id(message)
    if not file_id:
        await message.reply_text(
            "📸 Пришлите фото товара или изображение файлом.",
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
    image_guidance = str(context.user_data.get("img_guidance") or "")
    image_text_mode = normalize_image_text_mode(context.user_data.get("img_text_mode"))
    image_style_preset = normalize_image_style_preset(context.user_data.get("img_style_preset"))
    image_style_custom = normalize_image_style_custom(context.user_data.get("img_style_custom"))

    if not marketplace or not product_description or not photo_file_ids:
        await message.reply_text(
            "⚠️ Сессия генерации изображений устарела.\nНачните заново.",
            reply_markup=build_after_image_generation_keyboard(),
        )
        _clear_image_session(context)
        return

    current_balance = await db.get_image_balance(user_id)
    if current_balance < images_count:
        missing = images_count - current_balance
        await message.reply_text(
            f"⚠️ Не хватает изображений на балансе: {missing}.\nПополните баланс:",
            reply_markup=build_image_packages_keyboard(),
        )
        return

    report = _build_image_report_base(
        generation_mode="images_only",
        marketplace=marketplace,
        product_description=product_description,
        photo_file_ids=photo_file_ids,
        images_count=images_count,
        image_guidance=image_guidance,
        image_text_mode=image_text_mode,
        image_style_preset=image_style_preset,
        image_style_custom=image_style_custom,
    )

    session_id = await db.create_image_session(
        user_id=user_id,
        product_description=product_description,
        marketplace=marketplace,
        photos_count=len(photo_file_ids),
        images_requested=images_count,
        report_json=_serialize_image_report(report),
    )

    await message.reply_text("⏳ Разрабатываю концепцию изображений...")
    try:
        prompt_plan = await generate_image_prompts(
            product_description=product_description,
            marketplace=marketplace,
            photos_count=len(photo_file_ids),
            images_count=images_count,
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            site_url=settings.site_url,
            image_guidance=image_guidance,
            image_text_mode=image_text_mode,
            image_style_preset=image_style_preset,
            image_style_custom=image_style_custom,
        )
        concepts = prompt_plan.concepts
        _apply_prompt_plan_to_report(report, prompt_plan)
        await db.update_image_session_prompts(
            session_id,
            _serialize_image_concepts(concepts),
            status="generating",
        )
        await _save_image_report(db, session_id=session_id, report=report)
    except Exception as exc:
        reason = classify_generation_error(exc)
        log_generation_error(exc, marketplace=marketplace, mode="images_only", reason=reason)
        await db.set_image_session_status(session_id, "failed")
        report["status"] = "failed"
        report["error_reason"] = reason
        await _save_image_report(db, session_id=session_id, report=report)
        if reason in {"api_balance", "429"}:
            await message.reply_text(generation_error_message(reason))
        else:
            await message.reply_text(
                "⚠️ Не удалось разработать концепцию изображений.\nБаланс не списан."
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
        await _save_image_generation_cost_log(
            db,
            session_id=session_id,
            user_id=user_id,
            generated=generated,
            requested_count=images_count,
            fallback_model=settings.gpt_image_model,
        )
        _apply_generation_summary_to_report(
            report,
            generated=generated,
            requested_count=images_count,
            fallback_model=settings.gpt_image_model,
        )
        await _save_image_report(db, session_id=session_id, report=report)
    except Exception:
        logging.exception("Failed to save generated images")
        await db.set_image_session_status(session_id, "failed")
        report["status"] = "failed"
        report["error_reason"] = "save_error"
        await _save_image_report(db, session_id=session_id, report=report)
        await message.reply_text(
            "⚠️ Изображения отправлены, но историю сохранить не удалось.\nБаланс не списан."
        )
        return

    await message.reply_text(
        f"✅ Готово: {len(generated)} изображений для карточки.\n"
        f"Остаток: {image_balance} изображений.",
        reply_markup=build_after_image_generation_keyboard(),
    )
    _store_last_generation(
        context,
        marketplace=marketplace,
        mode="images_only",
        description=product_description,
        photo_file_ids=photo_file_ids,
        images_count=images_count,
        image_guidance=image_guidance,
        image_text_mode=image_text_mode,
        image_style_preset=image_style_preset,
        image_style_custom=image_style_custom,
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
    image_guidance = str(context.user_data.get("img_guidance") or "")
    image_text_mode = normalize_image_text_mode(context.user_data.get("img_text_mode"))
    image_style_preset = normalize_image_style_preset(context.user_data.get("img_style_preset"))
    image_style_custom = normalize_image_style_custom(context.user_data.get("img_style_custom"))

    if not marketplace or not product_description or not photo_file_ids:
        await message.reply_text(
            "⚠️ Сессия генерации устарела.\nНачните заново.",
            reply_markup=build_after_image_generation_keyboard(),
        )
        _clear_image_session(context)
        return

    usage_mode = await db.get_usage_mode(user_id, trial_generations=settings.trial_generations)
    if usage_mode is UsageMode.BLOCKED:
        await message.reply_text(
            "⚠️ Бесплатные генерации закончились.\nКупите пакет, чтобы продолжить.",
            reply_markup=build_buy_keyboard(),
        )
        return

    current_image_balance = await db.get_image_balance(user_id)
    if current_image_balance < images_count:
        await message.reply_text(
            f"⚠️ Не хватает изображений на балансе: {images_count - current_image_balance}.",
            reply_markup=build_image_packages_keyboard(),
        )
        return

    report = _build_image_report_base(
        generation_mode="text_and_images",
        marketplace=marketplace,
        product_description=product_description,
        photo_file_ids=photo_file_ids,
        images_count=images_count,
        image_guidance=image_guidance,
        image_text_mode=image_text_mode,
        image_style_preset=image_style_preset,
        image_style_custom=image_style_custom,
    )

    session_id = await db.create_image_session(
        user_id=user_id,
        product_description=product_description,
        marketplace=marketplace,
        photos_count=len(photo_file_ids),
        images_requested=images_count,
        report_json=_serialize_image_report(report),
    )

    await message.reply_text("⏳ Генерирую карточку...")
    category_profile, resolved_fields = await _resolve_generation_enrichment(
        context,
        product_description,
        marketplace,
        has_photo=True,
    )
    card_task = asyncio.create_task(
        generate_card(
            product_description,
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            site_url=settings.site_url,
            marketplace=marketplace,
            category_profile=category_profile,
            resolved_fields=resolved_fields,
        )
    )
    concepts_task = asyncio.create_task(
        _generate_image_prompts_for_batch(
            settings=settings,
            product_description=product_description,
            marketplace=marketplace,
            photo_file_ids=photo_file_ids,
            images_count=images_count,
            image_guidance=image_guidance,
            image_text_mode=image_text_mode,
            image_style_preset=image_style_preset,
            image_style_custom=image_style_custom,
        )
    )

    try:
        card = await card_task
    except Exception as exc:
        await _cancel_task(concepts_task)
        await db.set_image_session_status(session_id, "failed")
        reason = classify_generation_error(exc)
        log_generation_error(exc, marketplace=marketplace, mode="text_and_images", reason=reason)
        report["status"] = "failed"
        report["error_reason"] = reason
        await _save_image_report(db, session_id=session_id, report=report)
        await message.reply_text(generation_error_message(reason))
        return

    try:
        await db.save_successful_generation(
            user_id,
            product_description,
            card,
            usage_mode,
            trial_generations=settings.trial_generations,
        )
    except Exception as exc:
        await _cancel_task(concepts_task)
        await db.set_image_session_status(session_id, "failed")
        log_generation_error(
            exc,
            marketplace=marketplace,
            mode="text_and_images",
            reason="save_error",
        )
        report["status"] = "failed"
        report["error_reason"] = "save_error"
        await _save_image_report(db, session_id=session_id, report=report)
        await message.reply_text(
            "⚠️ Карточка создана, но историю сохранить не удалось.\nБаланс изображений не списан."
        )
        return

    await message.reply_text("✅ Текстовая карточка готова:")
    for text in build_generation_messages(card):
        await message.reply_text(text)
    await message.reply_text("🖼 Генерирую изображения.\nОбычно это занимает 1-2 минуты.")

    try:
        prompt_plan = await concepts_task
        concepts = prompt_plan.concepts
        _apply_prompt_plan_to_report(report, prompt_plan)
        await db.update_image_session_prompts(
            session_id,
            _serialize_image_concepts(concepts),
            status="generating",
        )
        await _save_image_report(db, session_id=session_id, report=report)
    except Exception as exc:
        reason = classify_generation_error(exc)
        log_generation_error(exc, marketplace=marketplace, mode="text_and_images", reason=reason)
        await db.set_image_session_status(session_id, "failed")
        report["status"] = "failed"
        report["error_reason"] = reason
        await _save_image_report(db, session_id=session_id, report=report)
        balance = await db.get_balance(user_id)
        text_left = max(settings.trial_generations - balance.trial_used, 0) + balance.balance
        if reason in {"api_balance", "429"}:
            await message.reply_text(
                f"{generation_error_message(reason)}\n"
                f"\nСписана только текстовая генерация.\n"
                f"Остаток: {text_left} текстовых / {balance.image_balance} изображений.",
                reply_markup=build_after_image_generation_keyboard(),
            )
        else:
            await message.reply_text(
                "⚠️ Не удалось разработать концепцию изображений.\n"
                "Списана только текстовая генерация.\n"
                f"Остаток: {text_left} текстовых / {balance.image_balance} изображений.",
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
        await _save_image_generation_cost_log(
            db,
            session_id=session_id,
            user_id=user_id,
            generated=generated,
            requested_count=images_count,
            fallback_model=settings.gpt_image_model,
        )
        _apply_generation_summary_to_report(
            report,
            generated=generated,
            requested_count=images_count,
            fallback_model=settings.gpt_image_model,
        )
        await _save_image_report(db, session_id=session_id, report=report)
    except Exception:
        logging.exception("Failed to save generated images")
        await db.set_image_session_status(session_id, "failed")
        report["status"] = "failed"
        report["error_reason"] = "save_error"
        await _save_image_report(db, session_id=session_id, report=report)
        await message.reply_text(
            "⚠️ Изображения отправлены, но историю сохранить не удалось.\nБаланс изображений не списан."
        )
        return

    balance = await db.get_balance(user_id)
    text_left = max(settings.trial_generations - balance.trial_used, 0) + balance.balance
    await message.reply_text(
        f"✅ Готово: текст и {len(generated)} изображений.\n\n"
        f"Потрачено: 1 текстовая генерация + {len(generated)} изображений.\n"
        f"Остаток: {text_left} текстовых / {image_balance} изображений.",
        reply_markup=build_after_image_generation_keyboard(),
    )
    _store_last_generation(
        context,
        marketplace=marketplace,
        mode="text_and_images",
        description=product_description,
        photo_file_ids=photo_file_ids,
        images_count=images_count,
        image_guidance=image_guidance,
        image_text_mode=image_text_mode,
        image_style_preset=image_style_preset,
        image_style_custom=image_style_custom,
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


async def _generate_image_prompts_for_batch(
    *,
    settings: Settings,
    product_description: str,
    marketplace: str,
    photo_file_ids: list[str],
    images_count: int,
    image_guidance: str | None = None,
    image_text_mode: str | None = None,
    image_style_preset: str | None = None,
    image_style_custom: str | None = None,
) -> ImagePromptPlan:
    return await generate_image_prompts(
        product_description=product_description,
        marketplace=marketplace,
        photos_count=len(photo_file_ids),
        images_count=images_count,
        api_key=settings.openrouter_api_key,
        model=settings.openrouter_model,
        site_url=settings.site_url,
        image_guidance=image_guidance,
        image_text_mode=image_text_mode,
        image_style_preset=image_style_preset,
        image_style_custom=image_style_custom,
    )


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
    generated_count = 0
    sent_count = 0
    stop_progress = asyncio.Event()
    progress_task = asyncio.create_task(
        _image_generation_heartbeat(
            status_message=status_message,
            total_count=total_count,
            get_counts=lambda: (generated_count, sent_count),
            stop_event=stop_progress,
        )
    )

    batch_results = []
    try:
        batch_results = await asyncio.wait_for(
            generate_marketplace_batch_image_results(
                concepts=[
                    ImageBatchConcept(
                        image_index=int(concept.image_index),
                        purpose=str(concept.purpose),
                        prompt=str(concept.prompt),
                    )
                    for concept in concepts
                ],
                reference_photo_file_ids=photo_file_ids,
                bot=context.bot,
                api_key=settings.openrouter_api_key,
                model=settings.gpt_image_model,
                site_url=settings.site_url,
            ),
            timeout=420,
        )
    except Exception as exc:
        reason = classify_generation_error(exc)
        logging.warning("Batch image generation failed reason=%s: %s", reason, exc)
        if reason in {"api_balance", "429"}:
            await message.reply_text(generation_error_message(reason))
        else:
            for concept in concepts:
                await message.reply_text(
                    f"Изображение {int(concept.image_index)}/{total_count} не удалось сгенерировать."
                )
    else:
        generated_count = len(batch_results)
        for concept, image_result in zip(concepts, batch_results):
            image_index = int(concept.image_index)
            try:
                image_record = await _send_generated_image_result(
                    message,
                    {
                        "image_index": image_index,
                        "purpose": concept.purpose,
                        "prompt_used": concept.prompt,
                        "image_bytes": image_result.image_bytes,
                        "model": image_result.usage.model,
                        "cost_usd": image_result.usage.cost_usd,
                    },
                )
            except Exception as exc:
                logging.warning("Failed to send generated image %s: %s", image_index, exc)
                await message.reply_text(
                    f"Изображение {image_index}/{total_count} не удалось отправить."
                )
                continue
            generated.append(image_record)
            sent_count += 1
            await _safe_edit_message_text(
                status_message,
                build_image_progress_message(total_count, generated_count, sent_count),
            )
    finally:
        stop_progress.set()
        await progress_task

    return generated


def _aggregate_image_generation_cost(
    generated: list[dict[str, Any]],
    requested_count: int,
    fallback_model: str,
) -> dict[str, Any]:
    model_costs: dict[str, float] = {}
    for item in generated:
        model = str(item.get("model") or fallback_model).strip() or fallback_model
        model_costs[model] = model_costs.get(model, 0.0) + float(item.get("cost_usd") or 0)

    if model_costs:
        model = max(model_costs.items(), key=lambda entry: entry[1])[0]
    else:
        model = fallback_model

    return {
        "model": model,
        "cost_usd": round(sum(model_costs.values()), 6),
        "image_count": len(generated),
        "failed_count": max(0, int(requested_count) - len(generated)),
    }


async def _save_image_generation_cost_log(
    db: Database,
    *,
    session_id: int,
    user_id: int,
    generated: list[dict[str, Any]],
    requested_count: int,
    fallback_model: str,
) -> None:
    summary = _aggregate_image_generation_cost(
        generated,
        requested_count=requested_count,
        fallback_model=fallback_model,
    )
    try:
        await db.save_image_generation_cost(
            session_id=session_id,
            user_id=user_id,
            model=summary["model"],
            cost_usd=summary["cost_usd"],
            image_count=summary["image_count"],
            failed_count=summary["failed_count"],
        )
        logging.info(
            "Image generation cost: session_id=%s user_id=%s model=%s cost_usd=%.6f image_count=%s failed_count=%s",
            session_id,
            user_id,
            summary["model"],
            summary["cost_usd"],
            summary["image_count"],
            summary["failed_count"],
        )
    except Exception:
        logging.exception("Failed to save image generation cost")


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
        "model": result.get("model"),
        "cost_usd": result.get("cost_usd", 0),
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
            "⚠️ Бесплатные генерации закончились.\nКупите пакет, чтобы продолжить.",
            reply_markup=build_buy_keyboard(),
        )
        return None

    if intro_text:
        await message.reply_text(intro_text)

    try:
        category_profile, resolved_fields = await _resolve_generation_enrichment(
            context,
            user_input,
            marketplace,
            has_photo=False,
        )
        card = await generate_card(
            user_input,
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            site_url=settings.site_url,
            marketplace=marketplace,
            category_profile=category_profile,
            resolved_fields=resolved_fields,
        )
    except Exception as exc:
        reason = classify_generation_error(exc)
        log_generation_error(exc, marketplace=marketplace, mode=mode, reason=reason)
        await message.reply_text(generation_error_message(reason))
        return None

    try:
        await db.save_successful_generation(
            user_id,
            user_input,
            card,
            usage_mode,
            trial_generations=settings.trial_generations,
        )
    except Exception as exc:
        log_generation_error(
            exc,
            marketplace=marketplace,
            mode=mode,
            reason="save_error",
        )
        await message.reply_text(
            "⚠️ Карточка создана, но историю сохранить не удалось.\nПопробуйте позже."
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
        await update.effective_message.reply_text("⚠️ Нет данных последней генерации для сохранения.")
        return True

    count = await _get_db(context).get_templates_count(user_id)
    if count >= TEMPLATES_LIMIT:
        await update.effective_message.reply_text(
            "⚠️ У вас уже 10 шаблонов — это максимум.\nУдалите старый шаблон, чтобы сохранить новый."
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
        image_guidance=last_generation.get("image_guidance") or "",
        image_text_mode=last_generation.get("image_text_mode") or "",
        image_style_preset=last_generation.get("image_style_preset") or "",
        image_style_custom=last_generation.get("image_style_custom") or "",
    )
    await update.effective_message.reply_text(
        f"✅ Шаблон \"{name}\" сохранён.\nНайдёте его в «Мои шаблоны»."
    )
    return True


async def _handle_new_template_name(update: Any, context: Any, user_id: int, user_input: str) -> bool:
    if not context.user_data.get("awaiting_new_template_name"):
        return False

    context.user_data.pop("awaiting_new_template_name", None)
    context.user_data["new_template_name"] = truncate_template_name(user_input)
    context.user_data["awaiting_new_template_text"] = True
    await update.effective_message.reply_text(NEW_TEMPLATE_TEXT_PROMPT)
    return True


async def _handle_new_template_text(update: Any, context: Any, user_id: int, user_input: str) -> bool:
    if not context.user_data.get("awaiting_new_template_text"):
        return False

    context.user_data.pop("awaiting_new_template_text", None)
    name = context.user_data.pop("new_template_name", None) or "Шаблон"
    count = await _get_db(context).get_templates_count(user_id)
    if count >= TEMPLATES_LIMIT:
        await update.effective_message.reply_text(
            "⚠️ У вас уже 10 шаблонов — это максимум.\nУдалите старый шаблон, чтобы сохранить новый."
        )
        return True

    await _get_db(context).save_template(
        user_id=user_id,
        name=name,
        marketplace="wb",
        mode="text_only",
        description=user_input,
        photo_file_ids=[],
        images_count=None,
    )
    await update.effective_message.reply_text(
        f"✅ Шаблон \"{name}\" сохранён.\nНайдёте его в «Мои шаблоны»."
    )
    return True


async def _handle_repeat_changes(update: Any, context: Any, user_id: int, user_input: str) -> bool:
    if not context.user_data.get("awaiting_repeat_changes"):
        return False

    context.user_data.pop("awaiting_repeat_changes", None)
    previous = context.user_data.get("last_generation")
    if not previous:
        await update.effective_message.reply_text("⚠️ Нет предыдущей генерации для повтора.")
        return True

    combined_description = combine_repeat_description(previous["description"], user_input)
    marketplace = previous["marketplace"]
    if previous["mode"] in {"text_and_images", "images_only"}:
        context.user_data["repeat_pending_generation"] = {
            "marketplace": marketplace,
            "mode": previous["mode"],
            "description": combined_description,
            "photo_file_ids": list(previous.get("photo_file_ids") or []),
            "images_count": previous.get("images_count") or 1,
            "image_guidance": previous.get("image_guidance") or "",
            "image_text_mode": previous.get("image_text_mode") or "minimal",
            "image_style_preset": previous.get("image_style_preset") or "",
            "image_style_custom": previous.get("image_style_custom") or "",
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
    photo_file_ids = list(generation.get("photo_file_ids") or [])[:MAX_REFERENCE_PHOTOS]
    images_count = int(generation.get("images_count") or 1)
    if not photo_file_ids:
        await update.callback_query.message.reply_text(
            "В шаблоне нет сохранённых фото. Загрузите новые фото для генерации."
        )
        context.user_data["marketplace"] = generation["marketplace"]
        context.user_data["mode"] = generation["mode"]
        context.user_data["img_description"] = generation["description"]
        context.user_data["img_photos"] = []
        context.user_data["img_guidance"] = generation.get("image_guidance") or ""
        context.user_data["img_text_mode"] = generation.get("image_text_mode") or "minimal"
        context.user_data["img_style_preset"] = generation.get("image_style_preset") or ""
        context.user_data["img_style_custom"] = generation.get("image_style_custom") or ""
        context.user_data["generation_step"] = "photos"
        context.user_data["repeat_images_count"] = images_count
        await update.callback_query.message.reply_text(IMAGE_PHOTO_PROMPT)
        return

    context.user_data["marketplace"] = generation["marketplace"]
    context.user_data["mode"] = generation["mode"]
    context.user_data["img_description"] = generation["description"]
    context.user_data["img_photos"] = photo_file_ids
    context.user_data["img_guidance"] = generation.get("image_guidance") or ""
    context.user_data["img_text_mode"] = generation.get("image_text_mode") or "minimal"
    context.user_data["img_style_preset"] = generation.get("image_style_preset") or ""
    context.user_data["img_style_custom"] = generation.get("image_style_custom") or ""
    if not is_allowed_image_count(images_count):
        context.user_data["generation_step"] = "count"
        image_balance = await _get_db(context).get_image_balance(user_id)
        await update.callback_query.message.reply_text(
            build_image_count_prompt(image_balance),
            reply_markup=build_image_count_keyboard(image_balance=image_balance),
        )
        return
    context.user_data["img_count"] = images_count
    if should_generate_text_with_images(generation["mode"]):
        await _generate_text_and_images_for_user(update, context, user_id, images_count)
    else:
        await _generate_images_for_user(update, context, user_id, images_count)


async def _run_saved_generation(
    update: Any,
    context: Any,
    user_id: int,
    generation: dict[str, Any],
) -> None:
    if generation["mode"] in {"text_and_images", "images_only"}:
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


async def _handle_reply_action(update: Any, context: Any, user_id: int, action: str) -> None:
    if action == "home":
        user = update.effective_user
        await _show_home(
            update.effective_message,
            context,
            user.first_name if user else None,
        )
        return
    if action == "generate":
        await generate_command(update, context)
        return
    if action == "buy":
        await _show_buy_menu(update.effective_message, context, user_id, kind="all")
        return
    if action == "balance":
        await balance_command(update, context)
        return
    if action == "templates":
        await _show_templates(update.effective_message, context, user_id, page=0)
        return
    if action == "history":
        await history_command(update, context)
        return
    if action == "help":
        await help_command(update, context)


async def handle_text(update: Any, context: Any) -> None:
    user_id = await _ensure_user(update, context)
    if user_id is None or update.effective_message is None:
        return

    user_input = (update.effective_message.text or "").strip()
    reply_action = classify_reply_action(user_input)
    if reply_action is not None:
        await _handle_reply_action(update, context, user_id, reply_action)
        return

    if await _handle_new_template_name(update, context, user_id, user_input):
        return
    if await _handle_new_template_text(update, context, user_id, user_input):
        return
    if await _handle_template_name(update, context, user_id, user_input):
        return
    if await _handle_repeat_changes(update, context, user_id, user_input):
        return
    if await _handle_image_style_custom(update, context, user_id, user_input):
        return
    if await _handle_image_guidance(update, context, user_id, user_input):
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
            "⚠️ Добавьте хотя бы название или категорию товара."
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
    if data == HOME_CALLBACK:
        user = update.effective_user
        await _show_home(query.message, context, user.first_name if user else None)
    elif data == "action:generate":
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
        if mode not in {"text_only", "text_and_images", "images_only"}:
            await query.message.reply_text(
                MODE_PROMPT,
                reply_markup=build_generation_mode_keyboard(),
            )
            return
        context.user_data["mode"] = mode
        if mode in {"text_and_images", "images_only"}:
            user = update.effective_user
            if user is None:
                return
            image_balance = await _get_db(context).get_image_balance(user.id)
            if image_balance <= 0:
                await query.message.reply_text(
                    "⚠️ На балансе нет изображений.\n"
                    "Купите пакет изображений, чтобы использовать этот режим.",
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
        user = update.effective_user
        if user is None:
            return
        photos = list(context.user_data.get("img_photos") or [])
        if not photos:
            await query.message.reply_text(IMAGE_PHOTO_PROMPT)
            return
        await _show_image_count_step(query.message, context, user.id)
    elif data == "img_guidance_write":
        await _show_image_guidance_step(query.message, context)
    elif data == "img_guidance_skip":
        user = update.effective_user
        if user is None:
            return
        context.user_data["img_guidance"] = ""
        await _continue_after_image_guidance(update, context, user.id)
    elif data.startswith("img_text_mode:"):
        user = update.effective_user
        if user is None:
            return
        text_mode_value = data.split(":", 1)[1]
        if text_mode_value == "skip":
            context.user_data["img_text_mode"] = ""
        else:
            context.user_data["img_text_mode"] = normalize_image_text_mode(text_mode_value)
        await _continue_after_image_text_mode(update, context, user.id)
    elif data.startswith("img_style:"):
        user = update.effective_user
        if user is None:
            return
        style_value = data.split(":", 1)[1]
        if style_value == "custom":
            context.user_data["generation_step"] = "image_style"
            context.user_data["awaiting_image_style_custom"] = True
            await query.message.reply_text(IMAGE_STYLE_CUSTOM_PROMPT)
            return
        if style_value == "skip":
            context.user_data["img_style_preset"] = ""
            context.user_data["img_style_custom"] = ""
            await _continue_after_image_style(update, context, user.id)
            return
        context.user_data["img_style_preset"] = normalize_image_style_preset(style_value)
        context.user_data["img_style_custom"] = ""
        await _continue_after_image_style(update, context, user.id)
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
        if not is_allowed_image_count(images_count):
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
        await _show_image_guidance_step(query.message, context)
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
    elif data == "action:feedback":
        await query.message.reply_text(FEEDBACK_MESSAGE)
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
            await query.message.reply_text("⚠️ Нет данных последней генерации для сохранения.")
            return
        count = await _get_db(context).get_templates_count(user_id)
        if count >= TEMPLATES_LIMIT:
            await query.answer(
                "У вас уже 10 шаблонов — это максимум. Удалите старый шаблон, чтобы сохранить новый.",
                show_alert=True,
            )
            return
        await query.answer()
        context.user_data["awaiting_template_name"] = True
        await query.message.reply_text(TEMPLATE_NAME_PROMPT)
    elif data == "action:repeat_edit":
        if not context.user_data.get("last_generation"):
            await query.message.reply_text("⚠️ Нет предыдущей генерации для повтора.")
            return
        context.user_data["awaiting_repeat_changes"] = True
        await query.message.reply_text(REPEAT_CHANGES_PROMPT)
    elif data.startswith("repeat:"):
        if user_id is None:
            return
        pending = context.user_data.get("repeat_pending_generation")
        if not pending:
            await query.message.reply_text("⚠️ Сессия повтора устарела.\nНачните заново.")
            return
        repeat_mode = data.split(":", 1)[1]
        context.user_data["repeat_mode"] = repeat_mode
        if repeat_mode == "same_photos":
            await _run_last_generation_with_images(update, context, user_id, pending)
            return
        if repeat_mode == "new_photos":
            context.user_data["marketplace"] = pending["marketplace"]
            context.user_data["mode"] = pending["mode"]
            context.user_data["img_description"] = pending["description"]
            context.user_data["img_photos"] = []
            context.user_data["img_guidance"] = pending.get("image_guidance") or ""
            context.user_data["img_text_mode"] = pending.get("image_text_mode") or "minimal"
            context.user_data["img_style_preset"] = pending.get("image_style_preset") or ""
            context.user_data["img_style_custom"] = pending.get("image_style_custom") or ""
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
    elif data == "template_new":
        await _start_new_template_flow(query.message, context)
    elif data.startswith("template_use:"):
        if user_id is None:
            return
        try:
            template_id = int(data.split(":", 1)[1])
        except ValueError:
            return
        template = await _get_db(context).get_template(template_id, user_id)
        if not template:
            await query.message.reply_text("⚠️ Шаблон не найден.")
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
            await query.message.reply_text("⚠️ Шаблон не найден.")
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
            await query.message.reply_text("⚠️ Шаблон не найден.")
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
            await query.message.reply_text("⚠️ Шаблон не найден.")
            return
        await query.message.reply_text(
            f"🗑 Удалить шаблон \"{template['name']}\"?",
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
        await query.message.reply_text("✅ Удаление отменено.")
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
            f"🖼 {text_count} карточек: выберите количество фото",
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
    await application.bot.delete_my_commands()


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
    application.bot_data["category_profiles"] = load_category_profiles()
    application.bot_data["ozon_categories"] = load_ozon_categories()
    application.bot_data["wb_category_profiles"] = load_wb_category_profiles()
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
