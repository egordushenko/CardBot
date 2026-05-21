from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


DEFAULT_DATASET_PATH = "data/wb_cards_dataset.json"
DEFAULT_OUTPUT_PATH = "data/wb_category_profiles.json"

TITLE_FORMULAS = {
    "Женщинам": "тип + крой/посадка + материал/сезон + назначение",
    "Мужчинам": "тип + базовость/крой + материал/рукав/сезон",
    "Детям": "тип + возраст/назначение + комплектность",
    "Обувь": "тип обуви + пол + сезон/материал + подошва/застежка",
    "Дом": "тип + зона применения + материал/свойство + размер/количество",
    "Электроника": "тип + модель + ключевая спецификация + цвет",
    "Бытовая техника": "тип + назначение + мощность/объем/программа + модель",
    "Красота": "тип средства + действие/зона + объем/количество",
    "Здоровье": "форма + назначение + активный компонент + объем/количество",
    "Продукты питания": "тип + вкус/форма + количество/вес",
    "Строительство и ремонт": "тип + материал + размер + комплектация",
    "Игрушки": "тип + механика/назначение + персонаж/размер",
    "Аксессуары": "тип аксессуара + материал/форма + количество/размер",
}

DESCRIPTION_TARGETS = {
    "Женщинам": (700, 1200),
    "Мужчинам": (700, 1200),
    "Детям": (700, 1200),
    "Обувь": (700, 1200),
    "Аксессуары": (600, 1100),
    "Дом": (900, 1400),
    "Игрушки": (900, 1400),
    "Электроника": (900, 1400),
    "Бытовая техника": (900, 1400),
    "Строительство и ремонт": (900, 1400),
    "Красота": (1000, 1800),
    "Здоровье": (1000, 1800),
    "Продукты питания": (600, 1000),
}


def _top_category(card: dict[str, Any]) -> str:
    return str(card.get("category") or "").split(" / ", 1)[0].strip() or "Без категории"


def _profile_category(card: dict[str, Any]) -> str:
    source = str(card.get("source_category") or "").strip()
    category = str(card.get("category") or "").strip()
    if source and "/" in source:
        normalized_source = source.replace("\\", "/").strip("/")
        if not re.search(r"[a-z]", normalized_source, flags=re.IGNORECASE):
            return " / ".join(part for part in normalized_source.split("/") if part)
    return category or _top_category(card)


def _parent_category(category: str) -> str:
    return category.split(" / ", 1)[0].strip() or category


def _words(value: str) -> list[str]:
    return [
        token.lower()
        for token in re.findall(r"[A-Za-zА-Яа-яЁё0-9]{3,}", value)
        if not token.isdigit()
    ]


def _source_keywords(source_category: str) -> list[str]:
    raw = source_category.replace("https://www.wildberries.ru/catalog/", "")
    parts = re.split(r"[/_-]+", raw.lower())
    stop = {"catalog", "vse", "dlya", "i", "ru", "sort", "popular"}
    return [part for part in parts if len(part) >= 3 and part not in stop and not part.isdigit()]


def _number_stats(values: list[int]) -> tuple[float, int, int]:
    if not values:
        return 0.0, 0, 0
    return round(mean(values), 1), min(values), max(values)


def _characteristic_targets(parent: str, avg_count: float) -> tuple[int, int]:
    if parent in {"Электроника", "Бытовая техника", "Строительство и ремонт"}:
        return max(18, round(avg_count * 0.75)), max(24, round(avg_count * 1.15))
    if parent in {"Дом", "Обувь", "Продукты питания"}:
        return max(12, round(avg_count * 0.75)), max(18, round(avg_count * 1.15))
    return max(8, min(12, round(avg_count * 0.75))), max(14, round(avg_count * 1.2))


def _build_profile(category: str, cards: list[dict[str, Any]]) -> dict[str, Any]:
    parent = _parent_category(category)
    field_counts: Counter[str] = Counter()
    title_terms: Counter[str] = Counter()
    source_terms: Counter[str] = Counter()
    title_lengths: list[int] = []
    description_lengths: list[int] = []
    characteristic_counts: list[int] = []

    for card in cards:
        title = str(card.get("title") or "")
        description = str(card.get("description") or "")
        characteristics = card.get("characteristics")
        title_lengths.append(len(title))
        description_lengths.append(len(description))
        title_terms.update(_words(title))
        source_terms.update(_source_keywords(str(card.get("source_category") or "")))
        if isinstance(characteristics, dict):
            clean_fields = [str(key).strip() for key in characteristics if str(key).strip()]
            field_counts.update(clean_fields)
            characteristic_counts.append(len(clean_fields))
        else:
            characteristic_counts.append(0)

    title_avg, title_min, title_max = _number_stats(title_lengths)
    desc_avg, desc_min, desc_max = _number_stats(description_lengths)
    chars_avg, _, _ = _number_stats(characteristic_counts)
    required = [
        field
        for field, count in field_counts.most_common()
        if count / len(cards) >= 0.6
    ][:12]
    recommended = [field for field, _ in field_counts.most_common(20)]
    target_min, target_max = _characteristic_targets(parent, chars_avg)
    desc_target = DESCRIPTION_TARGETS.get(parent, (800, 1200))

    return {
        "marketplace": "wb",
        "category": category,
        "parent_category": parent,
        "cards_count": len(cards),
        "title_formula": TITLE_FORMULAS.get(parent, "тип товара + ключевой параметр + размер/количество"),
        "title_target_min": max(20, min(40, round(title_avg - 8))),
        "title_target_max": min(60, max(45, round(title_avg + 12))),
        "description_target_min": desc_target[0],
        "description_target_max": desc_target[1],
        "characteristics_target_min": target_min,
        "characteristics_target_max": target_max,
        "required_characteristics": required,
        "recommended_characteristics": recommended,
        "top_title_words": [word for word, _ in title_terms.most_common(15)],
        "match_keywords": [
            word
            for word, _ in (source_terms + title_terms).most_common(30)
            if word not in {"для", "and", "the"}
        ],
        "hashtags_target": 0,
        "stats": {
            "title_avg": title_avg,
            "title_min": title_min,
            "title_max": title_max,
            "description_avg": desc_avg,
            "description_min": desc_min,
            "description_max": desc_max,
            "characteristics_avg": chars_avg,
        },
    }


def build_wb_category_profiles(cards: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in cards:
        if isinstance(card, dict):
            grouped[_top_category(card)].append(card)
            detailed = _profile_category(card)
            if detailed and detailed != _top_category(card):
                grouped[detailed].append(card)

    return {
        category: _build_profile(category, category_cards)
        for category, category_cards in sorted(grouped.items())
        if len(category_cards) >= 2
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build WB category profiles from reference cards.")
    parser.add_argument("--dataset", default=DEFAULT_DATASET_PATH)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()

    cards = json.loads(Path(args.dataset).read_text(encoding="utf-8"))
    if not isinstance(cards, list):
        raise SystemExit("Dataset must be a JSON array")

    profiles = build_wb_category_profiles(cards)
    Path(args.output).write_text(
        json.dumps(profiles, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(profiles)} WB profiles to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
