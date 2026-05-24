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
    body { font-family: Arial, sans-serif; line-height: 1.7; color: rgba(255,255,255,.78); margin: 0; background: #050607; }
    main { max-width: 860px; margin: 0 auto; padding: 56px 24px 72px; }
    h1, h2 { line-height: 1.2; }
    h1 { margin: 24px 0 0; font-size: 40px; color: #fff; letter-spacing: .04em; }
    h2 { margin-top: 40px; font-size: 22px; color: #fff; }
    p, li { font-size: 16px; }
    a { color: #fff; text-decoration-color: rgba(255,255,255,.45); text-underline-offset: 4px; }
    strong { color: #fff; }
    ul { margin-top: 12px; padding-left: 24px; }
    .home { font-size: 12px; text-transform: uppercase; letter-spacing: .3em; color: rgba(255,255,255,.45); }
    .lead { color: rgba(255,255,255,.6); }
    .requisites { margin-top: 16px; padding: 20px; border: 1px solid rgba(255,255,255,.1); border-radius: 16px; background: rgba(255,255,255,.05); }
  </style>
</head>
<body>
<main>
  <a class="home" href="https://t.me/CaardMakerBot">В бот</a>
  <h1>Публичная оферта CardBot</h1>
  <p class="lead">Актуальная редакция условий оказания цифровых услуг через Telegram-бот CardBot.</p>

  <h2>1. Общие положения</h2>
  <p>В настоящей Публичной оферте содержатся условия заключения Договора оказания цифровых услуг (далее по тексту - «Договор»). Настоящей офертой признается предложение Продавца, адресованное заинтересованному кругу лиц, заключить Договор на условиях, в порядке и объеме, изложенных ниже.</p>
  <p>Совершение указанных в настоящей Оферте действий является подтверждением согласия Сторон заключить Договор. Договор считается заключенным и приобретает силу с момента совершения Покупателем действий, означающих безоговорочное и полное принятие всех условий настоящей Оферты.</p>
  <p>Нижеизложенный текст Публичной оферты является официальным публичным предложением Продавца в соответствии с положениями пункта 2 статьи 437 Гражданского кодекса Российской Федерации.</p>
  <p><strong>Термины и определения:</strong></p>
  <p><strong>Договор</strong> - текст настоящей Оферты, акцептованный Покупателем путем совершения конклюдентных действий, предусмотренных настоящей Офертой.</p>
  <p><strong>Конклюдентные действия</strong> - поведение Покупателя, выражающее согласие заключить Договор, включая выбор пакета генераций, переход к оплате, оплату пакета, использование Telegram-бота CardBot и иных функций сервиса.</p>
  <p><strong>Сервис CardBot</strong> - Telegram-бот <a href="https://t.me/CaardMakerBot">@CaardMakerBot</a>, предназначенный для генерации SEO-карточек товаров, текстов, характеристик, ключевых слов, хэштегов и изображений для маркетплейсов Wildberries и Ozon.</p>
  <p><strong>Стороны Договора</strong> - Продавец и Покупатель.</p>
  <p><strong>Покупатель</strong> - физическое или юридическое лицо, совершившее акцепт настоящей Оферты и использующее Сервис CardBot.</p>
  <p><strong>Цифровая услуга</strong> - предоставление доступа к функциональности Сервиса CardBot и зачисление оплаченного пакета генераций на баланс Покупателя.</p>
  <p><strong>Пакет генераций</strong> - определенное количество текстовых генераций и/или изображений, отображаемое в Telegram-боте CardBot до оплаты.</p>
  <p><strong>Баланс</strong> - учет доступного Покупателю количества оплаченных и/или пробных генераций внутри Сервиса CardBot.</p>

  <h2>2. Предмет Договора</h2>
  <p>2.1. По настоящему Договору Продавец обязуется предоставить Покупателю доступ к цифровой услуге CardBot, а Покупатель обязуется принять услугу и оплатить выбранный пакет генераций.</p>
  <p>2.2. Сервис CardBot помогает создавать материалы для карточек товаров на маркетплейсах Wildberries и Ozon: названия, описания, характеристики, ключевые слова, хэштеги, а также изображения на основе предоставленных Покупателем сведений и материалов.</p>
  <p>2.3. Наименование, состав, количество генераций, стоимость пакета и иные существенные условия определяются сведениями, отображаемыми в Telegram-боте CardBot при оформлении заказа.</p>
  <p>2.4. Акцепт настоящей Оферты выражается в совершении конклюдентных действий, в частности:</p>
  <ul>
    <li>запуске или использовании Telegram-бота CardBot;</li>
    <li>выборе пакета генераций в меню Сервиса;</li>
    <li>переходе по платежной ссылке, сформированной Сервисом;</li>
    <li>оплате выбранного пакета генераций через Robokassa;</li>
    <li>использовании зачисленного баланса для генерации материалов.</li>
  </ul>
  <p>2.5. Данный перечень не является исчерпывающим. Акцептом могут считаться иные действия, которые ясно выражают намерение Покупателя принять условия настоящей Оферты.</p>

  <h2>3. Права и обязанности Сторон</h2>
  <p>3.1. Продавец вправе:</p>
  <ul>
    <li>требовать оплаты выбранного пакета генераций в порядке и на условиях, предусмотренных настоящей Офертой;</li>
    <li>изменять функциональность Сервиса CardBot, состав тарифов и стоимость пакетов до момента оплаты Покупателем;</li>
    <li>приостанавливать работу Сервиса для технического обслуживания, обновлений, устранения ошибок или по причинам, связанным с работой Telegram, Robokassa, AI-провайдеров и иных третьих лиц;</li>
    <li>отказать в обслуживании при недобросовестном использовании Сервиса, попытках обхода ограничений, злоупотреблении пробным периодом, нарушении законодательства Российской Федерации или прав третьих лиц.</li>
  </ul>
  <p>3.2. Продавец обязуется:</p>
  <ul>
    <li>после успешной оплаты зачислить оплаченный пакет генераций на баланс Покупателя в Сервисе CardBot;</li>
    <li>предоставить Покупателю информацию о составе и стоимости пакета до оплаты;</li>
    <li>принимать обращения по вопросам оплаты, зачисления баланса и работы Сервиса по адресу <a href="mailto:alterega@list.ru">alterega@list.ru</a>;</li>
    <li>принимать разумные меры для сохранности данных, необходимых для учета платежей, баланса и истории генераций.</li>
  </ul>
  <p>3.3. Покупатель вправе:</p>
  <ul>
    <li>использовать оплаченный баланс для генерации материалов в пределах функциональности Сервиса CardBot;</li>
    <li>получать информацию о доступном балансе и истории генераций в Telegram-боте;</li>
    <li>обращаться к Продавцу при ошибке оплаты, незачислении баланса или ином техническом сбое.</li>
  </ul>
  <p>3.4. Покупатель обязуется:</p>
  <ul>
    <li>предоставлять корректные сведения о товаре, необходимые для генерации карточек и изображений;</li>
    <li>самостоятельно проверять итоговые тексты, характеристики, изображения, ключевые слова и хэштеги перед публикацией на маркетплейсах;</li>
    <li>не использовать Сервис для создания материалов, нарушающих законодательство Российской Федерации, права третьих лиц, правила Telegram, Wildberries, Ozon или иных площадок;</li>
    <li>не передавать платежные ссылки, доступ к своему Telegram-аккаунту и иные данные третьим лицам, если это может привести к спору по оплате или балансу.</li>
  </ul>

  <h2>4. Цена и порядок расчетов</h2>
  <p>4.1. Стоимость пакетов генераций определяется сведениями, отображаемыми в Telegram-боте CardBot на момент оформления заказа Покупателем.</p>
  <p>4.2. Все расчеты по Договору производятся в безналичном порядке через платежный сервис Robokassa. Платежная ссылка формируется автоматически после выбора Покупателем пакета генераций.</p>
  <p>4.3. Оплата считается совершенной после подтверждения успешного платежа платежным сервисом Robokassa и получения Сервисом CardBot технического уведомления об оплате.</p>
  <p>4.4. Продавец вправе изменять стоимость пакетов и состав тарифов. Изменения не распространяются на пакеты, оплаченные Покупателем до момента изменения стоимости.</p>

  <h2>5. Порядок оказания цифровой услуги и возвраты</h2>
  <p>5.1. После успешной оплаты выбранный пакет генераций автоматически зачисляется на баланс Покупателя в Telegram-боте CardBot. Идентификация Покупателя производится по Telegram ID.</p>
  <p>5.2. Цифровая услуга считается оказанной в части предоставления доступа к оплаченному пакету с момента зачисления соответствующего количества генераций на баланс Покупателя.</p>
  <p>5.3. Если после успешной оплаты баланс не был зачислен автоматически, Покупатель может обратиться по адресу <a href="mailto:alterega@list.ru">alterega@list.ru</a>. В обращении необходимо указать Telegram ID, дату платежа, сумму платежа и доступные данные платежа.</p>
  <p>5.4. Возвраты, ошибочные платежи и спорные ситуации рассматриваются индивидуально в соответствии с законодательством Российской Федерации, фактическим статусом оплаты, объемом использованного баланса и техническими данными Сервиса.</p>
  <p>5.5. Сгенерированные Сервисом материалы создаются автоматически с использованием AI-моделей. Покупатель понимает, что результат генерации может требовать проверки, редактирования и адаптации под правила конкретного маркетплейса.</p>

  <h2>6. Конфиденциальность и безопасность</h2>
  <p>6.1. При исполнении настоящего Договора Продавец обрабатывает данные, необходимые для работы Сервиса CardBot: Telegram ID, имя пользователя Telegram при наличии, язык интерфейса, историю запросов и генераций, сведения о платежах, пакетах и балансе.</p>
  <p>6.2. Указанные данные используются для оказания цифровой услуги, учета платежей, зачисления баланса, отображения истории, поддержки Покупателя и предотвращения злоупотреблений.</p>
  <p>6.3. Продавец принимает разумные организационные и технические меры для защиты данных, необходимых для работы Сервиса. При этом Покупатель понимает, что передача данных через Telegram, платежные сервисы и AI-провайдеров регулируется также правилами соответствующих третьих лиц.</p>
  <p>6.4. Покупатель не должен направлять в Сервис сведения, которые не нужны для генерации карточки товара или изображения, включая избыточные персональные данные, коммерческие тайны и иную конфиденциальную информацию.</p>

  <h2>7. Форс-мажор</h2>
  <p>7.1. Стороны освобождаются от ответственности за неисполнение или ненадлежащее исполнение обязательств по Договору, если надлежащее исполнение оказалось невозможным вследствие обстоятельств непреодолимой силы.</p>
  <p>7.2. К таким обстоятельствам относятся, в том числе, запретные действия властей, сбои инфраструктуры связи, ограничения работы Telegram, платежных сервисов, банков, AI-провайдеров, дата-центров, эпидемии, блокада, эмбарго, пожары, наводнения, землетрясения и иные чрезвычайные и непредотвратимые обстоятельства.</p>
  <p>7.3. Сторона, для которой создалась невозможность исполнения обязательств, обязана уведомить другую Сторону о наступлении таких обстоятельств в разумный срок доступным способом связи.</p>
  <p>7.4. Если обстоятельства непреодолимой силы продолжают действовать более 60 (Шестидесяти) рабочих дней, каждая Сторона вправе отказаться от исполнения Договора в одностороннем порядке.</p>

  <h2>8. Ответственность Сторон</h2>
  <p>8.1. В случае неисполнения или ненадлежащего исполнения обязательств по Договору Стороны несут ответственность в соответствии с условиями настоящей Оферты и законодательством Российской Федерации.</p>
  <p>8.2. Продавец не гарантирует, что сгенерированные материалы будут приняты маркетплейсами Wildberries, Ozon или иными площадками без редактирования, а также не гарантирует конкретные коммерческие показатели карточек товаров.</p>
  <p>8.3. Продавец не несет ответственность за решения маркетплейсов, модерацию карточек, блокировки, изменение правил площадок, ошибки Покупателя при публикации материалов, а также за последствия использования Покупателем сгенерированных текстов и изображений без проверки.</p>
  <p>8.4. Продавец не несет ответственность за временную недоступность Сервиса, вызванную сбоями Telegram, Robokassa, банков, AI-провайдеров, хостинга, сетей связи или иных третьих лиц, если такие обстоятельства находятся вне разумного контроля Продавца.</p>
  <p>8.5. Покупатель несет ответственность за достоверность предоставленных сведений о товаре, правомерность загружаемых изображений и материалов, а также за соответствие итоговой публикации требованиям законодательства и правилам маркетплейсов.</p>

  <h2>9. Срок действия настоящей Оферты</h2>
  <p>9.1. Оферта вступает в силу с момента размещения по адресу <a href="https://alterega.ru/cardbot/offer">alterega.ru/cardbot/offer</a> и действует до момента ее отзыва Продавцом.</p>
  <p>9.2. Продавец оставляет за собой право внести изменения в условия Оферты или отозвать Оферту в любой момент по своему усмотрению. Актуальная редакция публикуется по адресу <a href="https://alterega.ru/cardbot/offer">alterega.ru/cardbot/offer</a>.</p>
  <p>9.3. Договор вступает в силу с момента Акцепта условий настоящей Оферты Покупателем и действует до полного исполнения Сторонами обязательств по Договору.</p>
  <p>9.4. Изменения, опубликованные в форме актуализированной Оферты, применяются к отношениям Сторон с момента публикации, если иное прямо не указано в новой редакции Оферты.</p>

  <h2>10. Дополнительные условия</h2>
  <p>10.1. Договор, его заключение и исполнение регулируются действующим законодательством Российской Федерации. Все вопросы, не урегулированные настоящей Офертой или урегулированные не полностью, регулируются в соответствии с законодательством Российской Федерации.</p>
  <p>10.2. В случае возникновения спора Стороны обязуются принять меры к его урегулированию путем переговоров и направления обращения на контактный e-mail Продавца. Досудебный порядок урегулирования спора является обязательным.</p>
  <p>10.3. В качестве языка Договора и языка взаимодействия Сторон определяется русский язык.</p>
  <p>10.4. Бездействие одной из Сторон в случае нарушения условий настоящей Оферты не лишает заинтересованную Сторону права осуществлять защиту своих интересов позднее и не означает отказ от прав.</p>
  <p>10.5. Если в Сервисе CardBot или на связанных страницах есть ссылки на сайты и материалы третьих лиц, такие ссылки размещаются в информационных целях. Продавец не контролирует содержание таких сайтов и материалов и не несет ответственность за последствия их использования.</p>
  <p>10.6. Недействительность отдельного положения настоящей Оферты не влечет недействительность остальных положений Оферты и Договора в целом.</p>

  <h2>Реквизиты Продавца</h2>
  <div class="requisites">
    <p>Полное наименование: —</p>
    <p>ИНН: 615422982815</p>
    <p>ОГРН/ОГРНИП: —</p>
    <p>Контактный телефон: +244 931 150 124</p>
    <p>Контактный e-mail: <a href="mailto:alterega@list.ru">alterega@list.ru</a></p>
  </div>
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


def _parse_int_or_none(value: str) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


async def _log_payment_event(
    db: Any,
    *,
    inv_id: str,
    user_id: str,
    status: str,
    payload: dict[str, Any],
    error_reason: str | None = None,
) -> None:
    await db.log_payment_event(
        inv_id=inv_id or None,
        user_id=_parse_int_or_none(user_id),
        event_type="robokassa_result",
        status=status,
        payload=payload,
        error_reason=error_reason,
    )


async def handle_robokassa_result(request: Any) -> web.Response:
    data = await request.post()
    payload = {str(key): str(value) for key, value in data.items()}

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
    db = request.app["db"]
    if signature.upper() != expected:
        logger.warning("Invalid Robokassa signature for InvId=%s", inv_id)
        await _log_payment_event(
            db,
            inv_id=inv_id,
            user_id=user_id,
            status="invalid_signature",
            payload=payload,
            error_reason="invalid_signature",
        )
        return web.Response(text="Invalid signature", status=400)

    payment = await db.get_payment_by_inv_id(inv_id)
    if not payment:
        logger.warning("Robokassa payment not found: InvId=%s", inv_id)
        await _log_payment_event(
            db,
            inv_id=inv_id,
            user_id=user_id,
            status="payment_not_found",
            payload=payload,
            error_reason="payment_not_found",
        )
        return web.Response(text=f"OK{inv_id}")

    if payment["status"] == "paid":
        await _log_payment_event(
            db,
            inv_id=inv_id,
            user_id=user_id,
            status="already_paid",
            payload=payload,
        )
        return web.Response(text=f"OK{inv_id}")

    if payment["package_code"] != package_code or str(payment["user_id"]) != user_id:
        logger.warning("Robokassa Shp mismatch for InvId=%s", inv_id)
        await _log_payment_event(
            db,
            inv_id=inv_id,
            user_id=user_id,
            status="payment_mismatch",
            payload=payload,
            error_reason="payment_mismatch",
        )
        return web.Response(text="Payment mismatch", status=400)

    if package_code not in PACKAGES:
        logger.error("Unknown CardBot payment package: %s", package_code)
        await _log_payment_event(
            db,
            inv_id=inv_id,
            user_id=user_id,
            status="unknown_package",
            payload=payload,
            error_reason="unknown_package",
        )
        return web.Response(text="Unknown package", status=400)

    if not _same_amount(out_sum, int(payment["amount_rub"])):
        logger.warning("Robokassa amount mismatch for InvId=%s", inv_id)
        await _log_payment_event(
            db,
            inv_id=inv_id,
            user_id=user_id,
            status="amount_mismatch",
            payload=payload,
            error_reason="amount_mismatch",
        )
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
    await _log_payment_event(
        db,
        inv_id=inv_id,
        user_id=user_id,
        status="paid" if paid_now else "already_paid",
        payload=payload,
    )

    return web.Response(text=f"OK{inv_id}")


async def _notify_user_about_payment(bot: Any, db: Any, user_id: int, payment: dict[str, Any]) -> None:
    user = await db.get_user(user_id)
    if not user:
        return
    try:
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
    except Exception as exc:
        try:
            from telegram.error import Forbidden, TelegramError
        except ImportError:  # pragma: no cover
            Forbidden = TelegramError = ()
        if Forbidden and isinstance(exc, Forbidden):
            await db.mark_user_blocked(user_id)
            logger.info("CardBot payment notification blocked by user=%s", user_id)
            return
        if TelegramError and isinstance(exc, TelegramError):
            logger.warning("CardBot payment notification failed for user=%s: %s", user_id, exc)
            return
        raise


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
