# Persistent Generation Actions And History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Store repeatable generation inputs in PostgreSQL so result/history actions survive bot restarts and cover text, combined, and image-only flows.

**Architecture:** Extend `generations` into the user-facing history registry and keep `image_sessions` as image execution telemetry. New inline callbacks carry a `generation_id`, which is resolved owner-safely from `generations` before saving a template or beginning a repeat flow; legacy callbacks remain for old Telegram messages.

**Tech Stack:** Python 3.11+, python-telegram-bot, asyncpg/PostgreSQL, pytest.

---

### Task 1: Persist Repeatable Generation Metadata

**Files:**
- Modify: `db.py`
- Test: `tests/test_db.py`

- [ ] **Step 1: Write failing schema and database behavior tests**

Add assertions that `CREATE_TABLES_SQL` migrates `generations` with `marketplace`, `mode`, `photo_file_ids`, `images_count`, and `image_guidance`. Add async database tests using fake connections that require:

```python
generation_id = await db.save_successful_generation(
    user_id=123,
    input_text="Рашгард Therapy",
    card=card,
    usage_mode=UsageMode.TRIAL,
    marketplace="ozon",
    mode="text_and_images",
    photo_file_ids=["photo-1"],
    images_count=3,
    image_guidance="светлый фон",
)
assert generation_id == 41
```

and:

```python
generation_id = await db.save_image_only_generation(
    user_id=123,
    input_text="Часы песочные",
    marketplace="ozon",
    photo_file_ids=["photo-1"],
    images_count=3,
    image_guidance="чистый фон",
)
assert generation_id == 42
```

Also require `get_generation_for_action(41, 123)` to issue `WHERE id = $1 AND user_id = $2` and return repeatable metadata.

- [ ] **Step 2: Run tests to prove RED**

Run: `py -m pytest -q tests/test_db.py`

Expected: failures for missing schema fields and missing/old database method contracts.

- [ ] **Step 3: Implement database metadata storage**

Change `CREATE_TABLES_SQL`:

```sql
ALTER TABLE generations ADD COLUMN IF NOT EXISTS marketplace TEXT;
ALTER TABLE generations ADD COLUMN IF NOT EXISTS mode TEXT;
ALTER TABLE generations ADD COLUMN IF NOT EXISTS photo_file_ids TEXT;
ALTER TABLE generations ADD COLUMN IF NOT EXISTS images_count INT;
ALTER TABLE generations ADD COLUMN IF NOT EXISTS image_guidance TEXT;
```

Extend `save_successful_generation(..., marketplace, mode, photo_file_ids=None, images_count=None, image_guidance=None) -> int`, JSON-encode photo ids, insert the metadata and `RETURNING id`. Add `save_image_only_generation(...) -> int` inserting input metadata with `NULL` output fields. Extend `get_recent_generations()` to return id and metadata; add `get_generation_for_action(generation_id, user_id)`.

- [ ] **Step 4: Run database tests to prove GREEN**

Run: `py -m pytest -q tests/test_db.py`

Expected: PASS.

### Task 2: Make Result Keyboards Addressable

**Files:**
- Modify: `bot_keyboards.py`
- Test: `tests/test_bot_logic.py`

- [ ] **Step 1: Write failing callback tests**

Require:

```python
keyboard = build_after_generation_keyboard(generation_id=41)
assert callbacks == ["action:generate", "generation_save:41", "generation_repeat:41", ...]
```

and the same for `build_after_image_generation_keyboard(generation_id=42)`. Add a test for:

```python
keyboard = build_history_generation_keyboard(41)
assert callback == "generation_save:41"
```

Keep existing no-id assertions for legacy callbacks.

- [ ] **Step 2: Run tests to prove RED**

Run: `py -m pytest -q tests/test_bot_logic.py -k "keyboard or after_generation"`

Expected: failure because builders do not accept ids and history action builder does not exist.

- [ ] **Step 3: Implement keyboard builders**

Give the after-generation builders an optional `generation_id: int | None = None`. Select callbacks with:

```python
save_callback = f"generation_save:{generation_id}" if generation_id is not None else "action:save_template"
repeat_callback = f"generation_repeat:{generation_id}" if generation_id is not None else "action:repeat_edit"
```

Add `build_history_generation_keyboard(generation_id)` containing one save button.

- [ ] **Step 4: Run keyboard tests to prove GREEN**

Run: `py -m pytest -q tests/test_bot_logic.py -k "keyboard or after_generation"`

Expected: PASS.

### Task 3: Load Actions From Database And Render Unified History

**Files:**
- Modify: `bot.py`
- Test: `tests/test_bot_logic.py`

- [ ] **Step 1: Write failing flow tests**

Add fake DB support for `get_generation_for_action()` and require:

```python
await handle_callback(_FakeCallbackUpdate("generation_save:41"), context)
assert context.user_data["pending_template_generation_id"] == 41
```

Then enter a name and assert saved template data comes from the DB input metadata rather than output fields.

Require:

```python
await handle_callback(_FakeCallbackUpdate("generation_repeat:41"), context)
assert context.user_data["last_generation"]["description"] == "исходный запрос"
assert context.user_data["awaiting_repeat_changes"] is True
```

For `history_command`, provide three records (`text_only`, `text_and_images`, `images_only`) and assert each complete record gets `generation_save:<id>`, while a legacy row with missing `marketplace`/`mode` has no save markup.

- [ ] **Step 2: Run tests to prove RED**

Run: `py -m pytest -q tests/test_bot_logic.py -k "generation_save or generation_repeat or history"`

Expected: failure because addressable callbacks and unified rendering do not exist.

- [ ] **Step 3: Implement owner-safe action loading**

Add a converter from generation DB rows into the existing repeatable input dictionary. In `handle_callback()` parse `generation_save:<id>` and `generation_repeat:<id>`, load via `db.get_generation_for_action(id, user_id)`, reject absent/incomplete rows with `⚠️ Генерация не найдена.`, and set only temporary dialog state.

When a `generation_save` flow asks for a name, store:

```python
context.user_data["pending_template_generation_id"] = generation_id
```

In `_handle_template_name()`, if that id exists, re-fetch the generation by id and owner before calling `save_template()`. Preserve legacy `last_generation` behavior when no pending id is present.

- [ ] **Step 4: Implement history rendering**

Render all rows returned by `get_recent_generations(user_id, limit=5)`. For output formatting:

```python
if generation["mode"] == "images_only":
    text = f"...\nЗапрос: {input_text}\n\n🖼 Только изображения: запрошено {images_count}"
else:
    text = existing_text_output_format
```

Pass `reply_markup=build_history_generation_keyboard(generation["id"])` only when both `marketplace` and `mode` are present.

- [ ] **Step 5: Run flow tests to prove GREEN**

Run: `py -m pytest -q tests/test_bot_logic.py -k "generation_save or generation_repeat or history"`

Expected: PASS.

### Task 4: Store New Records And Attach Durable Buttons In Every Flow

**Files:**
- Modify: `bot.py`
- Test: `tests/test_bot_logic.py`

- [ ] **Step 1: Write failing generation wiring tests**

Add tests around text-only, combined, and image-only helpers using fake DB methods. Require:

```python
assert reply_markup callback data includes "generation_save:41"
assert reply_markup callback data includes "generation_repeat:41"
```

Require image-only to call `save_image_only_generation()` only after generated images are successfully persisted. Require combined text persistence to receive `mode="text_and_images"` plus its photo/settings inputs and to reuse its returned id for both success and partial image-failure result keyboards.

- [ ] **Step 2: Run tests to prove RED**

Run: `py -m pytest -q tests/test_bot_logic.py -k "durable or image_only or text_and_images"`

Expected: failures because current flow stores only memory state and static callbacks.

- [ ] **Step 3: Wire text-only and combined creation**

Capture `generation_id` returned by `save_successful_generation()`. Supply metadata from the caller flow and use:

```python
build_after_generation_keyboard(generation_id=generation_id)
build_after_image_generation_keyboard(generation_id=generation_id)
```

where a user-facing completion or partial-completion message is sent.

- [ ] **Step 4: Wire image-only creation**

After `save_generated_images_and_consume_balance()` succeeds and at least one image exists, call `save_image_only_generation()` with marketplace, description, photos, image count, and guidance. Use the returned id in the image-result keyboard.

- [ ] **Step 5: Run wiring tests to prove GREEN**

Run: `py -m pytest -q tests/test_bot_logic.py`

Expected: PASS.

### Task 5: Documentation, Regression Verification, And Delivery

**Files:**
- Modify only if implementation reveals a necessary clarification: `docs/superpowers/specs/2026-05-24-persistent-generation-actions-history-design.md`
- Track: `docs/superpowers/plans/2026-05-24-persistent-generation-actions-history-implementation.md`

- [ ] **Step 1: Run full verification**

Run:

```powershell
py -m pytest -q
powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\alterega\.codex\scripts\assert-utf8.ps1' -Path 'D:\github\CardBot\bot.py' -FailOnSuspiciousMojibake
powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\alterega\.codex\scripts\assert-utf8.ps1' -Path 'D:\github\CardBot\bot_keyboards.py' -FailOnSuspiciousMojibake
powershell -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\alterega\.codex\scripts\assert-utf8.ps1' -Path 'D:\github\CardBot\db.py' -FailOnSuspiciousMojibake
git diff --check
```

Expected: test suite passes, UTF-8 checks show no likely mojibake, and diff check reports no whitespace errors.

- [ ] **Step 2: Review security boundary**

Verify every addressable callback resolves its generation using both `id` and `user_id`, and that no output data is written into templates.

- [ ] **Step 3: Commit and push scoped files**

Stage only `db.py`, `bot_keyboards.py`, `bot.py`, touched tests, the specification if changed, and this plan. Do not stage scratch files under `data/`.

```powershell
git add -- db.py bot_keyboards.py bot.py tests/test_db.py tests/test_bot_logic.py docs/superpowers/plans/2026-05-24-persistent-generation-actions-history-implementation.md
git commit -m "feat: persist generation actions and history templates"
git push origin main
```
