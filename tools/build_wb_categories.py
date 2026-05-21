from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SOURCE_URL = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"
DEFAULT_OUTPUT_PATH = "data/wb_categories.json"
WB_URL_PREFIX = "https://www.wildberries.ru"


def _full_wb_url(path: str) -> str:
    value = str(path or "").strip()
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if not value.startswith("/"):
        value = f"/{value}"
    return f"{WB_URL_PREFIX}{value}"


def flatten_wb_menu(
    nodes: list[dict[str, Any]],
    parent_path: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in nodes:
        name = str(node.get("name") or "").strip()
        if not name:
            continue

        path_parts = parent_path + (name,)
        children = node.get("childs") if isinstance(node.get("childs"), list) else []
        row = {
            "id": node.get("id"),
            "name": name,
            "path": " / ".join(path_parts),
            "level": len(path_parts),
            "url": _full_wb_url(str(node.get("url") or "")),
            "query": str(node.get("query") or ""),
            "parent_path": " / ".join(parent_path),
            "children_count": len(children),
            "is_leaf": len(children) == 0,
        }
        rows.append(row)
        rows.extend(flatten_wb_menu(children, path_parts))
    return rows


def build_wb_categories_payload(
    menu: list[dict[str, Any]],
    *,
    source_url: str = DEFAULT_SOURCE_URL,
) -> dict[str, Any]:
    categories = flatten_wb_menu(menu)
    return {
        "source_url": source_url,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(categories),
        "leaf_total": sum(1 for item in categories if item["is_leaf"]),
        "max_level": max((int(item["level"]) for item in categories), default=0),
        "categories": categories,
    }


def fetch_wb_menu(source_url: str = DEFAULT_SOURCE_URL) -> list[dict[str, Any]]:
    with urllib.request.urlopen(source_url, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise ValueError("WB menu payload must be a JSON array")
    return [item for item in payload if isinstance(item, dict)]


def save_wb_categories(
    output_path: str | Path = DEFAULT_OUTPUT_PATH,
    *,
    source_url: str = DEFAULT_SOURCE_URL,
) -> dict[str, Any]:
    payload = build_wb_categories_payload(fetch_wb_menu(source_url), source_url=source_url)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build flattened Wildberries category tree.")
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()

    payload = save_wb_categories(args.output, source_url=args.source_url)
    print(f"Wrote {args.output}")
    print(f"Categories: {payload['total']}")
    print(f"Leaves: {payload['leaf_total']}")
    print(f"Max level: {payload['max_level']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
