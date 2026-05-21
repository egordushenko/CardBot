import pytest

from llm import CardGeneration
from tools.live_generation_eval import (
    build_markdown_report,
    load_live_eval_cases,
    run_live_eval,
)


def test_live_eval_fixture_covers_both_marketplaces_and_ozon_dataset_categories():
    cases = load_live_eval_cases()
    marketplaces = {case["marketplace"] for case in cases}
    ozon_categories = {case.get("category") for case in cases if case["marketplace"] == "ozon"}

    assert len(cases) >= 16
    assert marketplaces == {"wb", "ozon"}
    assert {"Электроника", "Дом и сад", "Красота и здоровье", "Товары для животных"} <= ozon_categories


@pytest.mark.asyncio
async def test_run_live_eval_uses_generator_and_quality_gates():
    cases = [
        {
            "id": "wb_ok",
            "marketplace": "wb",
            "user_input": "Женская футболка оверсайз черная",
        },
        {
            "id": "ozon_bad",
            "marketplace": "ozon",
            "category": "Электроника",
            "user_input": "Беспроводные наушники черные Bluetooth",
        },
    ]

    async def fake_generator(case, category_profile):
        if case["id"] == "wb_ok":
            return CardGeneration(
                title="Футболка женская оверсайз черная",
                description=(
                    "Женская футболка оверсайз подходит для повседневных образов, прогулок "
                    "и расслабленных комплектов. Свободный крой помогает чувствовать комфорт "
                    "в течение дня, а черный цвет легко сочетается с джинсами, брюками и юбкой. "
                    "Модель можно использовать как базовый слой под рубашку, куртку или худи. "
                    "Футболка уместна дома, на учебе, в поездке и на каждый день."
                ),
                keywords="",
                characteristics=(
                    "Цвет: черный\n"
                    "Покрой: свободный\n"
                    "Пол: Женский\n"
                    "Страна производства: Китай"
                ),
                marketplace="wb",
            )
        return CardGeneration(
            title="Беспроводные наушники Bluetooth",
            description="Наушники для музыки.",
            keywords="#наушники",
            characteristics="Тип: Наушники\nBluetooth: Да",
            marketplace="ozon",
        )

    report = await run_live_eval(cases, fake_generator)

    assert report["summary"]["total"] == 2
    assert report["summary"]["passed"] == 1
    assert report["summary"]["failed"] == 1
    assert report["results"][0]["id"] == "wb_ok"
    assert report["results"][0]["issues"] == []
    assert "description_too_short" in report["results"][1]["issues"]


@pytest.mark.asyncio
async def test_run_live_eval_records_generation_errors_after_retry():
    calls = 0

    async def broken_generator(case, category_profile):
        nonlocal calls
        calls += 1
        raise RuntimeError("empty response")

    report = await run_live_eval(
        [
            {
                "id": "wb_error",
                "marketplace": "wb",
                "user_input": "Футболка женская черная",
            }
        ],
        broken_generator,
        retries=1,
        retry_delay_seconds=0,
    )

    assert calls == 2
    assert report["summary"]["failed"] == 1
    assert "generation_error:RuntimeError" in report["results"][0]["issues"]


@pytest.mark.asyncio
async def test_run_live_eval_records_generation_timeout():
    async def slow_generator(case, category_profile):
        import asyncio

        await asyncio.sleep(1)
        raise AssertionError("must time out first")

    report = await run_live_eval(
        [
            {
                "id": "wb_timeout",
                "marketplace": "wb",
                "user_input": "Футболка женская черная",
            }
        ],
        slow_generator,
        retries=0,
        case_timeout_seconds=0.01,
    )

    assert report["summary"]["failed"] == 1
    assert "generation_error:TimeoutError" in report["results"][0]["issues"]


def test_build_markdown_report_contains_summary_and_failed_cases():
    markdown = build_markdown_report(
        {
            "summary": {
                "total": 2,
                "passed": 1,
                "failed": 1,
                "avg_score": 95,
                "issue_counts": {"description_too_short": 1},
            },
            "results": [
                {
                    "id": "bad",
                    "marketplace": "ozon",
                    "title": "Товар",
                    "issues": ["description_too_short"],
                    "score": 90,
                }
            ],
        }
    )

    assert "# Live generation quality eval" in markdown
    assert "Passed: 1 / 2" in markdown
    assert "description_too_short" in markdown
