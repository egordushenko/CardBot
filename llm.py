from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from prompts import OZON_SYSTEM_PROMPT, WB_SYSTEM_PROMPT


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class LLMResponseError(RuntimeError):
    pass


@dataclass(frozen=True)
class CardGeneration:
    title: str
    description: str
    keywords: str
    characteristics: str
    tokens_used: int = 0
    marketplace: str = "wb"


MARKETPLACE_NAMES = {
    "wb": "Wildberries",
    "wildberries": "Wildberries",
    "ozon": "Ozon",
}


def normalize_marketplace(marketplace: str) -> str:
    normalized = marketplace.strip().lower()
    if normalized == "wildberries":
        return "wb"
    if normalized in {"wb", "ozon"}:
        return normalized
    raise LLMResponseError(f"Unsupported marketplace: {marketplace}")


def select_system_prompt(marketplace: str) -> str:
    normalized = normalize_marketplace(marketplace)
    if normalized == "ozon":
        return OZON_SYSTEM_PROMPT
    return WB_SYSTEM_PROMPT


def build_user_prompt(marketplace: str, user_input: str) -> str:
    normalized = normalize_marketplace(marketplace)
    name = MARKETPLACE_NAMES[normalized]
    return f"Маркетплейс: {name}\nТовар: {user_input.strip()}"


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


_SERVICE_MARKERS_RE = re.compile(r"(?i)(\\r|\\n|\bsummary\b|\bdepth\b|\btfo\b)")
_CJK_RE = re.compile(r"[\u3400-\u9fff]")


def sanitize_characteristics(value: str) -> str:
    lines: list[str] = []
    for raw_line in value.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if _SERVICE_MARKERS_RE.search(line) or _CJK_RE.search(line):
            break
        if ":" not in line:
            continue
        key, field_value = line.split(":", 1)
        key = key.strip()
        field_value = field_value.strip()
        if not key or not field_value:
            continue
        lines.append(f"{key}: {field_value}")
    return "\n".join(lines).strip()


def parse_generation_payload(
    payload: str,
    tokens_used: int = 0,
    marketplace: str = "wb",
) -> CardGeneration:
    try:
        data = json.loads(_strip_markdown_fence(payload))
    except json.JSONDecodeError as exc:
        raise LLMResponseError("LLM returned invalid JSON") from exc

    normalized_marketplace = normalize_marketplace(marketplace)
    search_field = "hashtags" if normalized_marketplace == "ozon" else "keywords"

    if "characteristics" in data:
        data["characteristics"] = sanitize_characteristics(str(data["characteristics"]))

    required = ("title", "description", search_field, "characteristics")
    for field in required:
        if not str(data.get(field, "")).strip():
            raise LLMResponseError(f"LLM response is missing required field: {field}")

    return CardGeneration(
        title=str(data["title"]).strip(),
        description=str(data["description"]).strip(),
        keywords=str(data[search_field]).strip(),
        characteristics=str(data["characteristics"]).strip(),
        tokens_used=tokens_used,
        marketplace=normalized_marketplace,
    )


async def generate_card(
    user_input: str,
    api_key: str,
    model: str = "deepseek/deepseek-v4-flash",
    site_url: str = "https://alterega.ru",
    marketplace: str = "wb",
) -> CardGeneration:
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
        timeout=30.0,
        max_retries=1,
        default_headers={
            "HTTP-Referer": site_url,
            "X-Title": "CardBot",
        },
    )

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": select_system_prompt(marketplace)},
            {"role": "user", "content": build_user_prompt(marketplace, user_input)},
        ],
        max_tokens=1500,
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise LLMResponseError("LLM returned empty response")

    usage: Any = getattr(response, "usage", None)
    tokens_used = int(getattr(usage, "total_tokens", 0) or 0)
    return parse_generation_payload(content, tokens_used=tokens_used, marketplace=marketplace)
