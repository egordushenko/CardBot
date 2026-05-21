from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


DEFAULT_DATASET_PATH = "data/ozon_cards_dataset.json"
DEFAULT_OUTPUT_MD_PATH = "data/ozon_dataset_analysis.md"
DEFAULT_OUTPUT_JSON_PATH = "data/ozon_dataset_analysis.json"

TITLE_SOFT_MAX = 140
DESCRIPTION_TARGET_MIN = 900
DESCRIPTION_TARGET_MAX = 1400
HASHTAG_TARGET_MIN = 8
HASHTAG_TARGET_MAX = 15
CHARACTERISTICS_TARGET_MIN = 6
CHARACTERISTICS_TARGET_MAX = 12


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _top_category(card: dict[str, Any]) -> str:
    collection_category = str(card.get("collection_target_category") or "").strip()
    if collection_category:
        return collection_category
    raw_category = str(card.get("category") or "").strip()
    return raw_category.split(" / ", 1)[0].strip() or "Без категории"


def _safe_text(value: Any) -> str:
    return str(value or "").strip()


def _lengths(cards: list[dict[str, Any]], field: str) -> list[int]:
    return [len(_safe_text(card.get(field))) for card in cards]


def _percentile(values: list[int], percentile: int) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = round((len(ordered) - 1) * percentile / 100)
    return ordered[index]


def _number_stats(values: list[int]) -> dict[str, float | int]:
    return {
        "min": min(values, default=0),
        "avg": round(mean(values), 1) if values else 0.0,
        "p50": _percentile(values, 50),
        "p75": _percentile(values, 75),
        "p90": _percentile(values, 90),
        "max": max(values, default=0),
    }


def _characteristic_counts(cards: list[dict[str, Any]]) -> Counter[str]:
    fields: Counter[str] = Counter()
    for card in cards:
        characteristics = card.get("characteristics")
        if isinstance(characteristics, dict):
            fields.update(str(key).strip() for key in characteristics if str(key).strip())
    return fields


def _tokenize_title(title: str) -> list[str]:
    return [
        token.lower()
        for token in re.findall(r"[A-Za-zА-Яа-яЁё0-9]{3,}", title)
        if not token.isdigit()
    ]


def _top_title_terms(cards: list[dict[str, Any]], limit: int = 20) -> list[tuple[str, int]]:
    terms: Counter[str] = Counter()
    for card in cards:
        terms.update(_tokenize_title(_safe_text(card.get("title"))))
    return terms.most_common(limit)


def _hashtag_counts(cards: list[dict[str, Any]]) -> list[int]:
    counts: list[int] = []
    for card in cards:
        hashtags = card.get("hashtags")
        counts.append(len(hashtags) if isinstance(hashtags, list) else 0)
    return counts


def _characteristic_item_counts(cards: list[dict[str, Any]]) -> list[int]:
    counts: list[int] = []
    for card in cards:
        characteristics = card.get("characteristics")
        counts.append(len(characteristics) if isinstance(characteristics, dict) else 0)
    return counts


def _profile_cards(cards: list[dict[str, Any]]) -> dict[str, Any]:
    title_lengths = _lengths(cards, "title")
    description_lengths = _lengths(cards, "description")
    return {
        "title_length": _number_stats(title_lengths),
        "description_length": _number_stats(description_lengths),
        "characteristics_count": _number_stats(_characteristic_item_counts(cards)),
        "hashtags_count": _number_stats(_hashtag_counts(cards)),
        "top_characteristics": _characteristic_counts(cards).most_common(20),
        "top_title_terms": _top_title_terms(cards),
    }


def analyze_dataset(cards: list[dict[str, Any]]) -> dict[str, Any]:
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in cards:
        by_category[_top_category(card)].append(card)

    categories: dict[str, Any] = {}
    for category, category_cards in sorted(by_category.items()):
        profile = _profile_cards(category_cards)
        profile["count"] = len(category_cards)
        categories[category] = profile

    return {
        "total_cards": len(cards),
        "global": _profile_cards(cards),
        "categories": categories,
        "prompt_rules": {
            "title": {
                "hard_max": 200,
                "soft_max": TITLE_SOFT_MAX,
                "structure": "тип товара + бренд/модель при наличии + 2-4 важные характеристики",
                "avoid": [
                    "акции и скидки",
                    "контакты и ссылки",
                    "переспам синонимами",
                    "слова длиннее 27 символов",
                ],
            },
            "description": {
                "target_min": DESCRIPTION_TARGET_MIN,
                "target_max": DESCRIPTION_TARGET_MAX,
                "structure": "1 короткий абзац пользы + 3-5 преимуществ + сценарии применения",
            },
            "hashtags": {
                "target_min": HASHTAG_TARGET_MIN,
                "target_max": HASHTAG_TARGET_MAX,
                "max": 30,
                "format": "#слово #фраза_через_подчеркивание без запятых",
            },
            "characteristics": {
                "target_min": CHARACTERISTICS_TARGET_MIN,
                "target_max": CHARACTERISTICS_TARGET_MAX,
                "format": "Ключ: Значение, одна характеристика на строку",
            },
        },
    }


def _stats_line(stats: dict[str, Any]) -> str:
    return (
        f"{stats['min']} / {stats['avg']} / {stats['p50']} / "
        f"{stats['p75']} / {stats['p90']} / {stats['max']}"
    )


def build_markdown_report(report: dict[str, Any]) -> str:
    global_profile = report["global"]
    rules = report["prompt_rules"]
    lines = [
        "# Ozon dataset analysis",
        "",
        f"- Cards: {report['total_cards']}",
        f"- Categories: {len(report['categories'])}",
        "",
        "## Global profile",
        "",
        "| Metric | min / avg / p50 / p75 / p90 / max |",
        "|---|---:|",
        f"| Title length | {_stats_line(global_profile['title_length'])} |",
        f"| Description length | {_stats_line(global_profile['description_length'])} |",
        f"| Characteristics count | {_stats_line(global_profile['characteristics_count'])} |",
        f"| Hashtags count | {_stats_line(global_profile['hashtags_count'])} |",
        "",
        "## Prompt rules",
        "",
        f"- Title: до {rules['title']['hard_max']} символов по правилам Ozon, целевой потолок CardBot — {rules['title']['soft_max']} символов.",
        f"- Title structure: {rules['title']['structure']}.",
        f"- Description: {rules['description']['target_min']}-{rules['description']['target_max']} символов.",
        f"- Description structure: {rules['description']['structure']}.",
        f"- Hashtags: {rules['hashtags']['target_min']}-{rules['hashtags']['target_max']} штук, максимум {rules['hashtags']['max']}.",
        f"- Characteristics: {rules['characteristics']['target_min']}-{rules['characteristics']['target_max']} строк в формате `{rules['characteristics']['format']}`.",
        "",
        "## Category profiles",
        "",
        "| Category | Cards | Title avg | Desc avg | Chars avg | Hashtags avg | Top characteristics |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]

    for category, profile in report["categories"].items():
        top_fields = ", ".join(field for field, _ in profile["top_characteristics"][:5])
        lines.append(
            "| "
            f"{category} | "
            f"{profile['count']} | "
            f"{profile['title_length']['avg']} | "
            f"{profile['description_length']['avg']} | "
            f"{profile['characteristics_count']['avg']} | "
            f"{profile['hashtags_count']['avg']} | "
            f"{top_fields} |"
        )

    lines.extend(["", "## Global top characteristics", ""])
    for field, count in global_profile["top_characteristics"][:30]:
        lines.append(f"- {field}: {count}")

    lines.extend(["", "## Global top title terms", ""])
    for term, count in global_profile["top_title_terms"][:30]:
        lines.append(f"- {term}: {count}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Ozon reference cards for CardBot prompts.")
    parser.add_argument("--dataset", default=DEFAULT_DATASET_PATH)
    parser.add_argument("--output-md", default=DEFAULT_OUTPUT_MD_PATH)
    parser.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON_PATH)
    args = parser.parse_args()

    cards = _load_json(Path(args.dataset))
    if not isinstance(cards, list):
        raise SystemExit("Dataset must be a JSON array")

    report = analyze_dataset(cards)
    Path(args.output_json).write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    Path(args.output_md).write_text(build_markdown_report(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
