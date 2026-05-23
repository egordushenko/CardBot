from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from visual_pipeline import build_image_concepts_from_plan, detect_visual_profile, fallback_photo_analysis


CASES: list[dict[str, Any]] = [
    {
        "marketplace": "wb",
        "photos_count": 5,
        "images_count": 5,
        "product": "Рашгард Therapy черный размер M, 100% хлопок, тянущийся облегающий с горловиной, качественная печать текста Therapy на спине",
    },
    {
        "marketplace": "wb",
        "photos_count": 5,
        "images_count": 5,
        "product": "Женская футболка оверсайз черная, хлопок, свободный крой, базовая для повседневной носки",
    },
    {
        "marketplace": "ozon",
        "photos_count": 4,
        "images_count": 5,
        "product": "Часы песочные высота 15 см. Черное деревянное основание, белый песок, длительность цикла 5 минут, противоударные накладки на колбе",
    },
    {
        "marketplace": "ozon",
        "photos_count": 4,
        "images_count": 5,
        "product": "Настольная лампа LED спиральная белая USB 5W, три режима света, регулировка яркости, высота 35 см",
    },
    {
        "marketplace": "wb",
        "photos_count": 4,
        "images_count": 5,
        "product": "Наушники беспроводные Bluetooth черные, шумоподавление, микрофон, кейс, до 6 часов работы",
    },
    {
        "marketplace": "ozon",
        "photos_count": 4,
        "images_count": 5,
        "product": "Сыворотка для лица с ниацинамидом 30 мл, увлажнение, выравнивает тон, пипетка, стеклянный флакон",
    },
    {
        "marketplace": "wb",
        "photos_count": 4,
        "images_count": 5,
        "product": "Органайзер для ванной комнаты пластиковый белый, 3 секции, для косметики и зубных щеток",
    },
    {
        "marketplace": "ozon",
        "photos_count": 5,
        "images_count": 5,
        "product": "Рюкзак городской черный 22 литра, полиэстер, отделение для ноутбука 15.6, внешний карман, USB кабель",
    },
    {
        "marketplace": "wb",
        "photos_count": 3,
        "images_count": 4,
        "product": "Протеиновый батончик шоколадный 60 г, 20 г белка, без сахара, перекус после тренировки",
    },
    {
        "marketplace": "ozon",
        "photos_count": 5,
        "images_count": 5,
        "product": "Детская куртка демисезонная синяя, капюшон, молния, утепленная, для мальчика 6 лет",
    },
    {
        "marketplace": "wb",
        "photos_count": 4,
        "images_count": 4,
        "product": "Крем для рук увлажняющий с алоэ 75 мл, быстро впитывается, для сухой кожи",
    },
    {
        "marketplace": "ozon",
        "photos_count": 4,
        "images_count": 5,
        "product": "Коврик для ванной серый 50x80 см, мягкий ворс, нескользящее основание, быстро впитывает влагу",
    },
]


BAD_PROMPT_MARKERS = (
    "Made for everyday use",
    "Key features",
    "Reliable details",
    "Clean product view",
    "Fabric and print detail",
)


def _prompt_issues(prompt: str, product: str) -> list[str]:
    issues: list[str] = []
    overlay_line = next((line for line in prompt.splitlines() if line.startswith("TEXT OVERLAY:")), "")
    for marker in BAD_PROMPT_MARKERS:
        if marker in overlay_line:
            issues.append(f"bad_marker:{marker}")
    if "Детали" in overlay_line:
        issues.append("meaningless_overlay_heading")
    if "Do NOT use a pure white empty background" not in prompt:
        issues.append("missing_background_guard")
    if "large readable modern sans-serif" not in prompt:
        issues.append("missing_typography_guard")
    if "Do NOT place text in random corners" not in prompt:
        issues.append("missing_text_position_guard")
    if detect_visual_profile(product) in {"clothing", "kids"}:
        if "размер" in overlay_line.casefold() or "size" in overlay_line.casefold():
            issues.append("clothing_size_in_overlay")
        if "Preserve printed logos and text exactly" not in prompt:
            issues.append("missing_print_preservation_guard")
    return issues


def build_report() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for index, case in enumerate(CASES, start=1):
        product = str(case["product"])
        photos_count = int(case["photos_count"])
        analyses = [
            fallback_photo_analysis(photo_index, product, photos_count)
            for photo_index in range(photos_count)
        ]
        concepts = build_image_concepts_from_plan(
            product_description=product,
            marketplace=str(case["marketplace"]),
            images_count=int(case["images_count"]),
            photo_analyses=analyses,
        )
        concept_items: list[dict[str, Any]] = []
        case_issues: list[str] = []
        for concept in concepts:
            issues = _prompt_issues(concept.prompt, product)
            case_issues.extend(issues)
            concept_items.append(
                {
                    "image_index": concept.image_index,
                    "role": concept.purpose,
                    "photo_index": concept.photo_index,
                    "prompt": concept.prompt,
                    "issues": issues,
                }
            )
        cases.append(
            {
                "case_index": index,
                "marketplace": case["marketplace"],
                "visual_profile": detect_visual_profile(product, str(case["marketplace"])),
                "product": product,
                "photo_analysis": [
                    {
                        "photo_index": item.photo_index,
                        "tags": list(item.tags),
                        "visible_text": list(item.visible_text),
                        "defects": list(item.defects),
                        "usable_for": list(item.usable_for),
                    }
                    for item in analyses
                ],
                "concepts": concept_items,
                "issues": sorted(set(case_issues)),
            }
        )
    return {
        "summary": {
            "cases": len(cases),
            "concepts": sum(len(case["concepts"]) for case in cases),
            "cases_with_issues": sum(1 for case in cases if case["issues"]),
        },
        "cases": cases,
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Visual Prompt Dry Run",
        "",
        f"- Cases: {report['summary']['cases']}",
        f"- Concepts: {report['summary']['concepts']}",
        f"- Cases with issues: {report['summary']['cases_with_issues']}",
        "",
    ]
    for case in report["cases"]:
        lines.extend(
            [
                f"## Case {case['case_index']}: {case['visual_profile']} / {case['marketplace']}",
                "",
                f"Input: {case['product']}",
                "",
                f"Issues: {', '.join(case['issues']) if case['issues'] else 'none'}",
                "",
                "Photo analysis:",
            ]
        )
        for item in case["photo_analysis"]:
            lines.append(
                f"- photo {item['photo_index']}: tags={item['tags']}; usable_for={item['usable_for']}; defects={item['defects']}"
            )
        lines.append("")
        for concept in case["concepts"]:
            lines.extend(
                [
                    f"### Image {concept['image_index']}: {concept['role']} / photo {concept['photo_index']}",
                    "",
                    f"Issues: {', '.join(concept['issues']) if concept['issues'] else 'none'}",
                    "",
                    "```text",
                    concept["prompt"],
                    "```",
                    "",
                ]
            )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build image prompt dry-run without GPT Image generation.")
    parser.add_argument("--json", default="data/visual_prompt_dry_run.json")
    parser.add_argument("--md", default="data/visual_prompt_dry_run.md")
    args = parser.parse_args()

    report = build_report()
    json_path = Path(args.json)
    md_path = Path(args.md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(report, md_path)
    print(json.dumps(report["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
