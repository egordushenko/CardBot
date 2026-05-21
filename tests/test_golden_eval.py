from pathlib import Path

from tools.golden_eval import evaluate_golden_cases, load_golden_cases


def test_golden_eval_fixture_has_meaningful_coverage():
    cases = load_golden_cases(Path("data/golden_eval_cases.json"))

    marketplaces = {case["marketplace"] for case in cases}
    case_ids = {case["id"] for case in cases}

    assert len(cases) >= 30
    assert marketplaces == {"wb", "ozon"}
    assert len(case_ids) == len(cases)


def test_golden_eval_cases_pass_current_quality_gates():
    cases = load_golden_cases(Path("data/golden_eval_cases.json"))
    failures = evaluate_golden_cases(cases)

    assert failures == []
