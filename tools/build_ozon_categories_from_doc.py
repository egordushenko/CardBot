from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_INPUT_PATH = "docs/ozon_category_collection.md"
DEFAULT_OUTPUT_PATH = "data/ozon_categories_full.json"
DEFAULT_SEED_PATH = "data/ozon_categories.json"


ROOT_BY_FIRST_CATEGORY_URL = {
    "https://www.ozon.ru/category/zhenskaya-odezhda-7501/": "Одежда",
    "https://www.ozon.ru/category/zhenskaya-obuv-7640/": "Обувь",
    "https://www.ozon.ru/category/posuda-i-kuhonnye-prinadlezhnosti-14501/": "Дом и сад",
    "https://www.ozon.ru/category/tovary-dlya-shkoly-7182/": "Детские товары",
    "https://www.ozon.ru/category/uhod-za-volosami-6584/": "Красота и здоровье",
    "https://www.ozon.ru/category/krupnaya-bytovaya-tehnika-10501/": "Бытовая техника",
    "https://www.ozon.ru/category/sportivnoe-pitanie-11650/": "Спорт и отдых",
    "https://www.ozon.ru/category/instrumenty-dlya-remonta-i-stroitelstva-9856/": "Строительство и ремонт",
    "https://www.ozon.ru/category/chay-kofe-kakao-9370/": "Продукты питания",
    "https://www.ozon.ru/category/lekarstvennye-sredstva-30000/": "Аптека",
    "https://www.ozon.ru/category/dlya-koshek-12347/": "Товары для животных",
    "https://www.ozon.ru/category/nehudozhestvennaya-literatura-16511/": "Книги",
    "https://www.ozon.ru/category/turizm-i-otdyh-na-prirode-11424/": "Туризм, рыбалка, охота",
    "https://www.ozon.ru/category/avtozapchasti-8678/": "Автотовары",
    "https://www.ozon.ru/category/sadovaya-mebel-15155/": "Мебель",
    "https://www.ozon.ru/category/rukodelie-13586/": "Хобби и творчество",
    "https://www.ozon.ru/category/koltsa-yuvelirnye-50002/": "Ювелирные украшения",
    "https://www.ozon.ru/category/zhenskie-aksessuary-17000/": "Аксессуары",
    "https://www.ozon.ru/category/playstation-31719/": "Игры и консоли",
    "https://www.ozon.ru/category/pismennye-prinadlezhnosti-18015/": "Канцелярские товары",
    "https://www.ozon.ru/category/ceks-igrushki-9024/": "Товары для взрослых",
    "https://www.ozon.ru/category/kollektsionirovanie-13755/": "Антиквариат и коллекционирование",
    "https://www.ozon.ru/category/podarochnye-sertifikaty-32060/": "Подарочные сертификаты",
    "https://www.ozon.ru/category/bytovaya-himiya-36861/": "Бытовая химия и гигиена",
    "https://www.ozon.ru/category/muzyka-34944/": "Музыка и видео",
    "https://www.ozon.ru/category/elektronnye-sigarety-i-sistemy-nagrevaniya-31917/": "Товары для курения и аксессуары",
    "https://www.ozon.ru/category/telefony-i-smart-chasy-15501/": "Электроника",
}

ROOT_ALIASES = {
    "Спортивные товары": "Спорт и отдых",
    "Все для игр": "Игры и консоли",
    "Бытовая химия": "Бытовая химия и гигиена",
}


def normalize_url(value: str) -> str:
    url = str(value or "").strip()
    if not url:
        return ""
    url = url.split("?", 1)[0].split("#", 1)[0]
    return url if url.endswith("/") else f"{url}/"


def normalize_root_name(value: str) -> str:
    name = str(value or "").strip()
    return ROOT_ALIASES.get(name, name)


def extract_category_id(url: str) -> int | None:
    match = re.search(r"-(\d+)/?$", url)
    return int(match.group(1)) if match else None


def extract_json_payloads(markdown_text: str) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    pos = 0
    while True:
        marker = markdown_text.find('"page_url"', pos)
        if marker < 0:
            break
        start = markdown_text.rfind("{", 0, marker)
        if start < 0:
            break

        depth = 0
        in_string = False
        escaped = False
        end = None
        for index, char in enumerate(markdown_text[start:], start):
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break

        if end is None:
            break
        raw = markdown_text[start:end]
        payload = json.loads(raw)
        if isinstance(payload, dict) and isinstance(payload.get("categories"), list):
            payloads.append(payload)
        pos = end
    return payloads


def common_sidebar_categories(payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    category_lists = [
        [item for item in payload.get("categories", []) if isinstance(item, dict)]
        for payload in payloads
    ]
    if not category_lists:
        return []

    prefix: list[dict[str, Any]] = []
    max_size = min(len(items) for items in category_lists)
    for index in range(max_size):
        candidate = category_lists[0][index]
        candidate_url = normalize_url(str(candidate.get("url") or ""))
        if not candidate_url:
            break
        if all(normalize_url(str(items[index].get("url") or "")) == candidate_url for items in category_lists):
            prefix.append(candidate)
            continue
        break
    return prefix


def infer_payload_root(
    categories: list[dict[str, Any]],
    sidebar_size: int,
    payload_root: str | None = None,
) -> str | None:
    if payload_root and payload_root != "Unknown":
        return normalize_root_name(payload_root)
    if len(categories) <= sidebar_size:
        return None
    first_content_url = normalize_url(str(categories[sidebar_size].get("url") or ""))
    return normalize_root_name(ROOT_BY_FIRST_CATEGORY_URL.get(first_content_url, ""))


def category_row(
    *,
    name: str,
    url: str,
    path: str,
    level: int,
    parent_path: str,
    source: str,
    payload_index: int | None = None,
) -> dict[str, Any]:
    normalized_url = normalize_url(url)
    row: dict[str, Any] = {
        "id": extract_category_id(normalized_url),
        "name": name,
        "path": path,
        "level": level,
        "url": normalized_url,
        "parent_path": parent_path,
        "source": source,
        "is_leaf": True,
    }
    if payload_index is not None:
        row["payload_index"] = payload_index
    return row


def build_ozon_categories_payload(
    payloads: list[dict[str, Any]],
    seed_categories: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sidebar = common_sidebar_categories(payloads)
    sidebar_size = len(sidebar)
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    def add_row(row: dict[str, Any]) -> None:
        key = (row["path"], row["url"])
        if key in seen:
            return
        seen.add(key)
        rows.append(row)

    if isinstance(seed_categories, dict):
        for root_item in seed_categories.get("categories") or []:
            if not isinstance(root_item, dict):
                continue
            root_name = normalize_root_name(str(root_item.get("name") or ""))
            root_url = normalize_url(str(root_item.get("url") or ""))
            if not root_name or not root_url:
                continue
            add_row(
                category_row(
                    name=root_name,
                    url=root_url,
                    path=root_name,
                    level=1,
                    parent_path="",
                    source="seed",
                )
            )
            for subcategory in root_item.get("subcategories") or []:
                if not isinstance(subcategory, dict):
                    continue
                name = str(subcategory.get("name") or "").strip()
                url = normalize_url(str(subcategory.get("url") or ""))
                if not name or not url:
                    continue
                add_row(
                    category_row(
                        name=name,
                        url=url,
                        path=f"{root_name} / {name}",
                        level=2,
                        parent_path=root_name,
                        source="seed",
                    )
                )

    for item in sidebar:
        name = str(item.get("name") or "").strip()
        url = normalize_url(str(item.get("url") or ""))
        if not name or not url:
            continue
        add_row(
            category_row(
                name=name,
                url=url,
                path=name,
                level=1,
                parent_path="",
                source="sidebar",
            )
        )

    unresolved_payloads: list[int] = []
    for payload_index, payload in enumerate(payloads, start=1):
        categories = [item for item in payload.get("categories", []) if isinstance(item, dict)]
        root = infer_payload_root(categories, sidebar_size, str(payload.get("root") or ""))
        if not root:
            unresolved_payloads.append(payload_index)
            continue
        for item in categories[sidebar_size:]:
            name = str(item.get("name") or "").strip()
            url = normalize_url(str(item.get("url") or ""))
            if not name or not url:
                continue
            add_row(
                category_row(
                    name=name,
                    url=url,
                    path=f"{root} / {name}",
                    level=2,
                    parent_path=root,
                    source="devtools_flat",
                    payload_index=payload_index,
                )
            )

    roots = sorted({row["path"].split(" / ", 1)[0] for row in rows if row["path"]})
    return {
        "source": "docs/ozon_category_collection.md raw DevTools payloads",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "payload_total": len(payloads),
        "sidebar_count": sidebar_size,
        "raw_category_total": sum(len(payload.get("categories", [])) for payload in payloads),
        "total": len(rows),
        "root_total": len(roots),
        "roots": roots,
        "unresolved_payloads": unresolved_payloads,
        "notes": [
            "Built from flat DevTools link dumps, not Ozon Seller API.",
            "Paths preserve root/category only because the raw extractor did not capture visual group headers.",
            "Use improved DevTools extractor for root/group/category hierarchy when collecting next batches.",
        ],
        "categories": rows,
    }


def save_ozon_categories_from_doc(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
    seed_path: str | Path | None = DEFAULT_SEED_PATH,
) -> dict[str, Any]:
    markdown = Path(input_path).read_text(encoding="utf-8")
    seed_categories = None
    if seed_path and Path(seed_path).exists():
        seed_categories = json.loads(Path(seed_path).read_text(encoding="utf-8"))
    payload = build_ozon_categories_payload(extract_json_payloads(markdown), seed_categories=seed_categories)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build flattened Ozon category tree from DevTools JSON payloads in markdown.")
    parser.add_argument("--input", default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--seed", default=DEFAULT_SEED_PATH)
    args = parser.parse_args()

    payload = save_ozon_categories_from_doc(args.input, args.output, seed_path=args.seed)
    print(f"Wrote {args.output}")
    print(f"Payloads: {payload['payload_total']}")
    print(f"Sidebar categories: {payload['sidebar_count']}")
    print(f"Categories: {payload['total']}")
    print(f"Roots: {payload['root_total']}")
    print(f"Unresolved payloads: {payload['unresolved_payloads']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
