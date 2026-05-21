from config import Settings
from payments import (
    PACKAGES,
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
    assert PACKAGES["promo_img_10"].price_rub == 575


def test_calculate_package_counts_handles_main_and_addon_packages():
    assert calculate_package_counts("text_start_x7") == (10, 70)
    assert calculate_package_counts("addon_text_30") == (30, 0)
    assert calculate_package_counts("addon_img_50") == (0, 50)


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
        inv_id="abc123",
        user_id=598380407,
        package_code="text_start_x0",
    )

    assert url.startswith("https://auth.robokassa.ru/Merchant/Index.aspx?")
    assert "MerchantLogin=CardBot" in url
    assert "OutSum=490.00" in url
    assert "InvId=abc123" in url
    assert "Shp_user_id=598380407" in url
    assert "Shp_package=text_start_x0" in url
    assert "SuccessURL=https%3A%2F%2Ft.me%2FCaardMakerBot" in url
    assert "FailURL=https%3A%2F%2Ft.me%2FCaardMakerBot" in url
    assert "IsTest=1" in url


def test_generate_inv_id_is_uuid_without_dashes():
    inv_id = generate_inv_id()

    assert len(inv_id) == 32
    assert "-" not in inv_id


def test_format_out_sum_uses_two_decimal_places():
    assert format_out_sum(490) == "490.00"
