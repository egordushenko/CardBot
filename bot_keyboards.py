from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from payments import (
    IMAGE_ADDON_CODES,
    MAIN_PACKAGE_CODES,
    PACKAGES as PAYMENT_PACKAGES,
    PROMO_PACKAGE_CODE,
    TEXT_ADDON_CODES,
)


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
    if sent_count <= 0:
        estimated_minutes = max(2, total_count * 2)
        suffix = "\nЗапрос еще выполняется." if still_working else ""
        return (
            f"🎨 Генерирую {total_count} изображений.\n"
            f"Ориентир: около {estimated_minutes} минут.\n"
            f"Изображения придут вместе после завершения генерации."
            f"{suffix}"
        )
    return (
        "🎨 Отправляю изображения...\n"
        f"Отправлено: {sent_count} из {total_count}"
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


def build_help_keyboard(offer_url: str) -> Any:
    return _keyboard([[_url_button("Публичная оферта", offer_url)], [_home_button()]])
