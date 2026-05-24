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
    assert "add column if not exists last_name" in schema
    assert "add column if not exists language_code" in schema
    assert "add column if not exists last_seen_at" in schema
    assert "add column if not exists notifications_enabled" in schema
    assert "add column if not exists blocked_at" in schema
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
    assert "create table if not exists payment_events" in schema
    assert "create table if not exists broadcast_messages" in schema
    assert "create table if not exists broadcast_deliveries" in schema
    assert "photo_file_ids text" in schema
    assert "images_count int" in schema
    assert "image_guidance text" in schema
    assert "add column if not exists image_guidance" in schema
    assert "report_json text" in schema
    assert "add column if not exists report_json" in schema
    assert "alter table generations add column if not exists marketplace text" in schema
    assert "alter table generations add column if not exists mode text" in schema
    assert "alter table generations add column if not exists photo_file_ids text" in schema
    assert "alter table generations add column if not exists images_count int" in schema
    assert "alter table generations add column if not exists image_guidance text" in schema
    assert "inv_id text unique not null" in schema
    assert "status text default 'pending'" in schema
    assert "idx_image_generation_costs_session" in schema
    assert "idx_templates_user_created" in schema
    assert "idx_payment_events_inv_created" in schema
    assert "idx_broadcast_deliveries_message" in schema


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


class _FakeTransaction:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class _FakeConn:
    def __init__(self, *, fetchval_result=None, fetchrow_result=None):
        self.calls = []
        self.fetchval_result = fetchval_result
        self.fetchrow_result = fetchrow_result

    def transaction(self):
        return _FakeTransaction()

    async def execute(self, query, *args):
        self.calls.append((query, args))
        placeholders = [int(value) for value in re.findall(r"\$(\d+)", query)]
        assert max(placeholders) == len(args)
        return "UPDATE 1"

    async def fetchval(self, query, *args):
        self.calls.append((query, args))
        return self.fetchval_result

    async def fetchrow(self, query, *args):
        self.calls.append((query, args))
        return self.fetchrow_result

    async def fetch(self, query, *args):
        self.calls.append((query, args))
        return self.fetchval_result


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
async def test_upsert_user_stores_support_profile_and_refreshes_last_seen():
    conn = _FakeConn()
    db = Database("postgresql://test")
    db.pool = _FakePool(conn)

    await db.upsert_user(
        598380407,
        "alterega",
        "Egor",
        last_name="Duschenko",
        language_code="ru",
    )

    query, args = conn.calls[0]
    normalized = " ".join(query.casefold().split())
    assert "last_name" in normalized
    assert "language_code" in normalized
    assert "last_seen_at = now()" in normalized
    assert "blocked_at = null" in normalized
    assert args == (598380407, "alterega", "Egor", "Duschenko", "ru")


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


@pytest.mark.asyncio
async def test_log_payment_event_stores_sanitized_audit_payload():
    conn = _FakeConn()
    db = Database("postgresql://test")
    db.pool = _FakePool(conn)

    await db.log_payment_event(
        inv_id="abc123",
        user_id=598380407,
        event_type="result",
        status="invalid_signature",
        payload={"InvId": "abc123", "SignatureValue": "secret"},
        error_reason="invalid_signature",
    )

    query, args = conn.calls[0]
    normalized = " ".join(query.casefold().split())
    assert "insert into payment_events" in normalized
    assert "signaturevalue" not in args[4].casefold()
    assert args[:4] == ("abc123", 598380407, "result", "invalid_signature")
    assert args[5] == "invalid_signature"


@pytest.mark.asyncio
async def test_get_broadcast_recipients_filters_opt_out_and_blocked_users():
    conn = _FakeConn(fetchval_result=[])
    db = Database("postgresql://test")
    db.pool = _FakePool(conn)

    await db.get_broadcast_recipients(limit=100)

    query, args = conn.calls[0]
    normalized = " ".join(query.casefold().split())
    assert "notifications_enabled is true" in normalized
    assert "blocked_at is null" in normalized
    assert args == (100,)


@pytest.mark.asyncio
async def test_save_successful_generation_returns_id_and_stores_repeatable_metadata():
    conn = _FakeConn(fetchval_result=41)
    db = Database("postgresql://test")
    db.pool = _FakePool(conn)
    card = type(
        "Card",
        (),
        {
            "title": "Рашгард Therapy",
            "description": "Описание",
            "keywords": "#рашгард",
            "characteristics": "Цвет: Черный",
            "tokens_used": 20,
        },
    )()

    generation_id = await db.save_successful_generation(
        user_id=123,
        input_text="Рашгард Therapy",
        card=card,
        usage_mode=UsageMode.TRIAL,
        marketplace="ozon",
        mode="text_and_images",
        photo_file_ids=["photo-1"],
        images_count=3,
        image_guidance="светлый фон",
    )

    assert generation_id == 41
    insert_query, insert_args = conn.calls[-1]
    assert "returning id" in insert_query.casefold()
    assert insert_args[-5:] == ("ozon", "text_and_images", '["photo-1"]', 3, "светлый фон")


@pytest.mark.asyncio
async def test_save_image_only_generation_stores_repeatable_metadata():
    conn = _FakeConn(fetchval_result=42)
    db = Database("postgresql://test")
    db.pool = _FakePool(conn)

    generation_id = await db.save_image_only_generation(
        user_id=123,
        input_text="Часы песочные",
        marketplace="ozon",
        photo_file_ids=["photo-1"],
        images_count=3,
        image_guidance="чистый фон",
    )

    assert generation_id == 42
    query, args = conn.calls[-1]
    assert "insert into generations" in query.casefold()
    assert "returning id" in query.casefold()
    assert args == (123, "Часы песочные", "ozon", "images_only", '["photo-1"]', 3, "чистый фон")


@pytest.mark.asyncio
async def test_get_generation_for_action_scopes_lookup_to_owner():
    row = {"id": 41, "user_id": 123, "input_text": "Рашгард", "marketplace": "ozon", "mode": "text_only"}
    conn = _FakeConn(fetchrow_result=row)
    db = Database("postgresql://test")
    db.pool = _FakePool(conn)

    result = await db.get_generation_for_action(41, 123)

    assert result == row
    query, args = conn.calls[-1]
    assert "where id = $1 and user_id = $2" in " ".join(query.casefold().split())
    assert args == (41, 123)
