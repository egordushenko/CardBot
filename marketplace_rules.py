from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class MarketplaceRules:
    title_max_chars: int
    title_word_max_chars: int | None = None
    hashtag_max_count: int | None = None
    hashtag_max_chars: int | None = None


MARKETPLACE_RULES = {
    "wb": MarketplaceRules(title_max_chars=60),
    "ozon": MarketplaceRules(
        title_max_chars=200,
        title_word_max_chars=27,
        hashtag_max_count=30,
        hashtag_max_chars=30,
    ),
}


_OZON_FORBIDDEN_TITLE_CHARS_RE = re.compile(r"[™©®\[\]=\\«»]")
_URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
_SOCIAL_HANDLE_RE = re.compile(r"(?<!\w)@\w+")
_PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")
_SPACES_RE = re.compile(r"\s+")
_HASHTAG_CLEAN_RE = re.compile(r"[^\wа-яА-ЯёЁ#]+", re.IGNORECASE)

_FORBIDDEN_PHRASES = (
    "акция",
    "распродажа",
    "скидка",
    "только сегодня",
    "лучший товар",
    "уникальный товар",
    "потрясающий товар",
    "аналог",
    "подделка",
    "копия",
    "copy",
    "реплика",
    "1:1",
    "по мотивам",
    "оригинал",
    "original",
    "подлинный",
)

_RULES_DOC_PATH = Path(__file__).resolve().parent / "docs" / "marketplace_rules.md"
_BACKTICK_VALUE_RE = re.compile(r"`([^`]+)`")


@lru_cache(maxsize=1)
def _load_forbidden_phrases() -> tuple[str, ...]:
    if not _RULES_DOC_PATH.exists():
        return _FORBIDDEN_PHRASES

    try:
        text = _RULES_DOC_PATH.read_text(encoding="utf-8")
    except OSError:
        return _FORBIDDEN_PHRASES

    for line in text.splitlines():
        lowered = line.lower()
        if "запрещены рекламные" not in lowered and "рискованные формулировки" not in lowered:
            continue
        phrases = tuple(
            phrase.strip()
            for phrase in _BACKTICK_VALUE_RE.findall(line)
            if phrase.strip()
        )
        if phrases:
            return phrases
    return _FORBIDDEN_PHRASES


def _collapse_spaces(value: str) -> str:
    return _SPACES_RE.sub(" ", value).strip(" ,.;:-")


def _remove_forbidden_phrases(value: str) -> str:
    result = value
    for phrase in _load_forbidden_phrases():
        result = re.sub(rf"(?iu)(?<!\w){re.escape(phrase)}(?!\w)", "", result)
    return _collapse_spaces(result)


def _truncate_by_words(value: str, max_chars: int) -> str:
    if len(value) <= max_chars:
        return value
    words: list[str] = []
    current_len = 0
    for word in value.split():
        next_len = len(word) if not words else current_len + 1 + len(word)
        if next_len > max_chars:
            break
        words.append(word)
        current_len = next_len
    if words:
        return " ".join(words).strip(" ,.;:-")
    return value[:max_chars].strip(" ,.;:-")


def sanitize_title(value: str, marketplace: str) -> str:
    rules = MARKETPLACE_RULES[marketplace]
    title = _collapse_spaces(value)
    if marketplace == "ozon":
        title = _OZON_FORBIDDEN_TITLE_CHARS_RE.sub(" ", title)
        title = _remove_forbidden_phrases(title)
        if rules.title_word_max_chars:
            title = " ".join(word[: rules.title_word_max_chars] for word in title.split())
    return _truncate_by_words(_collapse_spaces(title), rules.title_max_chars)


def sanitize_description(value: str, marketplace: str) -> str:
    description = value.strip()
    if marketplace == "ozon":
        description = _URL_RE.sub("", description)
        description = _SOCIAL_HANDLE_RE.sub("", description)
        description = _PHONE_RE.sub("", description)
        description = _remove_forbidden_phrases(description)
    return _collapse_spaces(description)


def sanitize_ozon_hashtags(value: str) -> str:
    rules = MARKETPLACE_RULES["ozon"]
    tags: list[str] = []
    seen: set[str] = set()
    raw_parts = re.split(r"[\s,;]+", value)
    for raw_part in raw_parts:
        part = raw_part.strip()
        if not part:
            continue
        part = _HASHTAG_CLEAN_RE.sub("_", part)
        part = part.strip("_#").lower()
        if not part:
            continue
        tag = f"#{part}"
        if rules.hashtag_max_chars and len(tag) > rules.hashtag_max_chars:
            continue
        if tag in seen:
            continue
        tags.append(tag)
        seen.add(tag)
        if rules.hashtag_max_count and len(tags) >= rules.hashtag_max_count:
            break
    return " ".join(tags)
