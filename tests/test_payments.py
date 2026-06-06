from urllib.parse import parse_qs, urlparse

from config import Settings
from payments import (
    PACKAGES,
    FIRST_PURCHASE_PACKAGE_CODES,
    PROMO_PACKAGE_CODES,
    REGULAR_PACKAGE_CODES,
    build_receipt,
    build_payment_url,
    calculate_package_counts,
    format_out_sum,
    generate_inv_id,
    robokassa_payment_signature,
    robokassa_result_signature,
)


def test_cardbot_packages_match_price_spec():
    assert PACKAGES["text_business_x5"].text_count == 30
    assert PACKAGES["text_business_x5"].images_per_card == 5
    assert PACKAGES["text_business_x5"].images_count == 150
    assert PACKAGES["text_business_x5"].price_rub == 7940
    assert PACKAGES["text_pro_x7"].images_count == 700
    assert PACKAGES["text_pro_x7"].price_rub == 30990
    assert PACKAGES["addon_img_50"].price_rub == 2750
    assert PACKAGES["addon_img_150"].price_rub == 7500
    assert PACKAGES["promo_img_10"].images_count == 10
    assert PACKAGES["promo_img_10"].price_rub == 290
    assert PACKAGES["promo_text_start_x3"].text_count == 10
    assert PACKAGES["promo_text_start_x3"].images_per_card == 3
    assert PACKAGES["promo_text_start_x3"].images_count == 30
    assert PACKAGES["promo_text_start_x3"].price_rub == 1240
    assert PACKAGES["promo_text_start_x5"].images_count == 50
    assert PACKAGES["promo_text_start_x5"].price_rub == 1740
    assert set(PROMO_PACKAGE_CODES).issuperset(
        {"promo_img_10", "promo_text_start_x3", "promo_text_start_x5"}
    )


def test_first_purchase_discount_exists_for_every_regular_package():
    assert "first_text_pro_x7" in PACKAGES
    assert PACKAGES["first_text_pro_x7"].text_count == PACKAGES["text_pro_x7"].text_count
    assert PACKAGES["first_text_pro_x7"].images_count == PACKAGES["text_pro_x7"].images_count
    assert PACKAGES["first_text_pro_x7"].price_rub == 15495
    assert "first_addon_img_150" in PACKAGES
    assert PACKAGES["first_addon_img_150"].images_count == 150
    assert PACKAGES["first_addon_img_150"].price_rub == 3750
    assert set(FIRST_PURCHASE_PACKAGE_CODES) == {f"first_{code}" for code in REGULAR_PACKAGE_CODES}
    assert set(FIRST_PURCHASE_PACKAGE_CODES).issubset(PROMO_PACKAGE_CODES)


def test_calculate_package_counts_handles_main_and_addon_packages():
    assert calculate_package_counts("text_start_x7") == (10, 70)
    assert calculate_package_counts("first_text_pro_x7") == (100, 700)
    assert calculate_package_counts("addon_text_30") == (30, 0)
    assert calculate_package_counts("first_addon_img_150") == (0, 150)


def test_robokassa_signatures_sort_shp_case_insensitive():
    shp = {"Shp_user_id": "598380407", "Shp_package": "text_start_x0"}

    assert (
        robokassa_payment_signature(
            merchant_login="CardBot",
            out_sum="490.00",
            inv_id="abc123",
            password1="pass1",
            shp_params=shp,
        )
        == "20B8D280615F3F94DDF581AE04214732"
    )
    assert (
        robokassa_result_signature(
            out_sum="490.00",
            inv_id="abc123",
            password2="pass2",
            shp_params=shp,
        )
        == "B5737D9CC85921036B7BF4D61E205414"
    )


def test_build_payment_url_contains_required_robokassa_fields():
    settings = Settings(
        bot_token="telegram-token",
        openrouter_api_key="openrouter-key",
        cardbot_db_url="postgresql://user:pass@127.0.0.1:5432/cardbot",
        robokassa_login="CardBot",
        robokassa_password1="pass1",
        robokassa_password2="pass2",
        robokassa_test_mode=True,
        cardbot_bot_url="https://t.me/CaardMakerBot",
    )

    url = build_payment_url(
        settings=settings,
        inv_id="1779390000000123456",
        user_id=598380407,
        package_code="text_start_x0",
    )

    assert url.startswith("https://auth.robokassa.ru/Merchant/Index.aspx?")
    assert "MerchantLogin=CardBot" in url
    assert "OutSum=490.000000" in url
    assert "InvId=1779390000000123456" in url
    assert "Shp_user_id=598380407" in url
    assert "Shp_package=text_start_x0" in url
    assert "SuccessURL=https%3A%2F%2Ft.me%2FCaardMakerBot" in url
    assert "FailURL=https%3A%2F%2Ft.me%2FCaardMakerBot" in url
    assert "Receipt=%257B%2522sno%2522%253A%2522usn_income%2522" in url
    assert "IsTest=1" in url


def test_build_payment_url_signature_uses_encoded_receipt_before_password():
    settings = Settings(
        bot_token="telegram-token",
        openrouter_api_key="openrouter-key",
        cardbot_db_url="postgresql://user:pass@127.0.0.1:5432/cardbot",
        robokassa_login="CardBot",
        robokassa_password1="pass1",
        robokassa_password2="pass2",
        cardbot_bot_url="https://t.me/CaardMakerBot",
    )

    url = build_payment_url(
        settings=settings,
        inv_id="1779390000000123456",
        user_id=598380407,
        package_code="text_business_x3",
    )
    params = parse_qs(urlparse(url).query)
    receipt_for_sign = params["Receipt"][0]

    expected_signature = robokassa_payment_signature(
        merchant_login="CardBot",
        out_sum=params["OutSum"][0],
        inv_id=params["InvId"][0],
        password1="pass1",
        shp_params={
            "Shp_package": params["Shp_package"][0],
            "Shp_user_id": params["Shp_user_id"][0],
        },
        receipt_for_sign=receipt_for_sign,
    )

    assert params["SignatureValue"][0] == expected_signature


def test_generate_inv_id_is_numeric_robokassa_invoice_id():
    inv_id = generate_inv_id()

    assert inv_id.isdigit()
    assert 1 <= int(inv_id) <= 9_223_372_036_854_775_807


def test_build_payment_url_rejects_non_numeric_inv_id():
    settings = Settings(
        bot_token="telegram-token",
        openrouter_api_key="openrouter-key",
        cardbot_db_url="postgresql://user:pass@127.0.0.1:5432/cardbot",
        robokassa_login="CardBot",
        robokassa_password1="pass1",
    )

    try:
        build_payment_url(
            settings=settings,
            inv_id="81c33b1a548a452a9efd02836f257685",
            user_id=598380407,
            package_code="text_start_x0",
        )
    except ValueError as exc:
        assert "InvId" in str(exc)
    else:
        raise AssertionError("Expected non-numeric Robokassa InvId to be rejected")


def test_format_out_sum_uses_six_decimal_places_for_robokassa():
    assert format_out_sum(490) == "490.000000"


def test_build_receipt_returns_double_encoded_receipt_for_url():
    settings = Settings(
        bot_token="telegram-token",
        openrouter_api_key="openrouter-key",
        cardbot_db_url="postgresql://user:pass@127.0.0.1:5432/cardbot",
    )

    receipt_for_sign, receipt_for_url = build_receipt(
        settings=settings,
        package=PACKAGES["text_start_x0"],
        out_sum="490.000000",
    )

    assert receipt_for_sign.startswith("%7B%22sno%22%3A%22usn_income%22")
    assert receipt_for_url.startswith("%257B%2522sno%2522%253A%2522usn_income%2522")
