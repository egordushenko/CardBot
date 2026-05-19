from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    bot_token: str
    openrouter_api_key: str
    cardbot_db_url: str
    trial_generations: int = 3
    openrouter_model: str = "deepseek/deepseek-v4-flash"
    site_url: str = "https://alterega.ru"
    cardbot_result_url: str = "https://alterega.ru/api/payment/robokassa/cardbot-result"
    robokassa_login: str = ""
    robokassa_password1: str = ""
    robokassa_password2: str = ""
    robokassa_test_mode: bool = False


def _parse_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    result: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            result[key] = value
    return result


def _env(name: str, defaults: dict[str, str], fallback: str = "") -> str:
    return os.environ.get(name, defaults.get(name, fallback))


def _bool_env(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings(load_dotenv_files: bool = True) -> Settings:
    defaults: dict[str, str] = {}
    if load_dotenv_files:
        # .env wins over .env.example, but existing shell env wins over both.
        defaults.update(_parse_env_file(Path(".env.example")))
        defaults.update(_parse_env_file(Path("env.example")))
        defaults.update(_parse_env_file(Path(".env")))

    return Settings(
        bot_token=_env("BOT_TOKEN", defaults),
        openrouter_api_key=_env("OPENROUTER_API_KEY", defaults),
        cardbot_db_url=_env(
            "CARDBOT_DB_URL",
            defaults,
            "postgresql://cardbot_user:password@127.0.0.1:5432/cardbot",
        ),
        trial_generations=int(_env("TRIAL_GENERATIONS", defaults, "3")),
        openrouter_model=_env(
            "OPENROUTER_MODEL", defaults, "deepseek/deepseek-v4-flash"
        ),
        site_url=_env("SITE_URL", defaults, "https://alterega.ru"),
        cardbot_result_url=_env(
            "CARDBOT_RESULT_URL",
            defaults,
            "https://alterega.ru/api/payment/robokassa/cardbot-result",
        ),
        robokassa_login=_env("ROBOKASSA_LOGIN", defaults),
        robokassa_password1=_env("ROBOKASSA_PASSWORD1", defaults),
        robokassa_password2=_env("ROBOKASSA_PASSWORD2", defaults),
        robokassa_test_mode=_bool_env(_env("ROBOKASSA_TEST_MODE", defaults, "0")),
    )
