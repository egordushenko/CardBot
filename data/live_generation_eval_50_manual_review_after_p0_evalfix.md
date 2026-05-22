# Manual review after P0 profiles

## Summary

- Total: 50
- Passed: 25 / 50
- Average score: 91.2
- WB: 6 / 25, avg 84.8
- Ozon: 19 / 25, avg 97.6

## Manual findings

- P0 regressions not found: Ozon no longer outputs ??????/?? ??????? as default country; reviewed failed Ozon cases use ?????.
- WB fallback improved: organizer is no longer contaminated by rug fields; lamp is categorized as ???????????; pet food is categorized as ?????? ??? ????????; sport mat is categorized as ?????.
- The remaining dominant issue is sparse WB characteristics, not wrong category contamination. 19/25 WB cases still have too_few_characteristics + too_few_grounded_characteristics.
- Ozon quality is strong: 19/25 pass, avg 97.6. Remaining 6 failures are short-input cases with too_few_characteristics only.
- Eval fix applied: "???????? 1 ??" now counts as grounded input for field ???; pet food no longer gets hallucinated_weight.

## Spot-checked cases

### WB organizer

- Category: ???
- Characteristics kept: ?????? ????????????, ????????????, ???????? ???????, ????, ??????.
- Removed/absent: ????? ???????, ?????? ???????, ??????????? ???????.

### WB lamp

- Category: ???????????
- Characteristics: ??????, ????, ?????? ????????????, ????????????, ????????, ???????????, ??? ?????.
- Remaining issue: eval wants more fields than honest input/profile allows.

### WB pet food

- Category: ?????? ??? ????????
- Characteristics: ???, ??? ?????????, ????, ??????????, ?????? ????????????, ???.
- No hallucination issue after eval fix.

### WB sport mat

- Category: ?????
- Score: 100
- Characteristics: ???, ??????, ??????????, ????????????, ?????? ????????????.

## Remaining work

- P1: improve WB category-specific extraction so detailed inputs produce 6-10 useful characteristics for beauty, electronics, home, appliances and repair.
- P1: tune WB eval target by input richness/category instead of raw dataset average, otherwise good short-input cards are undercounted.
- P2: for Ozon short inputs, add 1-2 safe extracted fields where possible, but do not invent specs.

## Failed cases after eval fix

| Case | Marketplace | Category | Issues |
|---|---|---|---|
| wb_001_women_tshirt_short | wb | Женщинам / Одежда | too_few_characteristics, too_few_grounded_characteristics |
| wb_002_women_dress_medium | wb | Женщинам / Одежда | too_few_characteristics, too_few_grounded_characteristics |
| wb_003_women_pants_detailed | wb | Женщинам / Одежда | too_few_characteristics, too_few_grounded_characteristics |
| wb_005_women_suit_detailed | wb | Женщинам / Одежда | too_few_characteristics, too_few_grounded_characteristics |
| wb_006_men_tshirt_short | wb | Мужчинам / Одежда | too_few_characteristics, too_few_grounded_characteristics |
| wb_007_men_hoodie_medium | wb | Мужчинам / Одежда | too_few_characteristics, too_few_grounded_characteristics |
| wb_009_shoes_sneakers_medium | wb | Обувь | too_few_characteristics, too_few_grounded_characteristics |
| wb_010_shoes_slippers_short | wb | Обувь | too_few_characteristics, too_few_grounded_characteristics |
| wb_012_kids_toy_medium | wb | Игрушки / Антистресс | too_few_characteristics, too_few_grounded_characteristics |
| wb_013_beauty_shampoo_short | wb | Красота | too_few_characteristics, too_few_grounded_characteristics |
| wb_014_beauty_serum_detailed | wb | Красота | too_few_characteristics, too_few_grounded_characteristics |
| wb_015_home_bath_mat_medium | wb | Дом / Ванная / Коврики | too_few_characteristics, too_few_grounded_characteristics |
| wb_016_home_organizer_detailed | wb | Дом | too_few_characteristics, too_few_grounded_characteristics |
| wb_018_accessory_sleep_mask_medium | wb | Аксессуары / Маски для сна | too_few_characteristics, too_few_grounded_characteristics |
| wb_019_electronics_lamp_detailed | wb | Электроника | too_few_characteristics, too_few_grounded_characteristics |
| wb_020_electronics_phone_medium | wb | Электроника / Смартфоны и телефоны / Смартфоны | too_few_characteristics, too_few_grounded_characteristics |
| wb_022_health_vitamin_medium | wb | Здоровье | too_few_characteristics, too_few_grounded_characteristics |
| wb_024_appliance_blender_detailed | wb | Бытовая техника | too_few_characteristics, too_few_grounded_characteristics |
| wb_025_repair_faucet_medium | wb | Строительство и ремонт | too_few_characteristics, too_few_grounded_characteristics |
| ozon_005_phone_short | ozon | Электроника | too_few_characteristics |
| ozon_009_kids_diapers_short | ozon | Детские товары | too_few_characteristics |
| ozon_016_blender_detailed | ozon | Бытовая техника | too_few_characteristics |
| ozon_017_humidifier_medium | ozon | Бытовая техника | too_few_characteristics |
| ozon_021_cleaner_short | ozon | Бытовая химия | too_few_characteristics |
| ozon_024_tea_medium | ozon | Продукты питания | too_few_characteristics |
