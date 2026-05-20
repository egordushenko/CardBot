from __future__ import annotations

import logging
from decimal import Decimal, InvalidOperation
from typing import Any

from aiohttp import web

from payments import PACKAGES, format_out_sum, robokassa_result_signature


logger = logging.getLogger(__name__)


def build_cardbot_offer_html() -> str:
    return """<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Публичная оферта CardBot</title>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.55; color: #111827; margin: 0; background: #f8fafc; }
    main { max-width: 860px; margin: 0 auto; padding: 40px 20px 64px; background: #ffffff; }
    h1, h2 { line-height: 1.2; }
    h1 { margin-top: 0; font-size: 32px; }
    h2 { margin-top: 32px; font-size: 22px; }
    p, li { font-size: 16px; }
    a { color: #1d4ed8; }
  </style>
</head>
<body>
<main>
  <h1>Публичная оферта CardBot</h1>
  <p>Настоящая публичная оферта определяет условия оказания цифровой услуги через Telegram-бот CardBot.</p>

  <h2>1. Общие положения</h2>
  <p>Оферта является предложением Продавца заключить договор оказания цифровой услуги на условиях, изложенных ниже. Акцептом оферты считается оплата выбранного пакета генераций в Telegram-боте CardBot.</p>
  <p>Сервис CardBot доступен через Telegram-бот <a href="https://t.me/CaardMakerBot">@CaardMakerBot</a>.</p>

  <h2>2. Предмет договора</h2>
  <p>Продавец предоставляет Покупателю доступ к цифровому сервису генерации SEO-карточек товаров и изображений для маркетплейсов Wildberries и Ozon.</p>
  <p>После успешной оплаты выбранного пакета баланс Покупателя в CardBot пополняется автоматически на количество текстовых генераций и/или изображений, указанное в тарифе.</p>

  <h2>3. Порядок оплаты и оказания услуги</h2>
  <p>Стоимость пакетов отображается в Telegram-боте CardBot до оплаты. Оплата производится безналичным способом через Robokassa.</p>
  <p>Услуга считается оказанной в части пополнения баланса с момента автоматического зачисления оплаченного пакета на аккаунт Покупателя в Telegram.</p>

  <h2>4. Возвраты и обращения</h2>
  <p>Если после оплаты баланс не был зачислен автоматически, Покупатель может обратиться по e-mail <a href="mailto:alterega@list.ru">alterega@list.ru</a>. В обращении нужно указать Telegram ID и данные платежа.</p>
  <p>Возвраты и спорные ситуации рассматриваются индивидуально в соответствии с законодательством Российской Федерации.</p>

  <h2>5. Ограничения ответственности</h2>
  <p>CardBot генерирует материалы автоматически с использованием AI-моделей. Покупатель самостоятельно проверяет итоговые тексты и изображения перед публикацией на маркетплейсах.</p>

  <h2>6. Конфиденциальность</h2>
  <p>Продавец обрабатывает данные, необходимые для работы сервиса: Telegram ID, историю запросов, сведения о платежах и балансе. Эти данные используются для оказания услуги, поддержки и учета платежей.</p>

  <h2>7. Контакты и реквизиты</h2>
  <p>ИНН: 615422982815</p>
  <p>Контактный e-mail: <a href="mailto:alterega@list.ru">alterega@list.ru</a></p>
  <p>Контактный телефон: +7 961 306-16-40</p>
</main>
</body>
</html>"""


async def handle_cardbot_offer(request: Any) -> web.Response:
    return web.Response(
        text=build_cardbot_offer_html(),
        content_type="text/html",
        charset="utf-8",
    )


def _same_amount(received: str, expected_rub: int) -> bool:
    try:
        received_amount = Decimal(received).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return False
    return received_amount == Decimal(format_out_sum(expected_rub))


async def handle_robokassa_result(request: Any) -> web.Response:
    data = await request.post()

    out_sum = str(data.get("OutSum", ""))
    inv_id = str(data.get("InvId", ""))
    signature = str(data.get("SignatureValue") or data.get("signature") or data.get("crc") or "")
    user_id = str(data.get("Shp_user_id", ""))
    package_code = str(data.get("Shp_package", ""))
    password2 = request.app["robokassa_password2"]

    expected = robokassa_result_signature(
        out_sum=out_sum,
        inv_id=inv_id,
        password2=password2,
        shp_params={
            "Shp_package": package_code,
            "Shp_user_id": user_id,
        },
    )
    if signature.upper() != expected:
        logger.warning("Invalid Robokassa signature for InvId=%s", inv_id)
        return web.Response(text="Invalid signature", status=400)

    db = request.app["db"]
    payment = await db.get_payment_by_inv_id(inv_id)
    if not payment:
        logger.warning("Robokassa payment not found: InvId=%s", inv_id)
        return web.Response(text=f"OK{inv_id}")

    if payment["status"] == "paid":
        return web.Response(text=f"OK{inv_id}")

    if payment["package_code"] != package_code or str(payment["user_id"]) != user_id:
        logger.warning("Robokassa Shp mismatch for InvId=%s", inv_id)
        return web.Response(text="Payment mismatch", status=400)

    if package_code not in PACKAGES:
        logger.error("Unknown CardBot payment package: %s", package_code)
        return web.Response(text="Unknown package", status=400)

    if not _same_amount(out_sum, int(payment["amount_rub"])):
        logger.warning("Robokassa amount mismatch for InvId=%s", inv_id)
        return web.Response(text="Amount mismatch", status=400)

    paid_now = await db.mark_payment_paid_and_add_balance(inv_id)
    if paid_now:
        logger.info(
            "CardBot payment OK: user=%s package=%s text=%s images=%s",
            user_id,
            package_code,
            payment["text_count"],
            payment["images_count"],
        )
        await _notify_user_about_payment(request.app["bot"], db, int(user_id), payment)

    return web.Response(text=f"OK{inv_id}")


async def _notify_user_about_payment(bot: Any, db: Any, user_id: int, payment: dict[str, Any]) -> None:
    user = await db.get_user(user_id)
    if not user:
        return
    await bot.send_message(
        chat_id=user_id,
        text=(
            "✅ Оплата получена!\n\n"
            "Зачислено:\n"
            f"📝 Текстовых карточек: +{payment['text_count']}\n"
            f"🖼 Изображений: +{payment['images_count']}\n\n"
            "Текущий баланс:\n"
            f"📝 {user['balance']} карточек\n"
            f"🖼 {user['image_balance']} изображений"
        ),
    )


async def start_webhook_server(
    *,
    bot: Any,
    db: Any,
    robokassa_password2: str,
    port: int = 8090,
) -> web.AppRunner | None:
    if not robokassa_password2:
        logger.warning("ROBOKASSA_PASSWORD2 is not configured; webhook server is disabled")
        return None

    app = web.Application()
    app["bot"] = bot
    app["db"] = db
    app["robokassa_password2"] = robokassa_password2
    app.router.add_post("/robokassa/result", handle_robokassa_result)
    app.router.add_post("/api/payment/robokassa/cardbot-result", handle_robokassa_result)
    app.router.add_get("/cardbot/offer", handle_cardbot_offer)
    app.router.add_get("/offer-cardbot", handle_cardbot_offer)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", port)
    await site.start()
    logger.info("CardBot webhook server started on 127.0.0.1:%s", port)
    return runner
