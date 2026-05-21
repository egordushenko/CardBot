import argparse
import json
import re
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any


STOP_SECTION_MARKERS = {
    "Фото",
    "Отзывы",
    "Описание",
    "Вопросы",
    "Похожие товары",
    "С этим товаром покупают",
    "Фото и видео покупателей",
}

STOP_SECTION_PREFIXES = (
    "Информация о технических характеристиках",
    "Подборки товаров",
    "Зарегистрирован в системе",
    "Отзывы о товаре",
    "Вопросы о товаре",
    "Все отзывы",
    "Этот вариант товара",
    "Рекомендуем",
    "Похожие",
    "Смотрите также",
)


def is_stop_section_line(line: str) -> bool:
    return line in STOP_SECTION_MARKERS or any(
        line.startswith(prefix) for prefix in STOP_SECTION_PREFIXES
    )


BROWSER_EXTRACTOR_JS = r"""
(() => {
  const clean = (value) => String(value || '').replace(/\s+/g, ' ').trim();
  const lines = document.body.innerText
    .split('\n')
    .map((line) => clean(line))
    .filter(Boolean);

  const stop = new Set(['Фото', 'Отзывы', 'Описание', 'Вопросы', 'Похожие товары', 'С этим товаром покупают', 'Фото и видео покупателей']);
  const stopPrefixes = ['Информация о технических характеристиках', 'Подборки товаров', 'Зарегистрирован в системе', 'Отзывы о товаре', 'Вопросы о товаре', 'Все отзывы', 'Этот вариант товара', 'Рекомендуем', 'Похожие', 'Смотрите также'];
  const isStopLine = (line) => stop.has(line) || stopPrefixes.some((prefix) => line.startsWith(prefix));
  const characteristics = {};
  let start = lines.findIndex((line) => line === 'Характеристики');
  if (start < 0) start = lines.findIndex((line) => line === 'О товаре');
  if (start >= 0) {
    let firstPairIndex = start + 1;
    if (lines[firstPairIndex] === 'Перейти к описанию') firstPairIndex += 1;
    for (let i = firstPairIndex; i < lines.length - 1; i += 2) {
      if (isStopLine(lines[i])) break;
      if (lines[i].includes(':')) {
        const [rawKey, ...rawValue] = lines[i].split(':');
        const key = rawKey.trim();
        const value = rawValue.join(':').trim();
        if (key && value && key.length <= 90 && value.length <= 240) characteristics[key] = value;
        i -= 1;
        continue;
      }
      const key = lines[i].replace(/:$/, '');
      const value = lines[i + 1];
      if (isStopLine(value)) break;
      if (key && value && key.length <= 90 && value.length <= 240) {
        characteristics[key] = value;
      }
    }
  }

  const productLd = [...document.querySelectorAll('script[type="application/ld+json"]')]
    .map((node) => {
      try { return JSON.parse(node.textContent); } catch (_) { return null; }
    })
    .flatMap((item) => Array.isArray(item) ? item : [item])
    .find((item) => item && (item['@type'] === 'Product' || (Array.isArray(item['@type']) && item['@type'].includes('Product'))));

  const rating = productLd?.aggregateRating?.ratingValue ? Number(String(productLd.aggregateRating.ratingValue).replace(',', '.')) : null;
  const reviewCount = productLd?.aggregateRating?.reviewCount ? Number(String(productLd.aggregateRating.reviewCount).replace(/\D/g, '')) : null;
  const title = clean(productLd?.name || document.querySelector('h1')?.innerText || document.title);
  const description = clean(productLd?.description || '');
  const hashtags = title
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s-]/gu, ' ')
    .split(/\s+/)
    .filter((word) => word.length > 3)
    .slice(0, 12)
    .map((word) => `#${word.replace(/-/g, '_')}`);

  const payload = {
    source_url: location.href,
    product_id: (location.pathname.match(/-(\d+)\/?$/) || [])[1] || null,
    category: [...document.querySelectorAll('nav a, [data-widget*="bread"] a')]
      .map((node) => clean(node.innerText))
      .filter(Boolean)
      .join(' / '),
    title,
    description,
    rating,
    review_count: reviewCount,
    characteristics,
    hashtags,
    scraped_at: new Date().toISOString()
  };

  console.log(JSON.stringify(payload, null, 2));
  navigator.clipboard?.writeText(JSON.stringify(payload, null, 2));
  return payload;
})();
""".strip()


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value or "")).strip()


def parse_review_count(text: str) -> int | None:
    value = normalize_text(text).lower()
    match = re.search(r"(\d[\d\s]*(?:[,.]\d+)?)\s*(тыс\.?|k)?\s*отзыв", value)
    if not match:
        return None

    number = float(match.group(1).replace(" ", "").replace(",", "."))
    if match.group(2):
        number *= 1000
    return int(number)


def parse_rating(text: str) -> float | None:
    value = normalize_text(text)
    match = re.search(r"([1-5](?:[,.]\d)?)", value)
    if not match:
        return None
    return float(match.group(1).replace(",", "."))


def parse_characteristics_from_text(text: str) -> dict[str, str]:
    lines = [normalize_text(line) for line in text.splitlines()]
    lines = [line for line in lines if line]
    if "Характеристики" in lines:
        start = lines.index("Характеристики") + 1
    elif "О товаре" in lines:
        start = lines.index("О товаре") + 1
        if start < len(lines) and lines[start] == "Перейти к описанию":
            start += 1
    else:
        return {}

    result: dict[str, str] = {}
    index = start
    while index < len(lines) - 1:
        key = lines[index].rstrip(":")
        if is_stop_section_line(lines[index]):
            break
        if ":" in lines[index]:
            key, value = [part.strip() for part in lines[index].split(":", 1)]
            if key and value and 1 < len(key) <= 90 and len(value) <= 240:
                result[key] = value
            index += 1
            continue
        key = lines[index].rstrip(":")
        value = lines[index + 1]
        if is_stop_section_line(value):
            break
        if 1 < len(key) <= 90 and 0 < len(value) <= 240:
            result[key] = value
        index += 2
    return result


def _iter_json_ld_objects(html: str) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    pattern = re.compile(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(html):
        raw = unescape(match.group(1)).strip()
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, list):
            objects.extend(item for item in parsed if isinstance(item, dict))
        elif isinstance(parsed, dict):
            graph = parsed.get("@graph")
            if isinstance(graph, list):
                objects.extend(item for item in graph if isinstance(item, dict))
            objects.append(parsed)
    return objects


def _is_product_type(value: Any) -> bool:
    if isinstance(value, str):
        return value.lower() == "product"
    if isinstance(value, list):
        return any(_is_product_type(item) for item in value)
    return False


def parse_json_ld_products(html: str) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    for item in _iter_json_ld_objects(html):
        if not _is_product_type(item.get("@type")):
            continue
        rating_data = item.get("aggregateRating") or {}
        products.append(
            {
                "title": normalize_text(str(item.get("name", ""))),
                "description": normalize_text(str(item.get("description", ""))),
                "rating": parse_rating(str(rating_data.get("ratingValue", ""))),
                "review_count": parse_review_count(
                    f"{rating_data.get('reviewCount', '')} отзывов"
                ),
            }
        )
    return products


def parse_category_from_text(text: str) -> str:
    lines = [normalize_text(line) for line in text.splitlines()]
    crumbs = [line for line in lines if line and line not in STOP_SECTION_MARKERS]
    return " / ".join(crumbs[:4]) if len(crumbs) >= 2 else ""


def extract_hashtags(title: str, description: str = "") -> list[str]:
    words = re.findall(r"[A-Za-zА-Яа-яЁё0-9-]{4,}", f"{title} {description}".lower())
    seen: set[str] = set()
    result: list[str] = []
    for word in words:
        tag = "#" + word.replace("-", "_")
        if tag not in seen:
            seen.add(tag)
            result.append(tag)
        if len(result) >= 12:
            break
    return result


def build_card_record(content: str, source_url: str = "") -> dict[str, Any]:
    json_products = parse_json_ld_products(content)
    product = json_products[0] if json_products else {}
    plain_text = re.sub(r"<[^>]+>", "\n", content)
    title = product.get("title") or normalize_text(plain_text.splitlines()[0] if plain_text else "")
    description = product.get("description") or ""

    return {
        "source_url": source_url,
        "category": parse_category_from_text(plain_text),
        "title": title,
        "description": description,
        "rating": product.get("rating"),
        "review_count": product.get("review_count"),
        "characteristics": parse_characteristics_from_text(plain_text),
        "hashtags": extract_hashtags(title, description),
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }


def is_reference_card(
    record: dict[str, Any],
    min_rating: float = 4.7,
    min_reviews: int = 1000,
) -> bool:
    rating = record.get("rating")
    review_count = record.get("review_count")
    return (
        isinstance(rating, int | float)
        and isinstance(review_count, int)
        and rating >= min_rating
        and review_count >= min_reviews
    )


def load_input_record(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        record = json.loads(content)
        if "scraped_at" not in record:
            record["scraped_at"] = datetime.now(timezone.utc).isoformat()
        return record
    return build_card_record(content, source_url="")


def collect_dataset(
    input_dir: Path,
    min_rating: float = 4.7,
    min_reviews: int = 1000,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(input_dir.glob("*")):
        if path.suffix.lower() not in {".html", ".htm", ".txt", ".json"}:
            continue
        record = load_input_record(path)
        if is_reference_card(record, min_rating=min_rating, min_reviews=min_reviews):
            records.append(record)
    return records


def write_dataset(records: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect Ozon product-card reference records into JSON."
    )
    parser.add_argument("--input-dir", type=Path, help="Directory with .html/.txt/.json exports.")
    parser.add_argument("--output", type=Path, default=Path("data/ozon_cards_dataset.json"))
    parser.add_argument("--min-rating", type=float, default=4.7)
    parser.add_argument("--min-reviews", type=int, default=1000)
    parser.add_argument(
        "--browser-snippet",
        action="store_true",
        help="Print JavaScript extractor for an opened Ozon product page.",
    )
    args = parser.parse_args()

    if args.browser_snippet:
        print(BROWSER_EXTRACTOR_JS)
        return 0
    if not args.input_dir:
        parser.error("--input-dir is required unless --browser-snippet is used")

    records = collect_dataset(args.input_dir, args.min_rating, args.min_reviews)
    write_dataset(records, args.output)
    print(f"Wrote {len(records)} records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
