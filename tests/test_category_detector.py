from __future__ import annotations

from category_detector import detect_category


def test_detect_category_uses_known_categories_for_different_products(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("CARDBOT_DISABLE_LLM_CATEGORY", "1")

    cases = [
        ("увлажняющий крем для лица для сухой кожи 50 мл", "Красота и здоровье"),
        ("платье женское летнее хлопок размер 44 цвет синий", "Одежда"),
        ("беспроводные bluetooth наушники с шумоподавлением", "Электроника"),
        ("резиновые автомобильные коврики Lada Granta комплект", "Автотовары"),
        ("сухой корм для кошек с курицей 2 кг", "Товары для животных"),
    ]

    for description, expected in cases:
        assert detect_category(description) == expected
