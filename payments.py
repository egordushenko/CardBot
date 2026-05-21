from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from urllib.parse import urlencode

from config import Settings


ROBOKASSA_PAY_URL = "https://auth.robokassa.ru/Merchant/Index.aspx"


@dataclass(frozen=True)
class PaymentPackage:
    code: str
    title: str
    text_count: int
    images_per_card: int
    price_rub: int

    @property
    def images_count(self) -> int:
        if self.code.startswith("text_"):
            return self.text_count * self.images_per_card
        return self.images_per_card

    @property
    def description(self) -> str:
        if self.text_count and self.images_per_card:
            return f"{self.text_count} карточек + {self.images_count} изображений"
        if self.text_count:
            return f"{self.text_count} карточек"
        return f"{self.images_count} изображений"


PACKAGES: dict[str, PaymentPackage] = {
    "text_start_x0": PaymentPackage("text_start_x0", "Старт, без фото", 10, 0, 490),
    "text_start_x3": PaymentPackage("text_start_x3", "Старт × 3 фото", 10, 3, 1990),
    "text_start_x5": PaymentPackage("text_start_x5", "Старт × 5 фото", 10, 5, 2990),
    "text_start_x7": PaymentPackage("text_start_x7", "Старт × 7 фото", 10, 7, 3990),
    "text_business_x0": PaymentPackage("text_business_x0", "Бизнес, без фото", 30, 0, 1190),
    "text_business_x3": PaymentPackage("text_business_x3", "Бизнес × 3 фото", 30, 3, 5240),
    "text_business_x5": PaymentPackage("text_business_x5", "Бизнес × 5 фото", 30, 5, 7940),
    "text_business_x7": PaymentPackage("text_business_x7", "Бизнес × 7 фото", 30, 7, 10640),
    "text_pro_x0": PaymentPackage("text_pro_x0", "Про, без фото", 100, 0, 2990),
    "text_pro_x3": PaymentPackage("text_pro_x3", "Про × 3 фото", 100, 3, 14990),
    "text_pro_x5": PaymentPackage("text_pro_x5", "Про × 5 фото", 100, 5, 22990),
    "text_pro_x7": PaymentPackage("text_pro_x7", "Про × 7 фото", 100, 7, 30990),
    "addon_text_10": PaymentPackage("addon_text_10", "Докупить 10 карточек", 10, 0, 560),
    "addon_text_30": PaymentPackage("addon_text_30", "Докупить 30 карточек", 30, 0, 1370),
    "addon_text_100": PaymentPackage("addon_text_100", "Докупить 100 карточек", 100, 0, 3440),
    "addon_img_20": PaymentPackage("addon_img_20", "Докупить 20 изображений", 0, 20, 1150),
    "addon_img_50": PaymentPackage("addon_img_50", "Докупить 50 изображений", 0, 50, 2750),
    "addon_img_150": PaymentPackage("addon_img_150", "Докупить 150 изображений", 0, 150, 7500),
    "promo_img_10": PaymentPackage("promo_img_10", "Акция: 10 изображений", 0, 10, 575),
}

MAIN_PACKAGE_CODES = [
    "text_start_x0",
    "text_start_x3",
    "text_start_x5",
    "text_start_x7",
    "text_business_x0",
    "text_business_x3",
    "text_business_x5",
    "text_business_x7",
    "text_pro_x0",
    "text_pro_x3",
    "text_pro_x5",
    "text_pro_x7",
]
TEXT_ADDON_CODES = ["addon_text_10", "addon_text_30", "addon_text_100"]
IMAGE_ADDON_CODES = ["addon_img_20", "addon_img_50", "addon_img_150"]
PROMO_PACKAGE_CODE = "promo_img_10"


def generate_inv_id() -> str:
    return uuid.uuid4().hex


def format_out_sum(amount_rub: int) -> str:
    return f"{amount_rub:.2f}"


def calculate_package_counts(package_code: str) -> tuple[int, int]:
    package = PACKAGES[package_code]
    return package.text_count, package.images_count


def _sorted_shp_parts(shp_params: dict[str, str | int]) -> list[str]:
    return [
        f"{key}={shp_params[key]}"
        for key in sorted(shp_params, key=lambda value: value.lower())
    ]


def _md5_upper(value: str) -> str:
    return hashlib.md5(value.encode("utf-8")).hexdigest().upper()


def robokassa_payment_signature(
    *,
    merchant_login: str,
    out_sum: str,
    inv_id: str,
    password1: str,
    shp_params: dict[str, str | int],
) -> str:
    parts = [merchant_login, out_sum, inv_id, password1]
    parts.extend(_sorted_shp_parts(shp_params))
    return _md5_upper(":".join(parts))


def robokassa_result_signature(
    *,
    out_sum: str,
    inv_id: str,
    password2: str,
    shp_params: dict[str, str | int],
) -> str:
    parts = [out_sum, inv_id, password2]
    parts.extend(_sorted_shp_parts(shp_params))
    return _md5_upper(":".join(parts))


def build_payment_url(
    *,
    settings: Settings,
    inv_id: str,
    user_id: int,
    package_code: str,
) -> str:
    if not settings.robokassa_login:
        raise RuntimeError("ROBOKASSA_LOGIN is not configured")
    if not settings.robokassa_password1:
        raise RuntimeError("ROBOKASSA_PASSWORD1 is not configured")

    package = PACKAGES[package_code]
    out_sum = format_out_sum(package.price_rub)
    shp_params = {
        "Shp_package": package_code,
        "Shp_user_id": str(user_id),
    }
    signature = robokassa_payment_signature(
        merchant_login=settings.robokassa_login,
        out_sum=out_sum,
        inv_id=inv_id,
        password1=settings.robokassa_password1,
        shp_params=shp_params,
    )
    params: dict[str, str] = {
        "MerchantLogin": settings.robokassa_login,
        "OutSum": out_sum,
        "InvId": inv_id,
        "Description": f"CardBot: {package.title}",
        "Encoding": "utf-8",
        "Culture": "ru",
        "Shp_user_id": str(user_id),
        "Shp_package": package_code,
        "SuccessURL": settings.cardbot_bot_url,
        "FailURL": settings.cardbot_bot_url,
        "SignatureValue": signature,
    }
    if settings.robokassa_test_mode:
        params["IsTest"] = "1"
    return f"{ROBOKASSA_PAY_URL}?{urlencode(params)}"
