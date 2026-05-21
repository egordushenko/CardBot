from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_INPUT_PATH = "data/wb_nmids.md"
DEFAULT_OUTPUT_PATH = "data/wb_cards_dataset.json"
DEFAULT_RAW_DIR = "data/wb_raw"
DEFAULT_MIN_REVIEWS = 1000


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
    "Referer": "https://www.wildberries.ru/",
}

BASKET_VOL_RANGES = [
    (143, 1),
    (287, 2),
    (431, 3),
    (719, 4),
    (1007, 5),
    (1061, 6),
    (1115, 7),
    (1169, 8),
    (1313, 9),
    (1601, 10),
    (1655, 11),
    (1919, 12),
    (2045, 13),
    (2189, 14),
    (2405, 15),
    (2621, 16),
    (2837, 17),
    (3053, 18),
    (3269, 19),
    (3485, 20),
    (3701, 21),
    (3917, 22),
    (4133, 23),
    (4349, 24),
    (4565, 25),
    (4781, 26),
    (4997, 27),
    (5213, 28),
    (5429, 29),
    (5645, 30),
    (5969, 31),
    (6293, 32),
    (6617, 33),
    (6941, 34),
    (7265, 35),
    (7589, 36),
    (7913, 37),
    (8237, 38),
    (8561, 39),
    (8885, 40),
    (10209, 41),
]


CATEGORY_MAP = {
    "Женщинам/Одежда": "Женщинам / Одежда",
    "Женщинам/Платья": "Женщинам / Одежда / Платья",
    "Мужчинам/Одежда": "Мужчинам / Одежда",
    "Обувь": "Обувь",
    "Детям/Одежда": "Детям / Одежда",
    "Красота": "Красота",
    "dom-i-dacha/vannaya/kovriki": "Дом / Ванная / Коврики",
    "dom/vannaya/mebel-zerkala-shtory": "Дом / Ванная / Мебель, зеркала, шторы",
    "catalog/krasota/volosy/dlya-rosta": "Красота / Волосы / Для роста",
    "krasota/aksessuary/dlya-britya-i-udaleniya-volos": "Красота / Аксессуары / Для бритья и удаления волос",
    "aksessuary/maski-dlya-sna": "Аксессуары / Маски для сна",
    "elektronika/smartfony-i-telefony/vse-smartfony": "Электроника / Смартфоны и телефоны / Смартфоны",
    "elektronika/noutbuki-i-kompyutery/komplektuyushchie-dlya-pk/videokarty": "Электроника / Комплектующие для ПК / Видеокарты",
    "igrushki/antistress": "Игрушки / Антистресс",
    "igrushki/dlya-malyshey/kachalki": "Игрушки / Для малышей / Качалки",
    "zhenshchinam/bele-i-kupalniki/erotik": "Женщинам / Белье и купальники / Эротик",
    "pitanie/chay-kofe/chay": "Продукты питания / Чай, кофе / Чай",
    "elektronika/tehnika-dlya-kuhni/prigotovlenie-blyud": "Бытовая техника / Техника для кухни / Приготовление блюд",
    "dlya-remonta/santehnika/vanny": "Строительство и ремонт / Сантехника / Ванны",
    "dom/sad-i-dacha/sadovaya-tehnika/opryskivateli": "Дом / Сад и дача / Опрыскиватели",
    "dom-i-dacha/zdorove/kapli-sprei-i-rastvory": "Здоровье / Капли, спреи и растворы",
    "dom-i-dacha/zdorove/vitaminy-i-bady/vitamin-d": "Здоровье / Витамины и БАДы / Витамин D",
}


def _clean_source_category(value: str) -> str:
    value = value.strip().strip("*").strip(":").strip()
    value = re.sub(r"\s*\(\d+\)\s*$", "", value)
    value = value.removeprefix("https://www.wildberries.ru/catalog/")
    value = value.removeprefix("https://wildberries.ru/catalog/")
    value = value.removeprefix("www.wildberries.ru/catalog/")
    value = value.removeprefix("wildberries.ru/catalog/")
    value = value.split("?", 1)[0].strip("/")
    return value


def normalize_category(source_category: str, fallback: str = "") -> str:
    key = _clean_source_category(source_category)
    if key in CATEGORY_MAP:
        return CATEGORY_MAP[key]
    if re.search(r"[А-Яа-яЁё]", key):
        return " / ".join(part.strip() for part in key.split("/") if part.strip())
    if fallback:
        return fallback
    return " / ".join(part.replace("-", " ").strip().title() for part in key.split("/") if part)


def extract_nmids_from_text(text: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    current_category = "Без категории"
    seen: set[int] = set()

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("**") and stripped.endswith(":**"):
            current_category = _clean_source_category(stripped.strip("*"))
            continue
        if stripped.endswith(":") and not re.fullmatch(r"[\d,\s'\\n]+:", stripped):
            current_category = _clean_source_category(stripped[:-1])
            continue

        for raw_id in re.findall(r"(?<!\d)\d{7,10}(?!\d)", stripped):
            nmid = int(raw_id)
            if nmid in seen:
                continue
            seen.add(nmid)
            rows.append({"nmid": nmid, "source_category": current_category})
    return rows


def _basket_number(vol: int) -> int | None:
    for max_vol, basket in BASKET_VOL_RANGES:
        if vol <= max_vol:
            return basket
    return None


def _basket_hosts(nmid: int) -> list[str]:
    vol = nmid // 100000
    part = nmid // 1000
    preferred = _basket_number(vol)
    order: list[int] = []
    if preferred:
        order.extend([preferred, preferred - 1, preferred + 1])
        order.extend(range(max(1, preferred - 5), preferred + 6))
    if vol > BASKET_VOL_RANGES[-1][0]:
        order.extend(range(41, 81))
        order.extend(range(31, 41))
    order.extend(range(1, 81))
    seen: set[int] = set()
    result: list[str] = []
    for index in order:
        if index < 1 or index in seen:
            continue
        seen.add(index)
        result.append(
            f"https://basket-{index:02d}.wbbasket.ru/vol{vol}/part{part}/{nmid}/info/ru/card.json"
        )
    return result


def _load_json_url(url: str, timeout: float = 3) -> Any:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_card_info(nmid: int) -> dict[str, Any] | None:
    for url in _basket_hosts(nmid):
        try:
            return _load_json_url(url, timeout=2)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            continue
    return None


def fetch_detail_product(nmid: int) -> dict[str, Any] | None:
    url = (
        "https://card.wb.ru/cards/v4/detail?"
        f"appType=1&curr=rub&dest=-1257786&spp=30&nm={nmid}"
    )
    try:
        payload = _load_json_url(url)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None

    products = payload.get("products")
    if not isinstance(products, list) or not products:
        return None
    return products[0]


def parse_card_info(payload: dict[str, Any]) -> dict[str, Any]:
    characteristics: dict[str, str] = {}
    for item in payload.get("options") or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        value = item.get("value")
        if isinstance(value, list):
            value_text = ", ".join(str(part).strip() for part in value if str(part).strip())
        else:
            value_text = str(value or "").strip()
        if name and value_text:
            characteristics[name] = value_text

    root = str(payload.get("subj_root_name") or "").strip()
    subject = str(payload.get("subj_name") or "").strip()
    category = " / ".join(part for part in [root, subject] if part)

    return {
        "title": str(payload.get("imt_name") or "").strip(),
        "category": category,
        "description": str(payload.get("description") or "").strip(),
        "characteristics": characteristics,
    }


def parse_detail_product(product: dict[str, Any]) -> dict[str, Any]:
    return {
        "brand": str(product.get("brand") or "").strip(),
        "title": str(product.get("name") or "").strip(),
        "rating": product.get("reviewRating"),
        "reviews_count": int(product.get("feedbacks") or 0),
    }


def build_card_record(
    nmid: int,
    info: dict[str, Any],
    detail: dict[str, Any],
    source_category: str,
) -> dict[str, Any]:
    category = normalize_category(source_category, str(info.get("category") or ""))
    return {
        "url": f"https://www.wildberries.ru/catalog/{nmid}/detail.aspx",
        "nm_id": nmid,
        "title": detail.get("title") or info.get("title") or "",
        "category": category,
        "source_category": source_category,
        "brand": detail.get("brand") or "",
        "description": info.get("description") or "",
        "characteristics": info.get("characteristics") or {},
        "reviews_count": detail.get("reviews_count") or 0,
        "rating": detail.get("rating"),
        "hashtags": [],
    }


def is_valid_card(card: dict[str, Any], min_reviews: int = DEFAULT_MIN_REVIEWS) -> bool:
    return (
        bool(card.get("title"))
        and bool(card.get("description"))
        and isinstance(card.get("characteristics"), dict)
        and bool(card["characteristics"])
        and int(card.get("reviews_count") or 0) >= min_reviews
    )


def collect_cards(
    rows: list[dict[str, Any]],
    output_path: Path,
    raw_dir: Path,
    min_reviews: int = DEFAULT_MIN_REVIEWS,
    save_every: int = 10,
    sleep_seconds: float = 0.05,
) -> list[dict[str, Any]]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    existing_cards: list[dict[str, Any]] = []
    if output_path.exists():
        loaded = json.loads(output_path.read_text(encoding="utf-8"))
        if isinstance(loaded, list):
            existing_cards = loaded

    cards_by_id = {
        int(card["nm_id"]): card
        for card in existing_cards
        if isinstance(card, dict) and str(card.get("nm_id") or "").isdigit()
    }

    for raw_path in sorted(raw_dir.glob("*.json")):
        try:
            raw_card = json.loads(raw_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        raw_nmid = raw_card.get("nm_id")
        if str(raw_nmid or "").isdigit() and is_valid_card(raw_card, min_reviews=min_reviews):
            cards_by_id[int(raw_nmid)] = raw_card

    processed = 0
    for row in rows:
        nmid = int(row["nmid"])
        if nmid in cards_by_id:
            continue

        info_payload = fetch_card_info(nmid)
        detail_payload = fetch_detail_product(nmid)
        if not info_payload or not detail_payload:
            continue

        card = build_card_record(
            nmid=nmid,
            info=parse_card_info(info_payload),
            detail=parse_detail_product(detail_payload),
            source_category=str(row.get("source_category") or ""),
        )
        raw_path = raw_dir / f"{nmid}.json"
        raw_path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        if is_valid_card(card, min_reviews=min_reviews):
            cards_by_id[nmid] = card
            processed += 1
            if processed % save_every == 0:
                output_path.write_text(
                    json.dumps(list(cards_by_id.values()), ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    cards = list(cards_by_id.values())
    output_path.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return cards


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect Wildberries cards by nm_id list.")
    parser.add_argument("--input", default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--raw-dir", default=DEFAULT_RAW_DIR)
    parser.add_argument("--min-reviews", type=int, default=DEFAULT_MIN_REVIEWS)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    rows = extract_nmids_from_text(Path(args.input).read_text(encoding="utf-8"))
    if args.limit:
        rows = rows[: args.limit]
    cards = collect_cards(
        rows=rows,
        output_path=Path(args.output),
        raw_dir=Path(args.raw_dir),
        min_reviews=args.min_reviews,
    )
    print(f"Wrote {len(cards)} cards to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
