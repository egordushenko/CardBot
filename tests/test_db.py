import pytest

from db import (
    CREATE_TABLES_SQL,
    TRIAL_GENERATIONS,
    UsageMode,
    decide_usage_mode,
    package_rows,
)


def test_schema_creates_users_generations_packages_and_payments_tables():
    schema = CREATE_TABLES_SQL.lower()

    assert "create table if not exists users" in schema
    assert "create table if not exists generations" in schema
    assert "create table if not exists packages" in schema
    assert "create table if not exists payments" in schema
    assert "inv_id text unique not null" in schema
    assert "status text default 'pending'" in schema


@pytest.mark.parametrize(
    ("trial_used", "balance", "expected"),
    [
        (0, 0, UsageMode.TRIAL),
        (TRIAL_GENERATIONS - 1, 0, UsageMode.TRIAL),
        (TRIAL_GENERATIONS, 2, UsageMode.PAID),
        (TRIAL_GENERATIONS, 0, UsageMode.BLOCKED),
    ],
)
def test_decide_usage_mode(trial_used, balance, expected):
    assert decide_usage_mode(trial_used=trial_used, balance=balance) == expected


def test_package_rows_match_mvp_tariffs():
    rows = package_rows()

    assert rows == [
        ("starter", "Старт", 20, 390, "20 карточек"),
        ("basic", "Основной", 100, 990, "100 карточек"),
        ("pro", "Про", 300, 1990, "300 карточек"),
    ]
