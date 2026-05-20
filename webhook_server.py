from __future__ import annotations

import logging
from decimal import Decimal, InvalidOperation
from typing import Any

from aiohttp import web

from payments import PACKAGES, format_out_sum, robokassa_result_signature


logger = logging.getLogger(__name__)


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

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", port)
    await site.start()
    logger.info("CardBot webhook server started on 127.0.0.1:%s", port)
    return runner
