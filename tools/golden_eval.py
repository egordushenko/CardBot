from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from category_profiles import (
    detect_wb_category_profile,
    get_category_profile,
    load_category_profiles,
    load_wb_category_profiles,
)
from llm import LLMResponseError, parse_generation_payload
from ozon_generation_quality import apply_ozon_generation_quality
from wb_generation_quality import apply_wb_generation_quality, parse_characteristics_text


DEFAULT_CASES_PATH = Path("data/golden_eval_cases.json")


def load_golden_cases(path: str | Path = DEFAULT_CASES_PATH) -> list[dict[str, Any]]:
    cases_path = Path(path)
    data = json.loads(cases_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Golden eval cases must be a JSON array")
    return [case for case in data if isinstance(case, dict)]


def _category_profile(case: dict[str, Any]) -> dict[str, Any] | None:
    marketplace = str(case.get("marketplace") or "").strip().lower()
    user_input = str(case.get("user_input") or "")
    expected_category = case.get("expected_category")

    if marketplace == "wb":
        profiles = load_wb_category_profiles()
        profile = detect_wb_category_profile(profiles, user_input)
        if expected_category is not None:
            actual = profile.get("category") if profile else None
            if actual != expected_category:
                return {"__category_error__": actual}
        return profile

    if marketplace == "ozon" and expected_category:
        return get_category_profile(load_category_profiles(), str(expected_category))
    return None


def _render_case(case: dict[str, Any]) -> tuple[dict[str, str], str | None]:
    marketplace = str(case.get("marketplace") or "").strip().lower()
    raw_generation = case.get("raw_generation")
    if not isinstance(raw_generation, dict):
        return {}, "raw_generation must be an object"

    profile = _category_profile(case)
    if profile and "__category_error__" in profile:
        expected = case.get("expected_category")
        actual = profile.get("__category_error__")
        return {}, f"category mismatch: expected {expected!r}, got {actual!r}"

    try:
        card = parse_generation_payload(
            json.dumps(raw_generation, ensure_ascii=False),
            marketplace=marketplace,
        )
    except LLMResponseError as exc:
        return {}, f"parse error: {exc}"

    if marketplace == "wb":
        card = apply_wb_generation_quality(card, profile, user_input=str(case.get("user_input") or ""))
    elif marketplace == "ozon":
        card = apply_ozon_generation_quality(card, profile, user_input=str(case.get("user_input") or ""))
    else:
        return {}, f"unsupported marketplace: {marketplace}"

    return parse_characteristics_text(card.characteristics), None


def evaluate_golden_cases(cases: list[dict[str, Any]]) -> list[str]:
    failures: list[str] = []
    for index, case in enumerate(cases):
        case_id = str(case.get("id") or f"case_{index}")
        fields, error = _render_case(case)
        if error:
            failures.append(f"{case_id}: {error}")
            continue

        for field in case.get("expected_present_fields") or []:
            if field not in fields:
                failures.append(f"{case_id}: missing expected field {field!r}")

        for field in case.get("expected_absent_fields") or []:
            if field in fields:
                failures.append(f"{case_id}: forbidden field survived {field!r}")

        for field, expected_value in (case.get("expected_field_values") or {}).items():
            actual_value = fields.get(field)
            if actual_value != expected_value:
                failures.append(
                    f"{case_id}: field {field!r} expected {expected_value!r}, got {actual_value!r}"
                )

        if any(value.startswith("[укажите") for value in fields.values()):
            failures.append(f"{case_id}: placeholder survived")

    return failures


def main() -> int:
    failures = evaluate_golden_cases(load_golden_cases())
    if failures:
        print("\n".join(failures))
        return 1
    print("Golden eval passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
