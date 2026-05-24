from config import load_settings


def test_load_settings_reads_required_environment(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "telegram-token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "openrouter-key")
    monkeypatch.setenv("CARDBOT_DB_URL", "postgresql://user:pass@127.0.0.1:5432/cardbot")
    monkeypatch.setenv("TRIAL_GENERATIONS", "5")

    settings = load_settings(load_dotenv_files=False)

    assert settings.bot_token == "telegram-token"
    assert settings.openrouter_api_key == "openrouter-key"
    assert settings.cardbot_db_url == "postgresql://user:pass@127.0.0.1:5432/cardbot"
    assert settings.trial_generations == 5


def test_load_settings_parses_admin_user_ids(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "telegram-token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "openrouter-key")
    monkeypatch.setenv("CARDBOT_DB_URL", "postgresql://user:pass@127.0.0.1:5432/cardbot")
    monkeypatch.setenv("CARDBOT_ADMIN_IDS", "123, bad, 456,123")

    settings = load_settings(load_dotenv_files=False)

    assert settings.admin_user_ids == (123, 456)


def test_load_settings_reads_gpt_image_model(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "telegram-token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "openrouter-key")
    monkeypatch.setenv("CARDBOT_DB_URL", "postgresql://user:pass@127.0.0.1:5432/cardbot")
    monkeypatch.setenv("GPT_IMAGE_MODEL", "openai/gpt-5.4-image-2")

    settings = load_settings(load_dotenv_files=False)

    assert settings.gpt_image_model == "openai/gpt-5.4-image-2"


def test_load_settings_strips_openrouter_free_suffix(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "telegram-token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "openrouter-key")
    monkeypatch.setenv("CARDBOT_DB_URL", "postgresql://user:pass@127.0.0.1:5432/cardbot")
    monkeypatch.setenv("OPENROUTER_MODEL", "deepseek/deepseek-v4-flash:free")

    settings = load_settings(load_dotenv_files=False)

    assert settings.openrouter_model == "deepseek/deepseek-v4-flash"


def test_load_settings_keeps_robokassa_values_available_but_optional(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "telegram-token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "openrouter-key")
    monkeypatch.setenv("CARDBOT_DB_URL", "postgresql://user:pass@127.0.0.1:5432/cardbot")
    monkeypatch.setenv("ROBOKASSA_LOGIN", "merchant")
    monkeypatch.setenv("ROBOKASSA_PASSWORD1", "pass1")
    monkeypatch.setenv("ROBOKASSA_PASSWORD2", "pass2")
    monkeypatch.setenv("ROBOKASSA_TEST_MODE", "1")
    monkeypatch.setenv("ROBOKASSA_SNO", "usn_income")
    monkeypatch.setenv("ROBOKASSA_PAYMENT_METHOD", "full_payment")
    monkeypatch.setenv("ROBOKASSA_PAYMENT_OBJECT", "service")
    monkeypatch.setenv("ROBOKASSA_TAX", "none")
    monkeypatch.setenv("CARDBOT_WEBHOOK_PORT", "8091")
    monkeypatch.setenv("CARDBOT_BOT_URL", "https://t.me/CaardMakerBot")
    monkeypatch.setenv("CARDBOT_OFFER_URL", "https://alterega.ru/cardbot/offer")

    settings = load_settings(load_dotenv_files=False)

    assert settings.robokassa_login == "merchant"
    assert settings.robokassa_password1 == "pass1"
    assert settings.robokassa_password2 == "pass2"
    assert settings.robokassa_test_mode is True
    assert settings.robokassa_sno == "usn_income"
    assert settings.robokassa_payment_method == "full_payment"
    assert settings.robokassa_payment_object == "service"
    assert settings.robokassa_tax == "none"
    assert settings.cardbot_webhook_port == 8091
    assert settings.cardbot_bot_url == "https://t.me/CaardMakerBot"
    assert settings.cardbot_offer_url == "https://alterega.ru/cardbot/offer"
