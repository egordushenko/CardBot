from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = ROOT_DIR / "data" / "manual_marketplace_eval_results.json"
DEFAULT_JSON_PATH = ROOT_DIR / "data" / "quality_dashboard.json"
DEFAULT_MD_PATH = ROOT_DIR / "data" / "quality_dashboard.md"


def _count_characteristics(value: str) -> int:
    return len([line for line in value.splitlines() if ":" in line])


def _count_hashtags(value: str) -> int:
    return len([tag for tag in value.split() if tag.startswith("#")])


def _round(value: float) -> float:
    return round(value, 1)


def build_quality_dashboard(report: dict[str, Any]) -> dict[str, Any]:
    results = [item for item in report.get("results") or [] if isinstance(item, dict)]
    buckets: dict[str, dict[str, Any]] = {}

    for item in results:
        marketplace = str(item.get("marketplace") or "").strip() or "unknown"
        category = str(item.get("category") or "Без категории").strip() or "Без категории"
        key = f"{marketplace} / {category}"
        bucket = buckets.setdefault(
            key,
            {
                "cases": 0,
                "description_total": 0,
                "characteristics_total": 0,
                "hashtags_total": 0,
                "issue_counts": Counter(),
            },
        )
        bucket["cases"] += 1
        bucket["description_total"] += len(str(item.get("description") or ""))
        bucket["characteristics_total"] += _count_characteristics(str(item.get("characteristics") or ""))
        bucket["hashtags_total"] += _count_hashtags(str(item.get("keywords") or ""))
        bucket["issue_counts"].update(str(issue) for issue in (item.get("issues") or []))

    categories: dict[str, dict[str, Any]] = {}
    for key, bucket in sorted(buckets.items()):
        cases = max(int(bucket["cases"]), 1)
        issue_counts = dict(bucket["issue_counts"])
        categories[key] = {
            "cases": bucket["cases"],
            "avg_description_length": _round(bucket["description_total"] / cases),
            "avg_characteristics_count": _round(bucket["characteristics_total"] / cases),
            "avg_hashtags_count": _round(bucket["hashtags_total"] / cases),
            "issue_counts": issue_counts,
        }

    summary = report.get("summary") if isinstance(report.get("summary"), dict) else {}
    return {
        "source_summary": summary,
        "categories": categories,
    }


def build_dashboard_markdown(dashboard: dict[str, Any]) -> str:
    source = dashboard.get("source_summary") or {}
    lines = [
        "# Quality dashboard",
        "",
        f"- Total cases: {source.get('total', 0)}",
        f"- Passed: {source.get('passed', 0)}",
        f"- Failed: {source.get('failed', 0)}",
        "",
        "| Category | Cases | Avg description | Avg characteristics | Avg hashtags | Issues |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for category, stats in (dashboard.get("categories") or {}).items():
        issues = stats.get("issue_counts") or {}
        issue_text = ", ".join(f"{name}: {count}" for name, count in issues.items()) or "none"
        lines.append(
            "| "
            + " | ".join(
                [
                    category,
                    str(stats.get("cases", 0)),
                    str(stats.get("avg_description_length", 0)),
                    str(stats.get("avg_characteristics_count", 0)),
                    str(stats.get("avg_hashtags_count", 0)),
                    issue_text,
                ]
            )
            + " |"
        )
    return "\n".join(lines).strip() + "\n"


def write_quality_dashboard(
    input_path: str | Path = DEFAULT_INPUT_PATH,
    json_path: str | Path = DEFAULT_JSON_PATH,
    md_path: str | Path = DEFAULT_MD_PATH,
) -> dict[str, Any]:
    source_path = Path(input_path)
    report = json.loads(source_path.read_text(encoding="utf-8"))
    dashboard = build_quality_dashboard(report)
    Path(json_path).write_text(json.dumps(dashboard, ensure_ascii=False, indent=2), encoding="utf-8")
    Path(md_path).write_text(build_dashboard_markdown(dashboard), encoding="utf-8")
    return dashboard


def main() -> int:
    parser = argparse.ArgumentParser(description="Build compact CardBot quality dashboard from eval JSON.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT_PATH))
    parser.add_argument("--json", default=str(DEFAULT_JSON_PATH))
    parser.add_argument("--md", default=str(DEFAULT_MD_PATH))
    args = parser.parse_args()
    write_quality_dashboard(args.input, args.json, args.md)
    print(f"Wrote {args.json}")
    print(f"Wrote {args.md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
