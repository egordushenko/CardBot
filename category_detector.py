from __future__ import annotations

import json
import os
import re
from pathlib import Path

from config import load_settings
from llm import OPENROUTER_BASE_URL


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ANALYSIS_PATH = BASE_DIR / "data" / "ozon_dataset_analysis.json"


class CategoryDetectionError(RuntimeError):
    pass


def load_ozon_categories(path: str | Path = DEFAULT_ANALYSIS_PATH) -> list[str]:
    analysis_path = Path(path)
    data = json.loads(analysis_path.read_text(encoding="utf-8"))
    categories = data.get("categories")
    if not isinstance(categories, dict) or not categories:
        raise CategoryDetectionError("Ozon analysis file does not contain categories")
    return [str(category) for category in categories.keys()]


def _normalize_category(raw_category: str, categories: list[str]) -> str | None:
    value = raw_category.strip().strip('"').strip("'")
    if value in categories:
        return value

    value_lower = value.casefold()
    for category in categories:
        if category.casefold() == value_lower:
            return category

    for category in categories:
        if category.casefold() in value_lower:
            return category
    return None


_KEYWORD_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Автотовары", ("авто", "машин", "lada", "toyota", "коврик", "щетка стеклоочистителя")),
    ("Аптека", ("аптеч", "лекар", "витамин", "таблет", "капсул", "бинт")),
    ("Бытовая техника", ("пылесос", "чайник", "микроволнов", "блендер", "утюг", "кофемашин")),
    ("Бытовая химия", ("стираль", "моющее", "чистящее", "порошок", "кондиционер для белья")),
    ("Бытовая химия и гигиена", ("гигиен", "салфетки", "подгузник", "зубная паста", "мыло")),
    ("Все для игр", ("игров", "геймпад", "настольная игра", "playstation", "xbox")),
    ("Детские товары", ("детск", "ребен", "малыш", "коляска", "игрушк")),
    ("Дом и сад", ("лампа", "светильник", "плед", "посуда", "сад", "декор")),
    ("Канцелярские товары", ("ручка", "карандаш", "тетрад", "блокнот", "канцеляр")),
    ("Книги", ("книга", "роман", "учебник", "комикс")),
    ("Красота и здоровье", ("крем", "сыворот", "шампун", "маска для лица", "кожа", "макияж")),
    ("Мебель", ("стол", "стул", "диван", "шкаф", "кровать", "полка")),
    ("Обувь", ("кроссов", "ботинки", "туфли", "сапоги", "кеды", "обув")),
    ("Одежда", ("платье", "футболка", "брюки", "куртка", "худи", "рубашка", "одеж")),
    ("Продукты питания", ("кофе", "чай", "шоколад", "крупа", "печенье", "соус")),
    ("Спорт и отдых", ("фитнес", "трениров", "гантели", "коврик для йоги", "спорт")),
    ("Спортивные товары", ("мяч", "велосипед", "лыжи", "тренажер", "эспандер")),
    ("Строительство и ремонт", ("розетка", "дрель", "шуруповерт", "краска", "строитель", "ремонт")),
    ("Товары для животных", ("кош", "собак", "корм", "наполнитель", "поводок", "зоотовар")),
    ("Туризм, рыбалка, охота", ("палатка", "рыбал", "спиннинг", "термос", "туризм", "охот")),
    ("Хобби и творчество", ("набор для творчества", "пряжа", "рисован", "алмазная мозаика", "хобби")),
    ("Цифровые товары", ("подписка", "ключ активации", "цифров", "промокод")),
    ("Электроника", ("наушник", "bluetooth", "смартфон", "кабель", "заряд", "планшет")),
    ("Ювелирные украшения", ("кольцо", "серьги", "браслет", "цепочка", "ювелир")),
)


def _heuristic_detect_category(product_description: str, categories: list[str]) -> str:
    text = product_description.casefold()
    best_category = ""
    best_score = 0

    for category, keywords in _KEYWORD_RULES:
        if category not in categories:
            continue
        score = sum(1 for keyword in keywords if keyword.casefold() in text)
        if score > best_score:
            best_category = category
            best_score = score

    if best_category:
        return best_category
    return categories[0]


def _extract_category_from_response(content: str, categories: list[str]) -> str | None:
    text = content.strip()
    if not text:
        return None

    with_json = text
    if text.startswith("```"):
        with_json = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE | re.DOTALL)

    try:
        payload = json.loads(with_json)
    except json.JSONDecodeError:
        return _normalize_category(text, categories)

    if isinstance(payload, dict):
        raw_category = str(payload.get("category") or "")
        return _normalize_category(raw_category, categories)
    if isinstance(payload, str):
        return _normalize_category(payload, categories)
    return None


def _detect_category_llm(
    product_description: str,
    categories: list[str],
    *,
    api_key: str,
    model: str,
    site_url: str,
) -> str | None:
    from openai import OpenAI

    client = OpenAI(
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
        timeout=20.0,
        max_retries=1,
        default_headers={
            "HTTP-Referer": site_url,
            "X-Title": "CardBot",
        },
    )
    categories_text = "\n".join(f"- {category}" for category in categories)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты классифицируешь товар строго в одну категорию Ozon. "
                    "Верни только JSON вида {\"category\":\"...\"}. "
                    "Название категории должно полностью совпадать со списком."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Категории:\n{categories_text}\n\n"
                    f"Описание товара:\n{product_description.strip()}"
                ),
            },
        ],
        max_tokens=80,
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or ""
    return _extract_category_from_response(content, categories)


def detect_category(product_description: str) -> str:
    categories = load_ozon_categories()
    description = product_description.strip()
    if not description:
        return categories[0]

    if os.environ.get("CARDBOT_DISABLE_LLM_CATEGORY") == "1":
        return _heuristic_detect_category(description, categories)

    settings = load_settings()
    api_key = settings.openrouter_api_key.strip()
    if api_key:
        try:
            detected = _detect_category_llm(
                description,
                categories,
                api_key=api_key,
                model=settings.openrouter_model,
                site_url=settings.site_url,
            )
            if detected:
                return detected
        except Exception:
            pass

    return _heuristic_detect_category(description, categories)
