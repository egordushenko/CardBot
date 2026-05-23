# Manual review: live eval 50 after Ozon profiles

## Summary

- Script score improved: passed 24/50 -> 27/50, average score 87.0 -> 89.6.
- Ozon improved materially: passed 21/25 -> 22/25, average score 91.2 -> 95.2, average characteristics 5.0 -> 5.8.
- WB improved only slightly: passed 3/25 -> 5/25, average score 82.8 -> 84.0, average characteristics 6.3 -> 6.7.
- Manual review found issues that the fixed eval does not catch yet. Bot is better than before, but not ready to call this clean.

## Main Manual Findings

### P0: Ozon country default is still wrong

User requirement: if country is not explicit, default to China.

Observed problems:

- `ozon_002_organizer_detailed`: `Страна-изготовитель: Россия`
- `ozon_006_car_mats_medium`: `Страна-изготовитель: Россия`
- `ozon_010_women_tshirt_medium`: `Страна-изготовитель: Россия`
- `ozon_012_glue_medium`: `Страна-изготовитель: Россия`
- `ozon_014_cat_food_medium`: `Страна-изготовитель: Россия`
- `ozon_018_table_medium`: `Страна-изготовитель: Россия`
- `ozon_019_vitamin_medium`: `Страна-изготовитель: Россия`
- `ozon_021_cleaner_short`: `Страна-изготовитель: Россия`
- `ozon_022_notebook_medium`: `Страна-изготовитель: Россия`
- `ozon_024_tea_medium`: `Страна-изготовитель: Россия`
- `ozon_009_kids_diapers_short`: `Страна-изготовитель: Не указана`
- `ozon_013_screwdriver_detailed`: `Страна-изготовитель: Не указана`

Conclusion: Ozon enrichment/default layer still injects Russia or allows "Не указана". This is a release blocker for text quality because it contradicts the agreed rule.

### P0: Eval misses fabricated or irrelevant characteristics

Examples:

- `ozon_013_screwdriver_detailed`: `Время полного высыхания: Не применимо`, `Время схватывания: Не применимо`, `Партномер: Не указан`
- `ozon_014_cat_food_medium`: `Класс корма: Супер-премиум` is not grounded in input.
- `ozon_021_cleaner_short`: `Вкусовой акцент (вкус): Без вкуса`, `Максимальная влажность, %: 95`
- `wb_013_beauty_shampoo_short`: `Срок годности: В соответствии с информацией на упаковке`
- `wb_024_appliance_blender_detailed`: `Гарантийный срок: 1 год`, `Срок эксплуатации: 3 года`

Conclusion: eval must reject placeholders like "Не указана", "Не применимо", warranty/shelf-life/service-life fields without explicit input, and nonsensical fields for the detected product.

### P0: WB category/profile mismatch still leaks wrong fields

Examples:

- `wb_016_home_organizer_detailed`: organizer received `Форма коврика`, `Основа коврика`, `Особенности коврика`.
- `wb_019_electronics_lamp_detailed`: lamp was categorized as `Дом`, not electronics/lighting.
- `wb_023_pet_food_medium`: pet food category was `None`.
- `wb_021_sport_mat_medium`: sport mat category was `None`.

Conclusion: WB category detection still needs broader aliases and safer fallback profiles. Generic "Дом" must not inherit carpet-specific fields.

### P1: WB characteristics are often too sparse or miss obvious input facts

Examples:

- `wb_009_shoes_sneakers_medium`: input had upper material, eco-leather, light sole, lacing, season; output only color/sex/season/country.
- `wb_025_repair_faucet_medium`: input had chrome, single lever, brass body, ceramic cartridge, flexible hoses; output only комплект/страна/назначение.
- `wb_020_electronics_phone_medium`: input had 128 GB, 4 GB RAM, two SIM, camera 50 MP; output missed memory and SIM count.

Conclusion: for medium/detailed inputs, extractor should prioritize explicit facts before trying to satisfy target count.

### P1: Some script issues are false positives

Example:

- `wb_023_pet_food_medium`: `Вес: 1 кг` was marked as hallucinated, but input says `упаковка 1 кг`.

Conclusion: grounding eval should treat weight/volume/count values as grounded when the numeric value appears in the input even if the exact field word is absent.

## Net Result

Ozon category profiles improved the measurable report, especially electronics and several Ozon categories. However, manual review shows remaining release blockers:

1. Country default for Ozon is inconsistent.
2. Eval is too lenient for irrelevant/fabricated fields.
3. WB category detection/profile selection is still the main weak spot.

Recommended next patch: fix the three P0 items above, then rerun the same 50-case report.
