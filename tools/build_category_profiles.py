from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_PATH = BASE_DIR / "data" / "ozon_cards_dataset.json"
DEFAULT_OUTPUT_PATH = BASE_DIR / "data" / "category_profiles.json"
HASHTAGS_TARGET = 8

_WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+")
_VALUE_LIKE_FIELD_RE = re.compile(
    r"^\d+(?:[.,]\d+)?(?:\s*(?:шт|г|кг|мл|л|см|мм|м|дней|месяц(?:ев|а)?|год(?:а)?))?$",
    re.IGNORECASE,
)
_STOPWORDS = {
    "для",
    "или",
    "при",
    "под",
    "без",
    "над",
    "его",
    "ее",
    "это",
    "как",
    "что",
    "набор",
    "товар",
    "шт",
    "мл",
    "см",
    "мм",
    "кг",
}

_PROFILE_EXCLUDED_FIELDS = {
    "Артикул",
    "Бренд",
    "Добавить к сравнению",
    "Код ТРУ",
    "Номер СГР",
    "Сертификат",
    "Гарантия",
    "Китай",
    "Россия",
    "70 дней",
}

_PROFILE_EXCLUDED_MARKERS = (
    "упаков",
    "срок годности",
    "сертификат",
    "номер сгр",
    "код тру",
    "артикул",
    "бренд",
    "гарант",
    "вес с упаков",
    "вес товара",
    "длина предмета",
    "ширина предмета",
    "высота предмета",
)

_TITLE_TARGETS = {
    "Электроника": (45, 80),
    "Бытовая техника": (45, 80),
    "Красота и здоровье": (55, 95),
    "Аптека": (55, 95),
    "Одежда": (45, 85),
    "Обувь": (40, 75),
}
_DESCRIPTION_TARGETS = {
    "Электроника": (900, 1400),
    "Бытовая техника": (900, 1400),
    "Красота и здоровье": (1100, 1600),
    "Аптека": (900, 1400),
    "Продукты питания": (700, 1200),
    "Книги": (500, 900),
}


def _category_paths(card: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    raw_category = str(card.get("category") or "").strip()
    collection_category = str(card.get("collection_target_category") or "").strip()

    if raw_category:
        parts = [part.strip() for part in raw_category.split(" / ") if part.strip()]
        if len(parts) >= 3 and _looks_like_vendor_leaf(parts[-1]):
            parts = parts[:-1]
        if parts:
            paths.append(parts[0])
            if len(parts) > 1:
                paths.append(" / ".join(parts))
    if collection_category and collection_category not in paths:
        paths.append(collection_category)
    return paths


def _looks_like_vendor_leaf(value: str) -> bool:
    clean = value.strip()
    if not clean or len(clean) > 40:
        return False
    has_cyrillic = bool(re.search(r"[А-Яа-яЁё]", clean))
    has_latin = bool(re.search(r"[A-Za-z]", clean))
    if has_latin and not has_cyrillic:
        return True
    if " " in clean:
        return False
    return bool(has_cyrillic and clean.upper() == clean and len(clean) >= 4)


def _top_category(category: str) -> str:
    return category.split(" / ", 1)[0].strip()


def _iter_characteristic_keys(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [str(key).strip() for key in value if str(key).strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    result: list[str] = []
    for raw_line in str(value or "").splitlines():
        if ":" not in raw_line:
            continue
        key = raw_line.split(":", 1)[0].strip()
        if key:
            result.append(key)
    return result


def _iter_hashtags(value: Any) -> list[str]:
    raw_tags: list[str] = []
    if isinstance(value, list):
        raw_tags = [str(item) for item in value]
    else:
        raw_tags = re.split(r"[\s,;]+", str(value or ""))

    tags: list[str] = []
    for raw_tag in raw_tags:
        tag = raw_tag.strip().lower()
        if not tag:
            continue
        tag = tag if tag.startswith("#") else f"#{tag}"
        tags.append(tag)
    return tags


def _iter_title_words(title: str) -> list[str]:
    words: list[str] = []
    for match in _WORD_RE.finditer(title.lower()):
        word = match.group(0)
        if len(word) < 3 or word in _STOPWORDS:
            continue
        words.append(word)
    return words


def _is_generation_safe_characteristic(field: str) -> bool:
    clean = field.strip()
    lowered = clean.casefold()
    if not clean or clean in _PROFILE_EXCLUDED_FIELDS:
        return False
    if _VALUE_LIKE_FIELD_RE.fullmatch(clean):
        return False
    return not any(marker in lowered for marker in _PROFILE_EXCLUDED_MARKERS)


def _generation_characteristics(fields: list[str]) -> list[str]:
    result: list[str] = []
    for field in fields:
        if _is_generation_safe_characteristic(field) and field not in result:
            result.append(field)
    return result


def _target_range(values: list[int], *, fallback: tuple[int, int], min_floor: int, max_ceiling: int) -> tuple[int, int]:
    if not values:
        return fallback
    med = int(round(median(values)))
    low = max(min_floor, int(round(med * 0.75)))
    high = min(max_ceiling, int(round(med * 1.35)))
    if low > high:
        return fallback
    return low, high


def _description_targets(category: str, desc_lengths: list[int]) -> tuple[int, int]:
    parent = _top_category(category)
    if desc_lengths:
        return _target_range(desc_lengths, fallback=_DESCRIPTION_TARGETS.get(parent, (900, 1400)), min_floor=500, max_ceiling=1800)
    return _DESCRIPTION_TARGETS.get(parent, (900, 1400))


def _title_targets(category: str, title_lengths: list[int]) -> tuple[int, int]:
    parent = _top_category(category)
    if title_lengths:
        return _target_range(title_lengths, fallback=_TITLE_TARGETS.get(parent, (45, 85)), min_floor=35, max_ceiling=110)
    return _TITLE_TARGETS.get(parent, (45, 85))


def _characteristics_targets(counts: list[int]) -> tuple[int, int]:
    if not counts:
        return 4, 8
    avg = int(round(mean(counts)))
    low = max(3, min(8, int(round(avg * 0.55))))
    high = max(low + 2, min(18, int(round(avg * 1.25))))
    return low, high


def _match_keywords(category: str, title_words: Counter[str], hashtags: Counter[str]) -> list[str]:
    words: list[str] = []
    for part in category.replace("/", " ").split():
        clean = part.strip().casefold()
        if len(clean) >= 3 and clean not in _STOPWORDS and clean not in words:
            words.append(clean)
    for word, _ in title_words.most_common(12):
        if word not in words:
            words.append(word)
    for tag, _ in hashtags.most_common(8):
        clean = tag.lstrip("#").replace("_", " ").strip().casefold()
        for word in clean.split():
            if len(word) >= 3 and word not in _STOPWORDS and word not in words:
                words.append(word)
    return words[:18]


def _build_profile(category: str, category_cards: list[dict[str, Any]]) -> dict[str, Any]:
    characteristic_counts: Counter[str] = Counter()
    hashtag_counts: Counter[str] = Counter()
    title_word_counts: Counter[str] = Counter()
    title_lengths: list[int] = []
    desc_lengths: list[int] = []
    characteristics_per_card: list[int] = []

    for card in category_cards:
        title = str(card.get("title") or "").strip()
        description = str(card.get("description") or "").strip()
        characteristics = _iter_characteristic_keys(card.get("characteristics"))
        if title:
            title_lengths.append(len(title))
            title_word_counts.update(_iter_title_words(title))
        if description:
            desc_lengths.append(len(description))
        if characteristics:
            characteristics_per_card.append(len(characteristics))
        characteristic_counts.update(characteristics)
        hashtag_counts.update(_iter_hashtags(card.get("hashtags")))

    all_characteristics = [key for key, _ in characteristic_counts.most_common(24)]
    safe_characteristics = _generation_characteristics(all_characteristics)
    required_threshold = max(1, int(round(len(category_cards) * 0.6)))
    required = [
        key
        for key, count in characteristic_counts.most_common(16)
        if count >= required_threshold and _is_generation_safe_characteristic(key)
    ][:8]
    recommended = [key for key in safe_characteristics if key not in required][:10]
    prompt_characteristics = (required + recommended)[:14]
    title_min, title_max = _title_targets(category, title_lengths)
    desc_min, desc_max = _description_targets(category, desc_lengths)
    chars_min, chars_max = _characteristics_targets(characteristics_per_card)
    title_avg = int(round(mean(title_lengths))) if title_lengths else title_max
    desc_avg = int(round(mean(desc_lengths))) if desc_lengths else desc_max

    return {
        "marketplace": "ozon",
        "category": category,
        "parent_category": _top_category(category),
        "cards_count": len(category_cards),
        "top_characteristics": [key for key, _ in characteristic_counts.most_common(12)],
        "required_characteristics": required,
        "recommended_characteristics": recommended,
        "prompt_characteristics": prompt_characteristics,
        "characteristics_target_min": chars_min,
        "characteristics_target_max": chars_max,
        "top_hashtags": [tag for tag, _ in hashtag_counts.most_common(12)],
        "top_title_words": [word for word, _ in title_word_counts.most_common(8)],
        "match_keywords": _match_keywords(category, title_word_counts, hashtag_counts),
        "title_target_min": title_min,
        "title_target_max": title_max,
        "description_target_min": desc_min,
        "description_target_max": desc_max,
        "desc_target_chars": 1400,
        "title_target_chars": title_avg,
        "hashtags_target": HASHTAGS_TARGET,
        "stats": {
            "title_avg": title_avg,
            "description_avg": desc_avg,
            "characteristics_avg": round(mean(characteristics_per_card), 1) if characteristics_per_card else 0,
        },
    }


def build_category_profiles(cards: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen_by_category: dict[str, set[int]] = defaultdict(set)

    for index, card in enumerate(cards):
        for category in _category_paths(card):
            if index in seen_by_category[category]:
                continue
            grouped[category].append(card)
            seen_by_category[category].add(index)

    profiles: dict[str, dict[str, Any]] = {}
    for category in sorted(grouped):
        profiles[category] = _build_profile(category, grouped[category])
    return profiles


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Ozon category profiles for CardBot.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()

    cards = json.loads(args.dataset.read_text(encoding="utf-8"))
    if not isinstance(cards, list):
        raise SystemExit("Dataset must be a JSON array")

    profiles = build_category_profiles(cards)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(profiles, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Saved {len(profiles)} category profiles to {args.output}")


if __name__ == "__main__":
    main()
