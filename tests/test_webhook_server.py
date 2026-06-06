import pytest

from payments import robokassa_result_signature
from webhook_server import build_cardbot_offer_html, handle_cardbot_offer, handle_robokassa_result


class FakeRequest:
    def __init__(self, form, app):
        self._form = form
        self.app = app

    async def post(self):
        return self._form


class FakeGetRequest:
    app = {}


class FakeDb:
    def __init__(self):
        self.payment = {
            "inv_id": "abc123",
            "user_id": 598380407,
            "package_code": "addon_img_20",
            "amount_rub": 1150,
            "text_count": 0,
            "images_count": 20,
            "status": "pending",
        }
        self.mark_calls = 0
        self.payment_events = []
        self.blocked_users = []

    async def get_payment_by_inv_id(self, inv_id):
        return self.payment if inv_id == self.payment["inv_id"] else None

    async def mark_payment_paid_and_add_balance(self, inv_id, first_purchase_only_package_codes=()):
        self.mark_calls += 1
        self.payment["status"] = "paid"
        return True

    async def get_user(self, user_id):
        return {"balance": 3, "image_balance": 20}

    async def log_payment_event(self, **kwargs):
        self.payment_events.append(kwargs)

    async def mark_user_blocked(self, user_id):
        self.blocked_users.append(user_id)


class FakeBot:
    def __init__(self):
        self.messages = []

    async def send_message(self, chat_id, text):
        self.messages.append((chat_id, text))


class BlockingBot:
    async def send_message(self, chat_id, text):
        from telegram.error import Forbidden

        raise Forbidden("bot was blocked by the user")


@pytest.mark.asyncio
async def test_robokassa_result_validates_signature_marks_paid_and_notifies_user():
    db = FakeDb()
    bot = FakeBot()
    signature = robokassa_result_signature(
        out_sum="1150.00",
        inv_id="abc123",
        password2="pass2",
        shp_params={"Shp_package": "addon_img_20", "Shp_user_id": "598380407"},
    )
    request = FakeRequest(
        {
            "OutSum": "1150.00",
            "InvId": "abc123",
            "SignatureValue": signature,
            "Shp_user_id": "598380407",
            "Shp_package": "addon_img_20",
        },
        {"db": db, "bot": bot, "robokassa_password2": "pass2"},
    )

    response = await handle_robokassa_result(request)

    assert response.status == 200
    assert response.text == "OKabc123"
    assert db.mark_calls == 1
    assert db.payment_events[-1]["status"] == "paid"
    assert bot.messages[0][0] == 598380407
    assert "+20" in bot.messages[0][1]


@pytest.mark.asyncio
async def test_robokassa_result_stays_ok_when_payment_notification_is_blocked():
    db = FakeDb()
    signature = robokassa_result_signature(
        out_sum="1150.00",
        inv_id="abc123",
        password2="pass2",
        shp_params={"Shp_package": "addon_img_20", "Shp_user_id": "598380407"},
    )
    request = FakeRequest(
        {
            "OutSum": "1150.00",
            "InvId": "abc123",
            "SignatureValue": signature,
            "Shp_user_id": "598380407",
            "Shp_package": "addon_img_20",
        },
        {"db": db, "bot": BlockingBot(), "robokassa_password2": "pass2"},
    )

    response = await handle_robokassa_result(request)

    assert response.status == 200
    assert response.text == "OKabc123"
    assert db.payment_events[-1]["status"] == "paid"
    assert db.blocked_users == [598380407]


@pytest.mark.asyncio
async def test_robokassa_result_rejects_invalid_signature_before_balance_change():
    db = FakeDb()
    bot = FakeBot()
    request = FakeRequest(
        {
            "OutSum": "1150.00",
            "InvId": "abc123",
            "SignatureValue": "bad",
            "Shp_user_id": "598380407",
            "Shp_package": "addon_img_20",
        },
        {"db": db, "bot": bot, "robokassa_password2": "pass2"},
    )

    response = await handle_robokassa_result(request)

    assert response.status == 400
    assert db.mark_calls == 0
    assert db.payment_events[-1]["status"] == "invalid_signature"
    assert bot.messages == []


@pytest.mark.asyncio
async def test_robokassa_result_is_idempotent_for_already_paid_payment():
    db = FakeDb()
    db.payment["status"] = "paid"
    bot = FakeBot()
    signature = robokassa_result_signature(
        out_sum="1150.00",
        inv_id="abc123",
        password2="pass2",
        shp_params={"Shp_package": "addon_img_20", "Shp_user_id": "598380407"},
    )
    request = FakeRequest(
        {
            "OutSum": "1150.00",
            "InvId": "abc123",
            "SignatureValue": signature,
            "Shp_user_id": "598380407",
            "Shp_package": "addon_img_20",
        },
        {"db": db, "bot": bot, "robokassa_password2": "pass2"},
    )

    response = await handle_robokassa_result(request)

    assert response.status == 200
    assert response.text == "OKabc123"
    assert db.mark_calls == 0
    assert db.payment_events[-1]["status"] == "already_paid"
    assert bot.messages == []


@pytest.mark.asyncio
async def test_robokassa_result_rejects_stale_first_purchase_discount_invoice():
    class UsedFirstPurchaseDb(FakeDb):
        async def mark_payment_paid_and_add_balance(self, inv_id, first_purchase_only_package_codes=()):
            self.mark_calls += 1
            assert "first_text_pro_x7" in first_purchase_only_package_codes
            return False

    db = UsedFirstPurchaseDb()
    db.payment.update(
        {
            "package_code": "first_text_pro_x7",
            "amount_rub": 15495,
            "text_count": 100,
            "images_count": 700,
        }
    )
    bot = FakeBot()
    signature = robokassa_result_signature(
        out_sum="15495.00",
        inv_id="abc123",
        password2="pass2",
        shp_params={"Shp_package": "first_text_pro_x7", "Shp_user_id": "598380407"},
    )
    request = FakeRequest(
        {
            "OutSum": "15495.00",
            "InvId": "abc123",
            "SignatureValue": signature,
            "Shp_user_id": "598380407",
            "Shp_package": "first_text_pro_x7",
        },
        {"db": db, "bot": bot, "robokassa_password2": "pass2"},
    )

    response = await handle_robokassa_result(request)

    assert response.status == 400
    assert db.mark_calls == 1
    assert db.payment_events[-1]["status"] == "first_purchase_used"
    assert bot.messages == []


def test_cardbot_offer_html_is_public_and_contains_contacts():
    html = build_cardbot_offer_html()

    assert "Публичная оферта CardBot" in html
    assert "alterega@list.ru" in html
    assert "Telegram-бот CardBot" in html
    assert "615422982815" in html
    assert "+244 931 150 124" in html
    assert html.count("<h2") >= 10
    for heading in [
        "1. Общие положения",
        "2. Предмет Договора",
        "3. Права и обязанности Сторон",
        "4. Цена и порядок расчетов",
        "5. Порядок оказания цифровой услуги и возвраты",
        "6. Конфиденциальность и безопасность",
        "7. Форс-мажор",
        "8. Ответственность Сторон",
        "9. Срок действия настоящей Оферты",
        "10. Дополнительные условия",
        "Реквизиты Продавца",
    ]:
        assert heading in html
    assert "@CaardMakerBot" in html
    assert "Robokassa" in html
    assert "Wildberries" in html
    assert "Ozon" in html
    assert "AEGACut" not in html
    assert "AEGA Panel" not in html
    assert "AEGASync" not in html


@pytest.mark.asyncio
async def test_cardbot_offer_handler_returns_html():
    response = await handle_cardbot_offer(FakeGetRequest())

    assert response.status == 200
    assert response.content_type == "text/html"
    assert "Публичная оферта CardBot" in response.text
