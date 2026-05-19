from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


TRIAL_GENERATIONS = 3

PACKAGES = {
    "starter": {
        "name": "Старт",
        "generations": 20,
        "price_rub": 390,
        "description": "20 карточек",
    },
    "basic": {
        "name": "Основной",
        "generations": 100,
        "price_rub": 990,
        "description": "100 карточек",
    },
    "pro": {
        "name": "Про",
        "generations": 300,
        "price_rub": 1990,
        "description": "300 карточек",
    },
}

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    trial_used INT DEFAULT 0,
    balance INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS generations (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    input_text TEXT NOT NULL,
    output_title TEXT,
    output_description TEXT,
    output_keywords TEXT,
    output_characteristics TEXT,
    is_trial BOOLEAN DEFAULT FALSE,
    tokens_used INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS packages (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    generations_count INT NOT NULL,
    price_rub INT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    inv_id TEXT UNIQUE NOT NULL,
    package_code TEXT NOT NULL,
    amount_rub INT NOT NULL,
    generations_count INT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    paid_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_generations_user_created
    ON generations(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_payments_user_created
    ON payments(user_id, created_at DESC);
"""


class UsageMode(str, Enum):
    TRIAL = "trial"
    PAID = "paid"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class UserBalance:
    trial_used: int
    balance: int


def package_rows() -> list[tuple[str, str, int, int, str]]:
    return [
        (
            code,
            package["name"],
            package["generations"],
            package["price_rub"],
            package["description"],
        )
        for code, package in PACKAGES.items()
    ]


def decide_usage_mode(
    trial_used: int, balance: int, trial_generations: int = TRIAL_GENERATIONS
) -> UsageMode:
    if trial_used < trial_generations:
        return UsageMode.TRIAL
    if balance > 0:
        return UsageMode.PAID
    return UsageMode.BLOCKED


class Database:
    def __init__(self, db_url: str) -> None:
        self.db_url = db_url
        self.pool: Any | None = None

    async def connect(self) -> None:
        import asyncpg

        self.pool = await asyncpg.create_pool(self.db_url, min_size=1, max_size=5)

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    def _require_pool(self) -> Any:
        if self.pool is None:
            raise RuntimeError("Database pool is not initialized")
        return self.pool

    async def init_db(self) -> None:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            await conn.execute(CREATE_TABLES_SQL)
            await conn.executemany(
                """
                INSERT INTO packages(code, name, generations_count, price_rub, description)
                VALUES($1, $2, $3, $4, $5)
                ON CONFLICT (code) DO UPDATE SET
                    name = EXCLUDED.name,
                    generations_count = EXCLUDED.generations_count,
                    price_rub = EXCLUDED.price_rub,
                    description = EXCLUDED.description
                """,
                package_rows(),
            )

    async def upsert_user(self, user_id: int, username: str | None, first_name: str | None) -> None:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users(id, username, first_name)
                VALUES($1, $2, $3)
                ON CONFLICT (id) DO UPDATE SET
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name
                """,
                user_id,
                username,
                first_name,
            )

    async def get_balance(self, user_id: int) -> UserBalance:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT trial_used, balance FROM users WHERE id = $1", user_id
            )
        if row is None:
            return UserBalance(trial_used=0, balance=0)
        return UserBalance(trial_used=row["trial_used"], balance=row["balance"])

    async def get_usage_mode(
        self, user_id: int, trial_generations: int = TRIAL_GENERATIONS
    ) -> UsageMode:
        balance = await self.get_balance(user_id)
        return decide_usage_mode(
            balance.trial_used,
            balance.balance,
            trial_generations=trial_generations,
        )

    async def save_successful_generation(
        self,
        user_id: int,
        input_text: str,
        card: Any,
        usage_mode: UsageMode,
        trial_generations: int = TRIAL_GENERATIONS,
    ) -> None:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                if usage_mode is UsageMode.TRIAL:
                    status = await conn.execute(
                        """
                        UPDATE users
                        SET trial_used = trial_used + 1
                        WHERE id = $1 AND trial_used < $2
                        """,
                        user_id,
                        trial_generations,
                    )
                elif usage_mode is UsageMode.PAID:
                    status = await conn.execute(
                        """
                        UPDATE users
                        SET balance = balance - 1
                        WHERE id = $1 AND balance > 0
                        """,
                        user_id,
                    )
                else:
                    raise RuntimeError("Cannot save blocked generation")
                if status != "UPDATE 1":
                    raise RuntimeError("Generation balance was already consumed")

                await conn.execute(
                    """
                    INSERT INTO generations(
                        user_id,
                        input_text,
                        output_title,
                        output_description,
                        output_keywords,
                        output_characteristics,
                        is_trial,
                        tokens_used
                    )
                    VALUES($1, $2, $3, $4, $5, $6, $7, $8)
                    """,
                    user_id,
                    input_text,
                    card.title,
                    card.description,
                    card.keywords,
                    card.characteristics,
                    usage_mode is UsageMode.TRIAL,
                    card.tokens_used,
                )

    async def get_recent_generations(self, user_id: int, limit: int = 5) -> list[dict[str, Any]]:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT
                    input_text,
                    output_title,
                    output_description,
                    output_keywords,
                    output_characteristics,
                    is_trial,
                    created_at
                FROM generations
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT $2
                """,
                user_id,
                limit,
            )
        return [dict(row) for row in rows]
