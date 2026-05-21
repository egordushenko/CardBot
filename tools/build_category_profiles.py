from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_PATH = BASE_DIR / "data" / "ozon_cards_dataset.json"
DEFAULT_OUTPUT_PATH = BASE_DIR / "data" / "category_profiles.json"
DESC_TARGET_CHARS = 1400
HASHTAGS_TARGET = 8

_WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+")
_VALUE_LIKE_FIELD_RE = re.compile(r"^\d+(?:[.,]\d+)?(?:\s*(?:шт|г|кг|мл|л|см|мм|м|дней|месяц(?:ев|а)?|год(?:а)?))?$", re.IGNORECASE)
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
)


def _category_of(card: dict[str, Any]) -> str:
    collection_category = str(card.get("collection_target_category") or "").strip()
    if collection_category:
        return collection_category
    raw_category = str(card.get("category") or "").strip()
    return raw_category.split(" / ", 1)[0].strip()


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


def build_category_profiles(cards: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in cards:
        category = _category_of(card)
        if category:
            grouped[category].append(card)

    profiles: dict[str, dict[str, Any]] = {}
    for category in sorted(grouped):
        category_cards = grouped[category]
        characteristic_counts: Counter[str] = Counter()
        hashtag_counts: Counter[str] = Counter()
        title_word_counts: Counter[str] = Counter()
        title_lengths: list[int] = []

        for card in category_cards:
            title = str(card.get("title") or "").strip()
            if title:
                title_lengths.append(len(title))
                title_word_counts.update(_iter_title_words(title))
            characteristic_counts.update(_iter_characteristic_keys(card.get("characteristics")))
            hashtag_counts.update(_iter_hashtags(card.get("hashtags")))

        top_characteristics = [key for key, _ in characteristic_counts.most_common(16)]
        prompt_characteristics = _generation_characteristics(top_characteristics)[:8]

        profiles[category] = {
            "top_characteristics": [key for key, _ in characteristic_counts.most_common(8)],
            "prompt_characteristics": prompt_characteristics,
            "top_hashtags": [tag for tag, _ in hashtag_counts.most_common(8)],
            "top_title_words": [word for word, _ in title_word_counts.most_common(5)],
            "desc_target_chars": DESC_TARGET_CHARS,
            "title_target_chars": int(round(mean(title_lengths))) if title_lengths else 90,
            "hashtags_target": HASHTAGS_TARGET,
        }

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
