import re

import pytest

from db import (
    CREATE_TABLES_SQL,
    Database,
    IMAGE_PACKAGES,
    TRIAL_GENERATIONS,
    UsageMode,
    decide_usage_mode,
    image_package_rows,
    package_rows,
)


def test_schema_creates_users_generations_packages_and_payments_tables():
    schema = CREATE_TABLES_SQL.lower()

    assert "create table if not exists users" in schema
    assert "add column if not exists image_balance" in schema
    assert "create table if not exists generations" in schema
    assert "create table if not exists packages" in schema
    assert "create table if not exists payments" in schema
    assert "add column if not exists text_count" in schema
    assert "add column if not exists images_count" in schema
    assert "create table if not exists image_sessions" in schema
    assert "create table if not exists generated_images" in schema
    assert "create table if not exists image_generation_costs" in schema
    assert "cost_usd numeric(12,6)" in schema
    assert "failed_count int default 0" in schema
    assert "create table if not exists templates" in schema
    assert "photo_file_ids text" in schema
    assert "images_count int" in schema
    assert "image_guidance text" in schema
    assert "add column if not exists image_guidance" in schema
    assert "inv_id text unique not null" in schema
    assert "status text default 'pending'" in schema
    assert "idx_image_generation_costs_session" in schema
    assert "idx_templates_user_created" in schema


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


def test_image_package_rows_match_image_tariffs():
    rows = image_package_rows()

    assert rows == [
        ("img_mini", "Мини", 5, 199, "5 изображений"),
        ("img_standard", "Стандарт", 10, 590, "10 изображений"),
        ("img_pro", "Про", 25, 1290, "25 изображений"),
    ]
    assert IMAGE_PACKAGES["img_pro"]["images"] == 25


class _FakeConn:
    def __init__(self):
        self.calls = []

    async def execute(self, query, *args):
        self.calls.append((query, args))
        placeholders = [int(value) for value in re.findall(r"\$(\d+)", query)]
        assert max(placeholders) == len(args)


class _FakeAcquire:
    def __init__(self, conn):
        self.conn = conn

    async def __aenter__(self):
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        return False


class _FakePool:
    def __init__(self, conn):
        self.conn = conn

    def acquire(self):
        return _FakeAcquire(self.conn)


@pytest.mark.asyncio
async def test_create_pending_payment_uses_matching_sql_arguments():
    conn = _FakeConn()
    db = Database("postgresql://test")
    db.pool = _FakePool(conn)

    await db.create_pending_payment(
        inv_id="abc123",
        user_id=598380407,
        package_code="text_pro_x5",
        amount_rub=22990,
        text_count=100,
        images_count=500,
    )

    _, args = conn.calls[0]
    assert args == (598380407, "abc123", "text_pro_x5", 22990, 100, 500)
