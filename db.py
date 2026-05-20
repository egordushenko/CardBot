from __future__ import annotations

import json
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

IMAGE_PACKAGES = {
    "img_mini": {
        "name": "Мини",
        "images": 5,
        "price_rub": 199,
        "description": "5 изображений",
    },
    "img_standard": {
        "name": "Стандарт",
        "images": 10,
        "price_rub": 590,
        "description": "10 изображений",
    },
    "img_pro": {
        "name": "Про",
        "images": 25,
        "price_rub": 1290,
        "description": "25 изображений",
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

ALTER TABLE users ADD COLUMN IF NOT EXISTS image_balance INT DEFAULT 0;

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

CREATE TABLE IF NOT EXISTS image_sessions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    product_description TEXT,
    marketplace TEXT,
    photos_count INT,
    images_requested INT,
    prompts_json TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS generated_images (
    id SERIAL PRIMARY KEY,
    session_id INT REFERENCES image_sessions(id),
    user_id BIGINT REFERENCES users(id),
    image_index INT,
    prompt_used TEXT,
    telegram_file_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS templates (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    name TEXT NOT NULL,
    marketplace TEXT NOT NULL,
    mode TEXT NOT NULL,
    description TEXT NOT NULL,
    photo_file_ids TEXT,
    images_count INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_generations_user_created
    ON generations(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_payments_user_created
    ON payments(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_image_sessions_user_created
    ON image_sessions(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_generated_images_session
    ON generated_images(session_id, image_index);
CREATE INDEX IF NOT EXISTS idx_templates_user_created
    ON templates(user_id, created_at DESC);
"""


class UsageMode(str, Enum):
    TRIAL = "trial"
    PAID = "paid"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class UserBalance:
    trial_used: int
    balance: int
    image_balance: int = 0


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


def image_package_rows() -> list[tuple[str, str, int, int, str]]:
    return [
        (
            code,
            package["name"],
            package["images"],
            package["price_rub"],
            package["description"],
        )
        for code, package in IMAGE_PACKAGES.items()
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
                "SELECT trial_used, balance, image_balance FROM users WHERE id = $1", user_id
            )
        if row is None:
            return UserBalance(trial_used=0, balance=0, image_balance=0)
        return UserBalance(
            trial_used=row["trial_used"],
            balance=row["balance"],
            image_balance=row["image_balance"],
        )

    async def get_image_balance(self, user_id: int) -> int:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            value = await conn.fetchval(
                "SELECT image_balance FROM users WHERE id = $1",
                user_id,
            )
        return int(value or 0)

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

    async def save_template(
        self,
        user_id: int,
        name: str,
        marketplace: str,
        mode: str,
        description: str,
        photo_file_ids: list[str] | str | None,
        images_count: int | None,
    ) -> int:
        if isinstance(photo_file_ids, list):
            photo_file_ids = json.dumps(photo_file_ids, ensure_ascii=False)
        normalized_name = (name or "").strip()[:50] or "Шаблон"
        pool = self._require_pool()
        async with pool.acquire() as conn:
            return int(
                await conn.fetchval(
                    """
                    INSERT INTO templates(
                        user_id,
                        name,
                        marketplace,
                        mode,
                        description,
                        photo_file_ids,
                        images_count
                    )
                    VALUES($1, $2, $3, $4, $5, $6, $7)
                    RETURNING id
                    """,
                    user_id,
                    normalized_name,
                    marketplace,
                    mode,
                    description,
                    photo_file_ids,
                    images_count,
                )
            )

    async def get_templates_count(self, user_id: int) -> int:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            return int(
                await conn.fetchval(
                    "SELECT COUNT(*) FROM templates WHERE user_id = $1",
                    user_id,
                )
                or 0
            )

    async def get_templates(
        self,
        user_id: int,
        offset: int = 0,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT
                    id,
                    name,
                    marketplace,
                    mode,
                    description,
                    photo_file_ids,
                    images_count,
                    created_at
                FROM templates
                WHERE user_id = $1
                ORDER BY created_at DESC
                OFFSET $2
                LIMIT $3
                """,
                user_id,
                max(offset, 0),
                max(limit, 1),
            )
        return [dict(row) for row in rows]

    async def get_template(self, template_id: int, user_id: int) -> dict[str, Any] | None:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    id,
                    user_id,
                    name,
                    marketplace,
                    mode,
                    description,
                    photo_file_ids,
                    images_count,
                    created_at
                FROM templates
                WHERE id = $1 AND user_id = $2
                """,
                template_id,
                user_id,
            )
        return dict(row) if row else None

    async def delete_template(self, template_id: int, user_id: int) -> None:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM templates WHERE id = $1 AND user_id = $2",
                template_id,
                user_id,
            )

    async def create_image_session(
        self,
        user_id: int,
        product_description: str,
        marketplace: str,
        photos_count: int,
        images_requested: int,
    ) -> int:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            return int(
                await conn.fetchval(
                    """
                    INSERT INTO image_sessions(
                        user_id,
                        product_description,
                        marketplace,
                        photos_count,
                        images_requested,
                        status
                    )
                    VALUES($1, $2, $3, $4, $5, 'pending')
                    RETURNING id
                    """,
                    user_id,
                    product_description,
                    marketplace,
                    photos_count,
                    images_requested,
                )
            )

    async def update_image_session_prompts(
        self,
        session_id: int,
        prompts_json: str,
        status: str = "generating",
    ) -> None:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE image_sessions
                SET prompts_json = $2, status = $3
                WHERE id = $1
                """,
                session_id,
                prompts_json,
                status,
            )

    async def set_image_session_status(self, session_id: int, status: str) -> None:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE image_sessions SET status = $2 WHERE id = $1",
                session_id,
                status,
            )

    async def save_generated_images_and_consume_balance(
        self,
        session_id: int,
        user_id: int,
        generated_images: list[dict[str, Any]],
    ) -> int:
        pool = self._require_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
                count = len(generated_images)
                if count:
                    status = await conn.execute(
                        """
                        UPDATE users
                        SET image_balance = image_balance - $2
                        WHERE id = $1 AND image_balance >= $2
                        """,
                        user_id,
                        count,
                    )
                    if status != "UPDATE 1":
                        raise RuntimeError("Image balance was already consumed")
                    await conn.executemany(
                        """
                        INSERT INTO generated_images(
                            session_id,
                            user_id,
                            image_index,
                            prompt_used,
                            telegram_file_id
                        )
                        VALUES($1, $2, $3, $4, $5)
                        """,
                        [
                            (
                                session_id,
                                user_id,
                                image["image_index"],
                                image["prompt_used"],
                                image["telegram_file_id"],
                            )
                            for image in generated_images
                        ],
                    )
                await conn.execute(
                    "UPDATE image_sessions SET status = $2 WHERE id = $1",
                    session_id,
                    "done" if count else "failed",
                )
                return int(
                    await conn.fetchval(
                        "SELECT image_balance FROM users WHERE id = $1",
                        user_id,
                    )
                    or 0
                )
