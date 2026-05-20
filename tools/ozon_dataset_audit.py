from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


RECOMMENDED_CATEGORY_TARGETS: dict[str, int] = {
    "Дом и сад": 18,
    "Электроника": 20,
    "Автотовары": 12,
    "Детские товары": 12,
    "Одежда": 18,
    "Строительство и ремонт": 10,
    "Товары для животных": 10,
    "Бытовая техника": 10,
    "Мебель": 9,
    "Аптека": 8,
    "Спортивные товары": 14,
    "Бытовая химия": 6,
    "Канцелярские товары": 5,
    "Хобби и творчество": 5,
    "Туризм, рыбалка, охота": 5,
    "Красота и здоровье": 20,
    "Продукты питания": 8,
    "Ювелирные украшения": 4,
    "Книги": 3,
    "Все для игр": 3,
}

MIN_RATING = 4.7
MIN_REVIEWS = 1000


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _top_category(raw_category: str) -> str:
    top = (raw_category or "Без категории").split(" / ", 1)[0].strip() or "Без категории"
    if top == "Обувь":
        return "Одежда"
    if top == "Спорт и отдых":
        return "Спортивные товары"
    if top == "Бытовая химия и гигиена":
        return "Бытовая химия"
    return top


def _safe_len(value: Any) -> int:
    return len(str(value or ""))


def _avg(values: list[int]) -> float:
    return round(mean(values), 1) if values else 0.0


def _card_issues(card: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not str(card.get("title") or "").strip():
        issues.append("missing_title")
    if not str(card.get("description") or "").strip():
        issues.append("missing_description")
    if not isinstance(card.get("characteristics"), dict) or not card.get("characteristics"):
        issues.append("missing_characteristics")
    if not _as_list(card.get("hashtags")):
        issues.append("missing_hashtags")

    rating = card.get("rating")
    if not isinstance(rating, (int, float)) or rating < MIN_RATING:
        issues.append("low_rating")

    review_count = card.get("review_count")
    if not isinstance(review_count, int) or review_count < MIN_REVIEWS:
        issues.append("low_review_count")

    return issues


def audit_dataset(
    cards: list[dict[str, Any]],
    category_targets: dict[str, int] | None = None,
) -> dict[str, Any]:
    targets = category_targets or RECOMMENDED_CATEGORY_TARGETS
    product_ids = [str(card.get("product_id") or "").strip() for card in cards]
    source_urls = [str(card.get("source_url") or "").strip() for card in cards]
    category_counts = Counter(_top_category(str(card.get("category") or "")) for card in cards)

    issues: dict[int, list[str]] = {}
    for index, card in enumerate(cards):
        card_issues = _card_issues(card)
        if card_issues:
            issues[index] = card_issues

    title_lengths = [_safe_len(card.get("title")) for card in cards]
    description_lengths = [_safe_len(card.get("description")) for card in cards]
    characteristic_counts = [
        len(card.get("characteristics") or {})
        if isinstance(card.get("characteristics"), dict)
        else 0
        for card in cards
    ]
    hashtag_counts = [len(_as_list(card.get("hashtags"))) for card in cards]

    characteristic_fields: Counter[str] = Counter()
    for card in cards:
        characteristics = card.get("characteristics") or {}
        if isinstance(characteristics, dict):
            characteristic_fields.update(str(key) for key in characteristics)

    category_targets_report = {}
    for name, target in targets.items():
        current = category_counts.get(name, 0)
        category_targets_report[name] = {
            "current": current,
            "target": target,
            "missing": max(target - current, 0),
        }

    return {
        "total_cards": len(cards),
        "target_total": sum(targets.values()),
        "duplicate_product_ids": sorted(
            value for value, count in Counter(product_ids).items() if value and count > 1
        ),
        "duplicate_source_urls": sorted(
            value for value, count in Counter(source_urls).items() if value and count > 1
        ),
        "category_counts": dict(sorted(category_counts.items())),
        "category_targets": category_targets_report,
        "quality": {
            "invalid_cards": len(issues),
            "issues": issues,
            "min_rating": MIN_RATING,
            "min_reviews": MIN_REVIEWS,
        },
        "lengths": {
            "title_min": min(title_lengths, default=0),
            "title_avg": _avg(title_lengths),
            "title_max": max(title_lengths, default=0),
            "description_min": min(description_lengths, default=0),
            "description_avg": _avg(description_lengths),
            "description_max": max(description_lengths, default=0),
        },
        "field_counts": {
            "characteristics_min": min(characteristic_counts, default=0),
            "characteristics_avg": _avg(characteristic_counts),
            "characteristics_max": max(characteristic_counts, default=0),
            "hashtags_min": min(hashtag_counts, default=0),
            "hashtags_avg": _avg(hashtag_counts),
            "hashtags_max": max(hashtag_counts, default=0),
        },
        "top_characteristic_fields": characteristic_fields.most_common(30),
    }


def build_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Ozon dataset audit",
        "",
        f"- Cards: {report['total_cards']} / {report['target_total']}",
        f"- Duplicate product IDs: {len(report['duplicate_product_ids'])}",
        f"- Duplicate URLs: {len(report['duplicate_source_urls'])}",
        "",
        "## Quality",
        "",
        f"- Invalid cards: {report['quality']['invalid_cards']}",
        f"- Min rating required: {report['quality']['min_rating']}",
        f"- Min reviews required: {report['quality']['min_reviews']}",
        "",
        "## Lengths",
        "",
        f"- Title min/avg/max: {report['lengths']['title_min']} / {report['lengths']['title_avg']} / {report['lengths']['title_max']}",
        f"- Description min/avg/max: {report['lengths']['description_min']} / {report['lengths']['description_avg']} / {report['lengths']['description_max']}",
        "",
        "## Field Counts",
        "",
        f"- Characteristics min/avg/max: {report['field_counts']['characteristics_min']} / {report['field_counts']['characteristics_avg']} / {report['field_counts']['characteristics_max']}",
        f"- Hashtags min/avg/max: {report['field_counts']['hashtags_min']} / {report['field_counts']['hashtags_avg']} / {report['field_counts']['hashtags_max']}",
        "",
        "## Category coverage",
        "",
        "| Category | Current | Target | Missing |",
        "|---|---:|---:|---:|",
    ]

    for name, data in report["category_targets"].items():
        lines.append(f"| {name} | {data['current']} | {data['target']} | {data['missing']} |")

    lines.extend(
        [
            "",
            "## Top characteristic fields",
            "",
        ]
    )
    for key, count in report["top_characteristic_fields"][:20]:
        lines.append(f"- {key}: {count}")

    missing = [
        (name, data["missing"])
        for name, data in report["category_targets"].items()
        if data["missing"] > 0
    ]
    missing.sort(key=lambda item: item[1], reverse=True)
    lines.extend(["", "## Recommendations", ""])
    if missing:
        lines.append("Priority categories to collect next:")
        for name, count in missing[:10]:
            lines.append(f"- {name}: {count}")
    else:
        lines.append("Target category coverage is complete.")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Ozon reference cards dataset.")
    parser.add_argument("--dataset", default="data/ozon_cards_dataset.json")
    parser.add_argument("--output-md", default="")
    parser.add_argument("--output-json", default="")
    args = parser.parse_args()

    cards = _load_json(Path(args.dataset))
    if not isinstance(cards, list):
        raise SystemExit("Dataset must be a JSON array")

    report = audit_dataset(cards)
    if args.output_json:
        Path(args.output_json).write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    markdown = build_markdown_report(report)
    if args.output_md:
        Path(args.output_md).write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
