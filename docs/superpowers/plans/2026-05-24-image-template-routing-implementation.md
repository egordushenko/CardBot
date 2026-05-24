# Image Template Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate distinct GPT Image 2 marketplace slide prompts from clothing-specific or universal seven-role template sequences while preserving parallel image generation.

**Architecture:** Add a focused template module that owns category routing, role ordering, and per-slide prompt construction. Extend the existing image-plan boundary to accept the already resolved category profile, and pass that profile from both image-only and text-plus-images flows without waiting for generated card text.

**Tech Stack:** Python, `pytest`, existing Telegram bot flow, OpenRouter GPT Image 2 request pipeline.

---

### Task 1: Template Selection And Prompt Construction

**Files:**
- Create: `image_prompt_templates.py`
- Modify: `llm.py`
- Test: `tests/test_llm.py`

- [x] **Step 1: Write failing tests**

Add tests asserting that `generate_image_prompts(..., category_profile={"category": "Одежда / Мужская одежда / Рашгарды"})` returns clothing purposes in order and that a non-clothing profile returns universal purposes. Assert each prompt contains the user's product facts, category, provided style/guidance, single-image intent, and an instruction not to invent unconfirmed facts.

- [x] **Step 2: Run tests to verify RED**

Run: `py -m pytest tests\test_llm.py -q`
Expected: failures because `category_profile` is not accepted and image concepts still all use purpose `marketplace`.

- [x] **Step 3: Implement template module and delegate from LLM layer**

Create `image_prompt_templates.py` with:

```python
def build_image_template_prompts(
    *,
    product_description: str,
    images_count: int,
    category_profile: dict[str, Any] | None,
    image_guidance: str,
) -> list[tuple[str, str]]:
    ...
```

The function selects clothing templates only from the category profile and returns the first `images_count` `(purpose, prompt)` pairs. Modify `llm.generate_image_prompts()` to accept `category_profile`, call this function, and convert pairs to `ImageConcept` without calling another model.

- [x] **Step 4: Run tests to verify GREEN**

Run: `py -m pytest tests\test_llm.py -q`
Expected: PASS.

### Task 2: Pass Resolved Category To Both Image Flows

**Files:**
- Modify: `bot.py`
- Test: `tests/test_bot_logic.py`

- [x] **Step 1: Write failing tests**

Add tests or extend existing async flow tests to verify `_generate_image_prompts_for_batch()` passes `category_profile` into `generate_image_prompts()`, and that the images-only generation path resolves category enrichment before constructing image concepts.

- [x] **Step 2: Run tests to verify RED**

Run: `py -m pytest tests\test_bot_logic.py -q`
Expected: failures because category profiles are not forwarded to image prompt planning.

- [x] **Step 3: Implement category-profile plumbing**

Extend `_generate_image_prompts_for_batch(..., category_profile=None)` and forward the new parameter. In the combined flow, pass the already resolved profile to that call. In images-only flow, resolve enrichment with `has_photo=True` before calling `generate_image_prompts()` and pass its category profile.

- [x] **Step 4: Run tests to verify GREEN**

Run: `py -m pytest tests\test_bot_logic.py -q`
Expected: PASS.

### Task 3: Regression Verification And Delivery

**Files:**
- Verify: `image_prompt_templates.py`, `llm.py`, `bot.py`, `tests/test_llm.py`, `tests/test_bot_logic.py`

- [x] **Step 1: Check image request regression**

Run: `py -m pytest tests\test_image_generator.py -q`
Expected: PASS, confirming one collage input and one 3:4 output request contract remain intact.

- [x] **Step 2: Run the full suite and UTF-8 guards**

Run: `py -m pytest -q` and `powershell -File C:\Users\alterega\.codex\scripts\assert-utf8.ps1 -Path <each changed human-readable file>`
Expected: all tests pass and each checked file reports valid UTF-8 without mojibake.

- [ ] **Step 3: Commit only task files and push**

Run:

```powershell
git add -- image_prompt_templates.py llm.py bot.py tests/test_llm.py tests/test_bot_logic.py docs/superpowers/plans/2026-05-24-image-template-routing-implementation.md
git commit -m "feat: route image generation templates by category"
git push
```

Do not add existing untracked experiment assets or source prompt documents.
