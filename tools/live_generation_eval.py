from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Awaitable, Callable

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from category_profiles import (
    detect_wb_category_profile,
    get_category_profile,
    load_category_profiles,
    load_wb_category_profiles,
)
from config import load_settings
from llm import CardGeneration, generate_card, normalize_marketplace
from tools.card_quality_eval import evaluate_card_quality, summarize_quality_results


DEFAULT_CASES_PATH = ROOT_DIR / "data" / "live_generation_eval_cases.json"
DEFAULT_JSON_REPORT_PATH = ROOT_DIR / "data" / "live_generation_eval.json"
DEFAULT_MD_REPORT_PATH = ROOT_DIR / "data" / "live_generation_eval.md"

Generator = Callable[[dict[str, Any], dict[str, Any] | None], Awaitable[CardGeneration]]


def load_live_eval_cases(path: str | Path = DEFAULT_CASES_PATH) -> list[dict[str, Any]]:
    cases_path = Path(path)
    data = json.loads(cases_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Live eval cases must be a JSON array")
    return [case for case in data if isinstance(case, dict)]


def resolve_category_profile(case: dict[str, Any]) -> dict[str, Any] | None:
    marketplace = normalize_marketplace(str(case.get("marketplace") or ""))
    user_input = str(case.get("user_input") or "")
    if marketplace == "wb":
        return detect_wb_category_profile(load_wb_category_profiles(), user_input)

    category = str(case.get("category") or "").strip()
    if not category:
        return None
    return get_category_profile(load_category_profiles(), category)


async def run_live_eval(
    cases: list[dict[str, Any]],
    generator: Generator,
    retries: int = 1,
    retry_delay_seconds: float = 1,
    case_timeout_seconds: float = 120,
) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for case in cases:
        category_profile = resolve_category_profile(case)
        card: CardGeneration | None = None
        generation_error: Exception | None = None
        for attempt in range(retries + 1):
            try:
                card = await asyncio.wait_for(
                    generator(case, category_profile),
                    timeout=case_timeout_seconds,
                )
                generation_error = None
                break
            except Exception as exc:  # pragma: no cover - exact provider errors vary.
                generation_error = exc
                if attempt < retries and retry_delay_seconds > 0:
                    await asyncio.sleep(retry_delay_seconds)

        if card is None:
            issue = f"generation_error:{type(generation_error).__name__}"
            results.append(
                {
                    "id": case.get("id"),
                    "marketplace": normalize_marketplace(str(case.get("marketplace") or "")),
                    "category": case.get("category") or (category_profile or {}).get("category"),
                    "user_input": case.get("user_input"),
                    "title": "",
                    "description": "",
                    "keywords": "",
                    "characteristics": "",
                    "score": 0,
                    "issues": [issue],
                    "error": str(generation_error),
                }
            )
            continue

        quality = evaluate_card_quality(
            card,
            user_input=str(case.get("user_input") or ""),
            category_profile=category_profile,
        )
        results.append(
            {
                "id": case.get("id"),
                "marketplace": normalize_marketplace(str(case.get("marketplace") or "")),
                "category": case.get("category") or (category_profile or {}).get("category"),
                "user_input": case.get("user_input"),
                "title": card.title,
                "description": card.description,
                "keywords": card.keywords,
                "characteristics": card.characteristics,
                **quality,
            }
        )
    return {
        "summary": summarize_quality_results(results),
        "results": results,
    }


def build_markdown_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Live generation quality eval",
        "",
        f"- Total: {summary['total']}",
        f"- Passed: {summary['passed']} / {summary['total']}",
        f"- Failed: {summary['failed']}",
        f"- Average score: {summary['avg_score']}",
        "",
        "## Issue counts",
        "",
    ]
    issue_counts = summary.get("issue_counts") or {}
    if issue_counts:
        for issue, count in issue_counts.items():
            lines.append(f"- {issue}: {count}")
    else:
        lines.append("- none")

    lines.extend(["", "## Cases", ""])
    for result in report.get("results", []):
        issues = ", ".join(result.get("issues") or ["ok"])
        lines.extend(
            [
                f"### {result.get('id')}",
                "",
                f"- Marketplace: {result.get('marketplace')}",
                f"- Category: {result.get('category') or ''}",
                f"- Score: {result.get('score')}",
                f"- Issues: {issues}",
                f"- Title: {result.get('title')}",
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def _filter_cases(
    cases: list[dict[str, Any]],
    marketplace: str | None,
    limit: int | None,
) -> list[dict[str, Any]]:
    filtered = cases
    if marketplace:
        normalized = normalize_marketplace(marketplace)
        filtered = [
            case
            for case in filtered
            if normalize_marketplace(str(case.get("marketplace") or "")) == normalized
        ]
    if limit is not None:
        filtered = filtered[:limit]
    return filtered


async def _run_from_cli(args: argparse.Namespace) -> int:
    settings = load_settings()
    if not settings.openrouter_api_key:
        print("OPENROUTER_API_KEY is not configured; live eval was not run.")
        return 2

    cases = _filter_cases(
        load_live_eval_cases(args.cases),
        marketplace=args.marketplace,
        limit=args.limit,
    )

    async def api_generator(
        case: dict[str, Any],
        category_profile: dict[str, Any] | None,
    ) -> CardGeneration:
        return await generate_card(
            str(case["user_input"]),
            api_key=settings.openrouter_api_key,
            model=settings.openrouter_model,
            site_url=settings.site_url,
            marketplace=str(case["marketplace"]),
            category_profile=category_profile,
        )

    report = await run_live_eval(
        cases,
        api_generator,
        retries=args.retries,
        retry_delay_seconds=args.retry_delay_seconds,
        case_timeout_seconds=args.case_timeout_seconds,
    )
    json_path = Path(args.json_report)
    md_path = Path(args.md_report)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(build_markdown_report(report), encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Passed: {report['summary']['passed']} / {report['summary']['total']}")
    if args.fail_on_issues and report["summary"]["failed"]:
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run live CardBot generation quality eval.")
    parser.add_argument("--cases", default=str(DEFAULT_CASES_PATH))
    parser.add_argument("--json-report", default=str(DEFAULT_JSON_REPORT_PATH))
    parser.add_argument("--md-report", default=str(DEFAULT_MD_REPORT_PATH))
    parser.add_argument("--marketplace", choices=["wb", "ozon", "wildberries"])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--retry-delay-seconds", type=float, default=1)
    parser.add_argument("--case-timeout-seconds", type=float, default=120)
    parser.add_argument("--fail-on-issues", action="store_true")
    args = parser.parse_args()
    return asyncio.run(_run_from_cli(args))


if __name__ == "__main__":
    raise SystemExit(main())
