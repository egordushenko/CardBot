from bot import (
    PAYMENT_UNAVAILABLE_MESSAGE,
    build_balance_message,
    build_buy_keyboard,
    build_generation_messages,
    build_marketplace_keyboard,
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


def test_build_balance_message_shows_trial_and_paid_balance():
    text = build_balance_message(trial_used=1, balance=7)

    assert f"Бесплатно осталось: {TRIAL_GENERATIONS - 1}" in text
    assert "Платных генераций: 7" in text


def test_buy_keyboard_contains_package_buttons_but_runtime_uses_stub_message():
    keyboard = build_buy_keyboard()

    assert PAYMENT_UNAVAILABLE_MESSAGE == "💳 Оплата временно недоступна, скоро откроем!"
    assert len(keyboard.inline_keyboard) == 3
    assert keyboard.inline_keyboard[0][0].callback_data == "buy:starter"
