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
        "Do NOT use meaningless headings like \"Детали\".",
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


def _profile_sequence(profile: str) -> list[dict[str, Any]]:
    if profile == "clothing":
        return [
            {
                "role": "hero",
                "composition": "clean hero flatlay, product fully visible and neatly shaped",
                "background": "light warm studio surface with soft shadows, not a pure white empty background",
                "overlay": ("Clean product view",),
            },
            {
                "role": "closeup",
                "composition": "close-up of fabric, seams or print detail; do not crop away the meaningful detail",
                "background": "soft neutral studio macro background with fabric texture visible",
                "overlay": ("Fabric and print detail",),
            },
            {
                "role": "lifestyle_back",
                "composition": "adult model wearing the clothing, back view, natural confident pose",
                "background": "marketplace sports or streetwear studio background, softly blurred",
                "overlay": ("Back print",),
            },
            {
                "role": "lifestyle_front",
                "composition": "adult model wearing the clothing, front view, natural pose, good fit visible",
                "background": "bright marketplace studio or gym background, softly blurred",
                "overlay": ("Comfort in motion",),
            },
            {
                "role": "lifestyle_three_quarter",
                "composition": "adult model wearing the clothing, three-quarter 30-60 degree angle, natural pose",
                "background": "premium marketplace lifestyle background with soft directional light",
                "overlay": ("Fits the body",),
            },
            {
                "role": "scenario",
                "composition": "model using the clothing in a realistic activity scenario",
                "background": "contextual lifestyle background matching the product use case",
                "overlay": ("Ready for daily use",),
            },
            {
                "role": "closeup",
                "composition": "macro close-up of collar, seam, sleeve or printed element",
                "background": "soft macro studio background, no empty white field",
                "overlay": ("Detail quality",),
            },
        ]
    if profile == "kids":
        return [
            {
                "role": "hero",
                "composition": "clean product hero flatlay, full item visible",
                "background": "soft pastel studio surface with gentle shadows, not empty white",
                "overlay": ("Everyday comfort",),
            },
            {
                "role": "lifestyle_front",
                "composition": "child model of appropriate age wearing the item, neutral safe pose",
                "background": "bright child-safe room or studio background, softly blurred",
                "overlay": ("Comfort for kids",),
            },
            {
                "role": "closeup",
                "composition": "close-up of fabric, seam or functional detail",
                "background": "soft studio macro background",
                "overlay": ("Soft fabric",),
            },
        ]
    return _generic_sequence(profile)


def _generic_sequence(profile: str) -> list[dict[str, Any]]:
    if profile == "home_decor":
        return [
            {
                "role": "hero",
                "composition": "hero product shot on a desk or tabletop, full product visible",
                "background": "light interior desk scene with soft shadows, blurred contextual elements, not a pure white empty background",
                "overlay": ("Made for everyday use",),
            },
            {
                "role": "facts",
                "composition": "facts card with the product on the left and 3 concise icon facts on the right",
                "background": "warm studio tabletop with subtle interior depth and soft shadows",
                "overlay": ("Key features",),
            },
            {
                "role": "closeup",
                "composition": "closeup sand/glass or material detail, texture and construction visible",
                "background": "macro interior background with warm blur and directional light",
                "overlay": ("Reliable details",),
            },
            {
                "role": "interior",
                "composition": "product placed on an interior shelf or table as decor",
                "background": "cozy shelf interior with books, plant or decor softly blurred",
                "overlay": ("Adds atmosphere",),
            },
            {
                "role": "scenario",
                "composition": "scenario desk/kitchen use case, product in realistic context",
                "background": "desk or kitchen counter with contextual props softly blurred",
                "overlay": ("Useful every day",),
            },
            {
                "role": "facts",
                "composition": "clean benefits layout with product centered and two strong benefit blocks",
                "background": "soft studio table scene with depth, no blank white field",
                "overlay": ("Simple and visual",),
            },
            {
                "role": "closeup",
                "composition": "detail close-up of base, finish, texture or functional part",
                "background": "warm macro background with shallow depth of field",
                "overlay": ("Material close-up",),
            },
        ]
    backgrounds = {
        "electronics": "modern desk setup with soft screen glow and blurred accessories",
        "cosmetics": "clean bathroom or vanity scene with soft reflections and product-safe lighting",
        "bags": "urban desk or travel scene with blurred laptop, notebook or suitcase elements",
        "food": "warm kitchen tabletop or cafe counter with appetizing natural light",
        "sports": "gym or active lifestyle background with soft motion depth",
    }
    base_background = backgrounds.get(profile, "contextual marketplace studio background with soft shadows")
    return [
        {
            "role": "hero",
            "composition": "hero product shot, full product visible, premium marketplace framing",
            "background": base_background,
            "overlay": ("Main product view",),
        },
        {
            "role": "facts",
            "composition": "facts card with product and 3 concise benefits",
            "background": base_background,
            "overlay": ("Key benefits",),
        },
        {
            "role": "closeup",
            "composition": "close-up of material, texture, connector, label or functional detail",
            "background": "macro version of the contextual scene with shallow depth of field",
            "overlay": ("Detail quality",),
        },
        {
            "role": "lifestyle_front",
            "composition": "realistic use-case lifestyle image, product naturally used in context",
            "background": base_background,
            "overlay": ("Made for daily use",),
        },
        {
            "role": "scenario",
            "composition": "scenario image showing where and how the customer uses the product",
            "background": base_background,
            "overlay": ("Practical scenario",),
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
    sequence = _profile_sequence(profile)
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
                overlay_text=tuple(item.get("overlay") or ()),
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
) -> str:
    overlay = "; ".join(slide.overlay_text) if slide.overlay_text else "No overlay text unless it improves the slide."
    constraints = "\n".join(f"- {item}" for item in slide.negative_constraints)
    qa_checks = ", ".join(slide.qa_checks)
    marketplace_name = "Wildberries" if marketplace == "wb" else "Ozon"
    return (
        f"Create a 3:4 marketplace image for {marketplace_name}.\n"
        f"PRODUCT: {product_description.strip()}\n"
        f"SLIDE ROLE: {slide.role}\n"
        f"REFERENCE PHOTO: use only photo {slide.source_photo_index}; do not merge details from other photos.\n"
        f"COMPOSITION: {slide.composition}.\n"
        f"BACKGROUND: {slide.background}; Do NOT use a pure white empty background.\n"
        f"TEXT OVERLAY: {overlay}. Typography must be large readable modern sans-serif, 1-2 text blocks, safe margins. Do NOT place text in random corners.\n"
        f"{_visible_text_block(photo_analysis)}\n"
        f"{_defects_block(photo_analysis)}\n"
        f"NEGATIVE CONSTRAINTS:\n{constraints}\n"
        f"QA TARGETS: {qa_checks}.\n"
        "Make the image polished, commercial and ready for a marketplace gallery."
    )


def build_image_concepts_from_plan(
    product_description: str,
    marketplace: str,
    images_count: int,
    photo_analyses: list[PhotoAnalysis] | None = None,
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
