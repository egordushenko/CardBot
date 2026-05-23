from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from llm import ImageConcept


PHOTO_TAGS = {
    "front",
    "back",
    "closeup",
    "label",
    "on_model",
    "flatlay",
}

QA_ISSUES = {
    "pure_white_background",
    "small_text",
    "bad_typography",
    "random_corner_text",
    "forbidden_clothing_size",
    "deformation",
    "print_mismatch",
    "wrong_product_color",
    "raw_unprocessed_photo",
}


@dataclass(frozen=True)
class PhotoAnalysis:
    photo_index: int
    tags: tuple[str, ...] = ()
    visible_text: tuple[str, ...] = ()
    defects: tuple[str, ...] = ()
    usable_for: tuple[str, ...] = ()
    summary: str = ""


@dataclass(frozen=True)
class SlidePlan:
    image_index: int
    role: str
    source_photo_index: int
    composition: str
    background: str
    overlay_text: tuple[str, ...] = ()
    negative_constraints: tuple[str, ...] = ()
    qa_checks: tuple[str, ...] = ()


@dataclass(frozen=True)
class ImageQualityReport:
    passed: bool
    issues: tuple[str, ...] = ()
    summary: str = ""


def _strip_markdown_fence(payload: str) -> str:
    text = payload.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def _as_clean_tuple(value: Any, *, allowed: set[str] | None = None, limit: int = 8) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    result: list[str] = []
    for item in value:
        text = str(item).strip()
        if not text:
            continue
        normalized = text.casefold()
        if allowed is not None:
            if normalized not in allowed:
                continue
            text = normalized
        if text not in result:
            result.append(text)
        if len(result) >= limit:
            break
    return tuple(result)


def parse_photo_analysis_payload(payload: str, photos_count: int) -> list[PhotoAnalysis]:
    data = json.loads(_strip_markdown_fence(payload))
    raw_items = data.get("photos")
    if raw_items is None and isinstance(data.get("photo"), dict):
        raw_items = [data["photo"]]
    if not isinstance(raw_items, list):
        return []

    result: list[PhotoAnalysis] = []
    max_index = max(photos_count - 1, 0)
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        try:
            photo_index = int(item.get("photo_index", 0))
        except (TypeError, ValueError):
            photo_index = 0
        photo_index = min(max(photo_index, 0), max_index)
        result.append(
            PhotoAnalysis(
                photo_index=photo_index,
                tags=_as_clean_tuple(item.get("tags"), allowed=PHOTO_TAGS),
                visible_text=_as_clean_tuple(item.get("visible_text"), limit=12),
                defects=_as_clean_tuple(item.get("defects"), limit=8),
                usable_for=_as_clean_tuple(item.get("usable_for"), limit=10),
                summary=str(item.get("summary") or "").strip(),
            )
        )
    return result


def parse_image_quality_payload(payload: str) -> ImageQualityReport:
    data = json.loads(_strip_markdown_fence(payload))
    issues = _as_clean_tuple(data.get("issues"), allowed=QA_ISSUES, limit=8)
    passed = bool(data.get("passed")) and not issues
    return ImageQualityReport(
        passed=passed,
        issues=issues,
        summary=str(data.get("summary") or "").strip(),
    )


def detect_visual_profile(product_description: str, marketplace: str = "wb") -> str:
    text = product_description.casefold()
    if any(keyword in text for keyword in ("ламп", "светильник", "lamp")):
        return "home_decor"
    if any(keyword in text for keyword in ("рюкзак", "сумк", "кошелек", "чемодан", "backpack", "bag")):
        return "bags"
    profiles: list[tuple[str, tuple[str, ...]]] = [
        ("kids", ("детск", "ребен", "ребён", "малыш", "baby", "kids", "child", "подгуз")),
        ("clothing", ("рашгард", "футбол", "плать", "худи", "куртк", "брюк", "одежд", "shirt", "jacket", "dress", "rashguard", "hoodie")),
        ("electronics", ("наушник", "смартфон", "bluetooth", "usb", "power bank", "заряд", "колонк", "электрон", "headphones")),
        ("cosmetics", ("крем", "сыворот", "шампун", "маска", "лосьон", "cosmetic", "serum", "cream")),
        ("bags", ("рюкзак", "сумк", "кошелек", "чемодан", "backpack", "bag")),
        ("food", ("батончик", "кофе", "чай", "шоколад", "протеин", "еда", "food", "protein bar")),
        ("sports", ("спорт", "fitness", "workout", "yoga", "гантел", "коврик для йоги", "трениров")),
        ("home_decor", ("песочн", "час", "декор", "коврик", "органайзер", "лампа", "посуда", "home", "hourglass")),
    ]
    for profile, keywords in profiles:
        if any(keyword in text for keyword in keywords):
            return profile
    return "home_decor"


def fallback_photo_analysis(photo_index: int, product_description: str = "", photos_count: int = 1) -> PhotoAnalysis:
    profile = detect_visual_profile(product_description)
    tags: tuple[str, ...]
    usable_for: tuple[str, ...]
    if profile == "clothing":
        presets = [
            (("back", "on_model"), ("back_on_model", "print_reference")),
            (("closeup", "label"), ("closeup", "label_reference")),
            (("front", "on_model"), ("front_on_model",)),
            (("flatlay", "front"), ("hero", "flatlay")),
            (("back", "flatlay"), ("back_flatlay", "print_reference")),
        ]
        tags, usable_for = presets[photo_index % len(presets)]
    else:
        presets = [
            (("flatlay",), ("hero",)),
            (("closeup",), ("closeup",)),
            (("front",), ("facts",)),
            (("closeup",), ("detail",)),
        ]
        tags, usable_for = presets[photo_index % len(presets)]
    return PhotoAnalysis(photo_index=photo_index, tags=tags, usable_for=usable_for)


def _analysis_by_index(photo_analyses: list[PhotoAnalysis] | None, photos_count: int) -> list[PhotoAnalysis]:
    if photo_analyses:
        by_index = {item.photo_index: item for item in photo_analyses}
        return [by_index.get(index) or fallback_photo_analysis(index, photos_count=photos_count) for index in range(photos_count)]
    return [fallback_photo_analysis(index, photos_count=photos_count) for index in range(max(photos_count, 1))]


def _choose_photo_index(analyses: list[PhotoAnalysis], role: str) -> int:
    preferred: dict[str, tuple[str, ...]] = {
        "hero": ("hero", "flatlay", "front_on_model"),
        "facts": ("facts", "hero", "front_on_model"),
        "closeup": ("closeup", "label_reference", "print_reference", "detail"),
        "lifestyle_back": ("back_on_model", "back_flatlay", "print_reference"),
        "lifestyle_front": ("front_on_model", "hero", "flatlay"),
        "lifestyle_three_quarter": ("front_on_model", "back_on_model", "hero"),
        "interior": ("hero", "detail"),
        "scenario": ("hero", "front_on_model"),
    }
    needles = preferred.get(role, ("hero",))
    for needle in needles:
        for analysis in analyses:
            if needle in analysis.usable_for:
                return analysis.photo_index
    for analysis in analyses:
        if role == "closeup" and "closeup" in analysis.tags:
            return analysis.photo_index
        if role == "lifestyle_back" and "back" in analysis.tags:
            return analysis.photo_index
        if role == "lifestyle_front" and "front" in analysis.tags:
            return analysis.photo_index
    return analyses[0].photo_index if analyses else 0


def _common_negative_constraints(profile: str) -> tuple[str, ...]:
    constraints = [
        "Do NOT use a pure white empty background; use contextual light studio or interior background.",
        "Use large readable modern sans-serif typography only.",
        "Use 1-2 text blocks, not random corner labels.",
        "Do NOT use meaningless headings or generic detail labels.",
        "Preserve exact product shape, color, texture and proportions.",
        "Use only the selected reference photo; do not mix details from other photos.",
    ]
    if profile in {"clothing", "kids"}:
        constraints.extend(
            [
                "Do NOT put clothing size on overlay text.",
                "Preserve printed logos and text exactly; do not invent or move print elements.",
                "Do NOT change clothing color, fit, print, sleeve length, collar or silhouette.",
                "Remove home-photo defects, wrinkles, bad lighting and messy background without changing the product.",
            ]
        )
    if profile == "kids":
        constraints.append("Do NOT use adult models for children's clothing.")
    return tuple(constraints)


def _sanitize_product_description_for_prompt(product_description: str, profile: str) -> str:
    description = product_description.strip()
    if profile not in {"clothing", "kids"}:
        return description
    patterns = [
        r"\bsize\s*[:=]?\s*[a-z0-9]{1,4}\b",
        r"\bразмер\s*[:=]?\s*[a-zа-я0-9]{1,6}\b",
        r"\bр-р\s*[:=]?\s*[a-zа-я0-9]{1,6}\b",
    ]
    result = description
    for pattern in patterns:
        result = re.sub(pattern, "", result, flags=re.IGNORECASE)
    result = re.sub(r"\s{2,}", " ", result)
    result = re.sub(r"\s+,", ",", result)
    return result.strip(" ,.;") or description


def _overlay(*items: str) -> tuple[str, ...]:
    return tuple(item for item in items if item)


def _has_explicit_no_print(product_description: str) -> bool:
    text = product_description.casefold()
    return any(
        marker in text
        for marker in (
            "без принт",
            "без логотип",
            "без надпис",
            "без рисун",
            "однотон",
            "no print",
            "without print",
            "no logo",
            "without logo",
            "plain",
        )
    )


def _has_explicit_print(product_description: str) -> bool:
    if _has_explicit_no_print(product_description):
        return False
    text = product_description.casefold()
    return any(marker in text for marker in ("принт", "печать", "надпис", "логотип", "print", "logo"))


def _overlay_instruction_like(text: str) -> bool:
    normalized = text.casefold().strip()
    forbidden_fragments = (
        "товарный вид",
        "без лишнего фона",
        "разъемы крупно",
        "разъёмы крупно",
        "детали",
        "главное фото",
        "product view",
        "no extra background",
        "closeup",
        "close-up",
    )
    return any(fragment in normalized for fragment in forbidden_fragments)


def _extract_overlay_facts(product_description: str) -> tuple[str, ...]:
    text = product_description.casefold()
    result: list[str] = []

    def add(value: str) -> None:
        if value and value not in result:
            result.append(value)

    for match in re.finditer(r"(?:до\s*)?(\d{1,2})\s*(?:час(?:ов|а)?|hours?|h\b)", text, flags=re.IGNORECASE):
        add(f"{match.group(1)} часов")
    for match in re.finditer(r"(\d{1,2})\s*(?:light\s*)?(?:режим(?:а|ов)?|modes?)", text, flags=re.IGNORECASE):
        add(f"{match.group(1)} режима")
    for match in re.finditer(r"(\d{1,4})\s*(?:w|вт|ватт)", text, flags=re.IGNORECASE):
        add(f"{match.group(1)} Вт")
    if "bluetooth" in text or "блютуз" in text:
        add("Bluetooth")
    if "шумоподав" in text or "noise cancellation" in text:
        add("Шумоподавление")
    if "usb" in text:
        add("USB подключение")
    return tuple(result[:4])


def _extract_clothing_overlay_facts(product_description: str) -> tuple[str, ...]:
    text = product_description.casefold()
    result: list[str] = []

    def add(value: str) -> None:
        if value and value not in result:
            result.append(value)

    cotton_match = re.search(r"100\s*%\s*(?:хлопок|cotton)", text, flags=re.IGNORECASE)
    if cotton_match:
        add("100% ХЛОПОК")
    elif "хлопок" in text or "cotton" in text:
        add("Хлопок в составе")

    if _has_explicit_print(product_description):
        if "спин" in text or "back" in text:
            add("Принт на спине")
        else:
            add("Принт на ткани")
    if "дышащ" in text or "breathable" in text:
        add("Дышащая ткань")
    if "облега" in text or "fitted" in text:
        add("Облегающий крой")
    if "свобод" in text or "oversize" in text:
        add("Свободная посадка")

    return tuple(result[:3])


def _overlay_for_slide(profile: str, role: str, product_description: str, raw_overlay: tuple[str, ...]) -> tuple[str, ...]:
    cleaned: list[str] = []
    no_print = _has_explicit_no_print(product_description)
    has_print = _has_explicit_print(product_description)

    for item in raw_overlay:
        text = str(item).strip()
        if not text or _overlay_instruction_like(text):
            continue
        normalized = text.casefold()
        if no_print and any(marker in normalized for marker in ("принт", "печать", "логотип", "print", "logo")):
            continue
        if profile == "clothing" and not has_print and role in {"closeup", "lifestyle_back"}:
            if any(marker in normalized for marker in ("принт", "печать", "логотип", "print", "logo")):
                continue
        if text not in cleaned:
            cleaned.append(text)

    facts = list(_extract_overlay_facts(product_description))
    if role == "facts" and facts:
        cleaned = facts + [item for item in cleaned if item not in facts]
    elif profile == "electronics" and role == "closeup":
        closeup_fact = next((fact for fact in facts if not re.search(r"\d+\s*(?:час|Вт|режим)", fact)), "")
        if closeup_fact:
            cleaned = [closeup_fact] + [item for item in cleaned if item != closeup_fact]

    if profile == "clothing":
        clothing_facts = list(_extract_clothing_overlay_facts(product_description))
        if role == "hero":
            cleaned = []
        elif role in {"facts", "closeup"} and clothing_facts:
            cleaned = clothing_facts + [item for item in cleaned if item not in clothing_facts]
        elif role == "lifestyle_back" and has_print:
            print_text = "Принт на спине" if "спин" in product_description.casefold() else "Принт на ткани"
            cleaned = [print_text] + [item for item in cleaned if item != print_text]

        fallbacks = {
            "closeup": ("Ткань и швы",) if not has_print else ("Качество печати",),
            "lifestyle_back": ("Посадка со спины",) if not has_print else ("Принт на спине",),
            "lifestyle_front": ("Свобода движений",),
            "lifestyle_three_quarter": ("Подчеркивает посадку",),
            "scenario": ("Для тренировок и дня",),
        }
        if not cleaned and role in fallbacks:
            cleaned.extend(fallbacks[role])

    return tuple(cleaned[:2])


def _home_decor_subtype(product_description: str) -> str:
    text = product_description.casefold()
    if "песочн" in text or "hourglass" in text or ("таймер" in text and "5" in text):
        return "hourglass"
    if "коврик" in text and ("ванн" in text or "душ" in text or "туалет" in text):
        return "bath_mat"
    if "органайзер" in text or "organizer" in text:
        return "organizer"
    if "ламп" in text or "светильник" in text or "lamp" in text:
        return "lamp"
    return "generic"


def _profile_sequence(profile: str, product_description: str = "") -> list[dict[str, Any]]:
    if profile == "clothing":
        return [
            {
                "role": "hero",
                "composition": "clean hero flatlay, product fully visible and neatly shaped",
                "background": "light warm studio surface with soft shadows, not a pure white empty background",
                "overlay": _overlay(),
            },
            {
                "role": "closeup",
                "composition": "close-up of fabric, seams or print detail; do not crop away the meaningful detail",
                "background": "soft neutral studio macro background with fabric texture visible",
                "overlay": _overlay("Ткань и швы"),
            },
            {
                "role": "lifestyle_back",
                "composition": "adult model wearing the clothing, back view, natural confident pose",
                "background": "marketplace sports or streetwear studio background, softly blurred",
                "overlay": _overlay("Принт на спине"),
            },
            {
                "role": "lifestyle_front",
                "composition": "adult model wearing the clothing, front view, natural pose, good fit visible",
                "background": "bright marketplace studio or gym background, softly blurred",
                "overlay": _overlay("Свобода движений"),
            },
            {
                "role": "lifestyle_three_quarter",
                "composition": "adult model wearing the clothing, three-quarter 30-60 degree angle, natural pose",
                "background": "premium marketplace lifestyle background with soft directional light",
                "overlay": _overlay("Подчеркивает посадку"),
            },
            {
                "role": "scenario",
                "composition": "model using the clothing in a realistic activity scenario",
                "background": "contextual lifestyle background matching the product use case",
                "overlay": _overlay("Для тренировок и дня"),
            },
            {
                "role": "closeup",
                "composition": "macro close-up of collar, seam, sleeve or printed element",
                "background": "soft macro studio background, no empty white field",
                "overlay": _overlay("Качество деталей"),
            },
        ]
    if profile == "kids":
        return [
            {
                "role": "hero",
                "composition": "clean product hero flatlay, full item visible",
                "background": "soft pastel studio surface with gentle shadows, not empty white",
                "overlay": _overlay("Комфорт каждый день"),
            },
            {
                "role": "lifestyle_front",
                "composition": "child model of appropriate age wearing the item, neutral safe pose",
                "background": "bright child-safe room or studio background, softly blurred",
                "overlay": _overlay("Удобно ребенку"),
            },
            {
                "role": "closeup",
                "composition": "close-up of fabric, seam or functional detail",
                "background": "soft studio macro background",
                "overlay": _overlay("Мягкая ткань"),
            },
            {
                "role": "lifestyle_back",
                "composition": "child model of appropriate age wearing the item, back view, neutral safe pose",
                "background": "bright child-safe room or outdoor studio background, softly blurred",
                "overlay": _overlay("Свободно двигаться"),
            },
            {
                "role": "scenario",
                "composition": "child model of appropriate age using the item in a calm everyday scenario",
                "background": "safe playground, school or home scene with soft natural light",
                "overlay": _overlay("Для прогулок и школы"),
            },
        ]
    return _generic_sequence(profile, product_description)


def _generic_sequence(profile: str, product_description: str = "") -> list[dict[str, Any]]:
    if profile == "home_decor":
        subtype = _home_decor_subtype(product_description)
        if subtype == "organizer":
            return [
                {
                    "role": "hero",
                    "composition": "hero product shot on a bathroom shelf or vanity surface, full organizer visible, clean product arrangement",
                    "background": "light bathroom interior with sink, mirror or towels softly blurred, warm studio light, not a pure white empty background",
                    "overlay": _overlay("Порядок в ванной"),
                },
                {
                    "role": "facts",
                    "composition": "facts card with organizer on one side and 3 concise storage benefits on the other",
                    "background": "clean bathroom countertop scene with subtle depth and soft shadows",
                    "overlay": _overlay("3 секции", "Все под рукой"),
                },
                {
                    "role": "closeup",
                    "composition": "closeup of compartments, edges and material finish; show practical storage details",
                    "background": "macro bathroom background with soft towel or tile blur",
                    "overlay": _overlay("Для косметики и щеток"),
                },
                {
                    "role": "scenario",
                    "composition": "organizer in use with cosmetics, toothbrushes or small accessories neatly placed",
                    "background": "realistic vanity or bathroom shelf scene with contextual props softly blurred",
                    "overlay": _overlay("Аккуратное хранение"),
                },
                {
                    "role": "interior",
                    "composition": "organizer placed in a clean bathroom storage zone, showing how it fits the interior",
                    "background": "bathroom shelf or countertop with mirror, towels and light decor softly blurred",
                    "overlay": _overlay("Вписывается в интерьер"),
                },
            ]
        if subtype == "bath_mat":
            return [
                {
                    "role": "hero",
                    "composition": "hero product shot of bath mat laid flat, full shape visible, neat edges and soft pile visible",
                    "background": "light bathroom floor scene near shower or bathtub, soft shadows and blurred interior elements, not a pure white empty background",
                    "overlay": _overlay("Мягкий ворс"),
                },
                {
                    "role": "facts",
                    "composition": "facts card with bath mat and 3 concise comfort or safety benefits",
                    "background": "clean bathroom floor with subtle tile texture and soft daylight",
                    "overlay": _overlay("Не скользит", "Быстро впитывает"),
                },
                {
                    "role": "closeup",
                    "composition": "closeup of pile texture and edge finish, show softness without changing material",
                    "background": "macro bathroom textile background with shallow depth of field",
                    "overlay": _overlay("Приятен для ног"),
                },
                {
                    "role": "scenario",
                    "composition": "bath mat placed near bathtub, shower or sink in a realistic bathroom use case",
                    "background": "cozy bathroom interior with towels and neutral decor softly blurred",
                    "overlay": _overlay("Комфорт после душа"),
                },
                {
                    "role": "interior",
                    "composition": "bath mat shown as part of a finished bathroom interior, full placement visible",
                    "background": "bright bathroom scene with bathtub, sink or shower elements softly blurred",
                    "overlay": _overlay("Для ванной и душа"),
                },
            ]
        if subtype == "lamp":
            return [
                {
                    "role": "hero",
                    "composition": "hero product shot of the lamp on a desk or bedside table, full silhouette visible",
                    "background": "warm desk or bedroom interior with soft glow and blurred decor, not a pure white empty background",
                    "overlay": _overlay("Мягкий свет"),
                },
                {
                    "role": "facts",
                    "composition": "facts card with lamp and 3 concise lighting benefits",
                    "background": "modern desk scene with books or laptop softly blurred",
                    "overlay": _overlay("Для работы и отдыха"),
                },
                {
                    "role": "closeup",
                    "composition": "closeup of switch, base, light form or texture",
                    "background": "macro desk background with warm directional light",
                    "overlay": _overlay("Удобное управление"),
                },
                {
                    "role": "scenario",
                    "composition": "lamp used as bedside, desk or room decor lighting",
                    "background": "cozy room interior with soft evening light",
                    "overlay": _overlay("Создает уют"),
                },
                {
                    "role": "interior",
                    "composition": "lamp integrated into a modern interior, visible on desk, shelf or bedside table",
                    "background": "room interior with books, decor and soft ambient light, background gently blurred",
                    "overlay": _overlay("Декор и свет"),
                },
            ]
        return [
            {
                "role": "hero",
                "composition": "hero product shot on a desk or tabletop, full product visible",
                "background": "light interior desk scene with soft shadows, blurred contextual elements, not a pure white empty background",
                "overlay": _overlay("Наглядный таймер"),
            },
            {
                "role": "facts",
                "composition": "facts card with the product on the left and 3 concise icon facts on the right",
                "background": "warm studio tabletop with subtle interior depth and soft shadows",
                "overlay": _overlay("5 минут", "Деревянная основа"),
            },
            {
                "role": "closeup",
                "composition": "closeup sand/glass or material detail, texture and construction visible",
                "background": "macro interior background with warm blur and directional light",
                "overlay": _overlay("Белый песок", "Защита колбы"),
            },
            {
                "role": "interior",
                "composition": "product placed on an interior shelf or table as decor",
                "background": "cozy shelf interior with books, plant or decor softly blurred",
                "overlay": _overlay("Декор для стола"),
            },
            {
                "role": "scenario",
                "composition": "scenario desk/kitchen use case, product in realistic context",
                "background": "desk or kitchen counter with contextual props softly blurred",
                "overlay": _overlay("Для кухни и работы"),
            },
            {
                "role": "facts",
                "composition": "clean benefits layout with product centered and two strong benefit blocks",
                "background": "soft studio table scene with depth, no blank white field",
                "overlay": _overlay("Просто и наглядно"),
            },
            {
                "role": "closeup",
                "composition": "detail close-up of base, finish, texture or functional part",
                "background": "warm macro background with shallow depth of field",
                "overlay": _overlay("Фактура материала"),
            },
        ]
    backgrounds = {
        "electronics": {
            "hero": "premium tech desk hero scene with soft screen glow, blurred accessories and controlled reflections",
            "facts": "clean tech facts layout on a matte desk surface with subtle gradient light and depth",
            "closeup": "macro tech surface with shallow depth of field, soft highlights and blurred cables or devices",
            "lifestyle_front": "realistic work or commute scene with product in use, background softly blurred",
            "scenario": "everyday desk, travel or walking scenario with natural light and contextual tech props",
        },
        "cosmetics": {
            "hero": "clean bathroom or vanity hero scene with soft reflections and product-safe lighting",
            "facts": "vanity facts layout with subtle tiles, mirror blur and gentle daylight",
            "closeup": "macro cosmetic texture or packaging background with soft reflection and shallow depth",
            "lifestyle_front": "calm skincare routine scene near mirror or vanity, softly blurred background",
            "scenario": "morning bathroom or dressing table scenario with warm natural light",
        },
        "bags": {
            "hero": "urban desk or travel hero scene with blurred laptop, notebook or suitcase elements",
            "facts": "organized travel facts layout with table surface, passport or notebook softly blurred",
            "closeup": "macro textile, zipper or pocket surface with shallow depth of field",
            "lifestyle_front": "city commute or work scene with product naturally used",
            "scenario": "travel, office or study scenario with realistic contextual props",
        },
        "food": {
            "hero": "warm kitchen tabletop or cafe counter hero scene with appetizing natural light",
            "facts": "clean food facts layout on tabletop with soft ingredient blur",
            "closeup": "macro food texture or packaging detail with shallow depth of field",
            "lifestyle_front": "snack or drink used in a daily routine scene",
            "scenario": "work, road or kitchen use scenario with warm contextual background",
        },
        "sports": {
            "hero": "gym or active lifestyle hero background with soft motion depth",
            "facts": "sports facts layout with mat, weights or training props softly blurred",
            "closeup": "macro sport material or grip texture with directional studio light",
            "lifestyle_front": "active training scene with product naturally used",
            "scenario": "fitness, outdoor or home workout scenario with dynamic but clear composition",
        },
    }
    overlays = {
        "electronics": (
            _overlay("Чистый звук"),
            _overlay("Подключение без лишних проводов"),
            _overlay("Разъемы крупно"),
            _overlay("Для работы и прогулок"),
            _overlay("Всегда под рукой"),
        ),
        "cosmetics": (
            _overlay("Уход каждый день"),
            _overlay("Увлажнение и ровный тон"),
            _overlay("Текстура и флакон"),
            _overlay("Легко в рутине"),
            _overlay("Для утреннего ухода"),
        ),
        "bags": (
            _overlay("Городской формат"),
            _overlay("Все помещается"),
            _overlay("Карманы крупно"),
            _overlay("Для работы и поездок"),
            _overlay("Удобно каждый день"),
        ),
        "food": (
            _overlay("Вкусный перекус"),
            _overlay("Состав и польза"),
            _overlay("Аппетитная текстура"),
            _overlay("С собой каждый день"),
            _overlay("Для работы и дороги"),
        ),
        "sports": (
            _overlay("Для тренировок"),
            _overlay("Комфорт в движении"),
            _overlay("Фактура и детали"),
            _overlay("Активный сценарий"),
            _overlay("Спорт каждый день"),
        ),
    }
    base_backgrounds = backgrounds.get(
        profile,
        {
            "hero": "contextual marketplace studio hero background with soft shadows",
            "facts": "clean facts layout with subtle contextual background and soft depth",
            "closeup": "macro contextual scene with shallow depth of field",
            "lifestyle_front": "realistic lifestyle background matching product use",
            "scenario": "real use scenario with contextual props and soft blur",
        },
    )
    profile_overlays = overlays.get(
        profile,
        (
            _overlay("Товар в деталях"),
            _overlay("Главные преимущества"),
            _overlay("Крупный план"),
            _overlay("В ежедневном использовании"),
            _overlay("Реальный сценарий"),
        ),
    )
    return [
        {
            "role": "hero",
            "composition": "hero product shot, full product visible, premium marketplace framing",
            "background": base_backgrounds["hero"],
            "overlay": profile_overlays[0],
        },
        {
            "role": "facts",
            "composition": "facts card with product and 3 concise benefits",
            "background": base_backgrounds["facts"],
            "overlay": profile_overlays[1],
        },
        {
            "role": "closeup",
            "composition": "close-up of material, texture, connector, label or functional detail",
            "background": base_backgrounds["closeup"],
            "overlay": profile_overlays[2],
        },
        {
            "role": "lifestyle_front",
            "composition": "realistic use-case lifestyle image, product naturally used in context",
            "background": base_backgrounds["lifestyle_front"],
            "overlay": profile_overlays[3],
        },
        {
            "role": "scenario",
            "composition": "scenario image showing where and how the customer uses the product",
            "background": base_backgrounds["scenario"],
            "overlay": profile_overlays[4],
        },
    ]


def build_slide_plan(
    product_description: str,
    marketplace: str,
    images_count: int,
    photo_analyses: list[PhotoAnalysis] | None = None,
) -> list[SlidePlan]:
    if images_count < 1 or images_count > 9:
        raise ValueError("images_count must be between 1 and 9")
    profile = detect_visual_profile(product_description, marketplace)
    sequence = _profile_sequence(profile, product_description)
    analyses = _analysis_by_index(photo_analyses, max((a.photo_index for a in photo_analyses or []), default=0) + 1)
    constraints = _common_negative_constraints(profile)

    plan: list[SlidePlan] = []
    for offset in range(images_count):
        item = sequence[offset % len(sequence)]
        role = str(item["role"])
        plan.append(
            SlidePlan(
                image_index=offset + 1,
                role=role,
                source_photo_index=_choose_photo_index(analyses, role),
                composition=str(item["composition"]),
                background=str(item["background"]),
                overlay_text=_overlay_for_slide(profile, role, product_description, tuple(item.get("overlay") or ())),
                negative_constraints=constraints,
                qa_checks=(
                    "pure_white_background",
                    "small_text",
                    "bad_typography",
                    "deformation",
                    "print_mismatch",
                ),
            )
        )
    return plan


def _visible_text_block(photo_analysis: PhotoAnalysis | None) -> str:
    if not photo_analysis or not photo_analysis.visible_text:
        return "No trusted visible text detected."
    return "Trusted visible text from selected reference: " + "; ".join(photo_analysis.visible_text)


def _defects_block(photo_analysis: PhotoAnalysis | None) -> str:
    if not photo_analysis or not photo_analysis.defects:
        return "No specific source photo defects detected."
    return "Fix these source photo defects: " + "; ".join(photo_analysis.defects)


def build_prompt_from_slide(
    product_description: str,
    marketplace: str,
    slide: SlidePlan,
    photo_analysis: PhotoAnalysis | None,
    image_guidance: str | None = None,
) -> str:
    profile = detect_visual_profile(product_description, marketplace)
    product_for_prompt = _sanitize_product_description_for_prompt(product_description, profile)
    marketplace_name = "Wildberries" if marketplace == "wb" else "Ozon"

    overlay = "; ".join(slide.overlay_text) if slide.overlay_text else ""
    overlay_part = f'Add text overlay: "{overlay}".' if overlay else ""

    prompt = (
        f"Professional marketplace card image for {marketplace_name}, 3:4 ratio.\n"
        f"Product: {product_for_prompt}\n"
        f"Slide role: {slide.role}. {slide.composition}.\n"
        f"Background: {slide.background}.\n"
        f"{overlay_part}\n"
        f"Use reference photo {slide.source_photo_index} as product source. "
        f"Preserve product appearance exactly: shape, color, print, texture. "
        f"Make it polished and commercial."
    ).strip()
    guidance = _normalize_image_guidance(image_guidance)
    if guidance:
        prompt += f"\nUser image guidance: {guidance}. Adapt it into a safe commercial marketplace product card style."
    return prompt


def _normalize_image_guidance(image_guidance: str | None) -> str:
    if not image_guidance:
        return ""
    return re.sub(r"\s+", " ", str(image_guidance)).strip()[:1200]


def build_image_concepts_from_plan(
    product_description: str,
    marketplace: str,
    images_count: int,
    photo_analyses: list[PhotoAnalysis] | None = None,
    image_guidance: str | None = None,
) -> list[ImageConcept]:
    normalized_marketplace = "ozon" if marketplace == "ozon" else "wb"
    plan = build_slide_plan(
        product_description=product_description,
        marketplace=normalized_marketplace,
        images_count=images_count,
        photo_analyses=photo_analyses,
    )
    analyses_by_index = {analysis.photo_index: analysis for analysis in photo_analyses or []}
    return [
        ImageConcept(
            image_index=slide.image_index,
            purpose=slide.role,
            photo_index=slide.source_photo_index,
            prompt=build_prompt_from_slide(
                product_description=product_description,
                marketplace=normalized_marketplace,
                slide=slide,
                photo_analysis=analyses_by_index.get(slide.source_photo_index),
                image_guidance=image_guidance,
            ),
        )
        for slide in plan
    ]


def build_photo_analysis_prompt(product_description: str, marketplace: str, photo_index: int) -> str:
    return (
        "Analyze this product reference photo for marketplace image generation.\n"
        f"Product description: {product_description.strip()}\n"
        f"Marketplace: {marketplace}\n"
        f"Photo index: {photo_index}\n"
        "Return strict JSON only:\n"
        "{\n"
        '  "photos": [{\n'
        f'    "photo_index": {photo_index},\n'
        '    "tags": ["front|back|closeup|label|on_model|flatlay"],\n'
        '    "visible_text": ["exact visible text"],\n'
        '    "defects": ["home lighting", "wrinkles", "messy background"],\n'
        '    "usable_for": ["hero", "front_on_model", "back_on_model", "closeup", "label_reference", "print_reference"],\n'
        '    "summary": "short practical summary"\n'
        "  }]\n"
        "}\n"
    )


def build_image_quality_prompt(concept_prompt: str, expected_visible_text: tuple[str, ...] = ()) -> str:
    expected_text = "; ".join(expected_visible_text) if expected_visible_text else "No exact print text requirement."
    return (
        "Evaluate the generated marketplace image against the reference photo and prompt.\n"
        "Return strict JSON only with fields passed, issues, summary.\n"
        f"Prompt used: {concept_prompt[:2500]}\n"
        f"Expected visible product text/print: {expected_text}\n"
        "Fail if you see: pure white empty background, tiny or ugly text, random-corner labels, "
        "clothing size as overlay text, obvious product deformation, changed color, changed or invented print/logo, "
        "or raw unprocessed home-photo look.\n"
        "Allowed issue names: "
        + ", ".join(sorted(QA_ISSUES))
        + "."
    )
