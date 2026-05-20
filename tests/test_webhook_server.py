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

    async def get_payment_by_inv_id(self, inv_id):
        return self.payment if inv_id == self.payment["inv_id"] else None

    async def mark_payment_paid_and_add_balance(self, inv_id):
        self.mark_calls += 1
        self.payment["status"] = "paid"
        return True

    async def get_user(self, user_id):
        return {"balance": 3, "image_balance": 20}


class FakeBot:
    def __init__(self):
        self.messages = []

    async def send_message(self, chat_id, text):
        self.messages.append((chat_id, text))


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
    assert bot.messages[0][0] == 598380407
    assert "+20" in bot.messages[0][1]


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
    assert bot.messages == []


def test_cardbot_offer_html_is_public_and_contains_contacts():
    html = build_cardbot_offer_html()

    assert "Публичная оферта CardBot" in html
    assert "alterega@list.ru" in html
    assert "Telegram-бот CardBot" in html
    assert "615422982815" in html
    assert "AEGACut" not in html


@pytest.mark.asyncio
async def test_cardbot_offer_handler_returns_html():
    response = await handle_cardbot_offer(FakeGetRequest())

    assert response.status == 200
    assert response.content_type == "text/html"
    assert "Публичная оферта CardBot" in response.text
