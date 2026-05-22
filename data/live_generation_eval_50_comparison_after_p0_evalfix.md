# Live eval comparison after P0 eval fix

## Summary

- Before passed: 27 / 50
- After passed: 25 / 50
- Passed delta: -2
- Before avg score: 89.6
- After avg score: 91.2
- Avg score delta: 1.6

## Fixed issues

- description_too_long: 1
- forbidden_characteristic_field:Гарантийный срок: 1
- generation_error:LLMResponseError: 1
- hallucinated_characteristic_value:Вес: 1
- too_few_characteristics: 2
- too_few_grounded_characteristics: 2

## New issues

- too_few_characteristics: 7
- too_few_grounded_characteristics: 2

## Cases

| Case | MP | Category | Score | Delta | Fixed | New/Current |
|---|---|---|---:|---:|---|---|
| wb_001_women_tshirt_short | wb | Женщинам / Одежда | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_002_women_dress_medium | wb | Женщинам / Одежда | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_003_women_pants_detailed | wb | Женщинам / Одежда | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_004_women_jacket_medium | wb | Женщинам / Одежда | 100 | 20 | too_few_characteristics, too_few_grounded_characteristics | - |
| wb_005_women_suit_detailed | wb | Женщинам / Одежда | 80 | -20 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_006_men_tshirt_short | wb | Мужчинам / Одежда | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_007_men_hoodie_medium | wb | Мужчинам / Одежда | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_008_men_pants_detailed | wb | Мужчинам / Одежда | 100 | 20 | too_few_characteristics, too_few_grounded_characteristics | - |
| wb_009_shoes_sneakers_medium | wb | Обувь | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_010_shoes_slippers_short | wb | Обувь | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_011_kids_pajama_detailed | wb | Детям / Одежда | 100 | 0 | - | - |
| wb_012_kids_toy_medium | wb | Игрушки / Антистресс | 80 | -20 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_013_beauty_shampoo_short | wb | Красота | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_014_beauty_serum_detailed | wb | Красота | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_015_home_bath_mat_medium | wb | Дом / Ванная / Коврики | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_016_home_organizer_detailed | wb | Дом | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_017_accessory_backpack_detailed | wb | Аксессуары | 100 | 0 | - | - |
| wb_018_accessory_sleep_mask_medium | wb | Аксессуары / Маски для сна | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_019_electronics_lamp_detailed | wb | Электроника | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_020_electronics_phone_medium | wb | Электроника / Смартфоны и телефоны / Смартфоны | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_021_sport_mat_medium | wb | Спорт | 100 | 0 | - | - |
| wb_022_health_vitamin_medium | wb | Здоровье | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| wb_023_pet_food_medium | wb | Товары для животных | 100 | 10 | hallucinated_characteristic_value:Вес | - |
| wb_024_appliance_blender_detailed | wb | Бытовая техника | 80 | 10 | forbidden_characteristic_field:Гарантийный срок | too_few_characteristics, too_few_grounded_characteristics |
| wb_025_repair_faucet_medium | wb | Строительство и ремонт | 80 | 0 | - | too_few_characteristics, too_few_grounded_characteristics |
| ozon_001_bath_mat_medium | ozon | Дом и сад | 100 | 0 | - | - |
| ozon_002_organizer_detailed | ozon | Дом и сад | 100 | 0 | - | - |
| ozon_003_headphones_detailed | ozon | Электроника | 100 | 0 | - | - |
| ozon_004_led_lamp_detailed | ozon | Электроника | 100 | 0 | - | - |
| ozon_005_phone_short | ozon | Электроника | 90 | -10 | - | too_few_characteristics |
| ozon_006_car_mats_medium | ozon | Автотовары | 100 | 0 | - | - |
| ozon_007_car_charger_detailed | ozon | Автотовары | 100 | 0 | - | - |
| ozon_008_kids_constructor_medium | ozon | Детские товары | 100 | 0 | - | - |
| ozon_009_kids_diapers_short | ozon | Детские товары | 90 | -10 | - | too_few_characteristics |
| ozon_010_women_tshirt_medium | ozon | Одежда | 100 | 0 | - | - |
| ozon_011_men_sneakers_medium | ozon | Обувь | 100 | 100 | generation_error:LLMResponseError | - |
| ozon_012_glue_medium | ozon | Строительство и ремонт | 100 | 0 | - | - |
| ozon_013_screwdriver_detailed | ozon | Строительство и ремонт | 100 | 0 | - | - |
| ozon_014_cat_food_medium | ozon | Товары для животных | 100 | 0 | - | - |
| ozon_015_dog_leash_short | ozon | Товары для животных | 100 | 0 | - | - |
| ozon_016_blender_detailed | ozon | Бытовая техника | 90 | -10 | - | too_few_characteristics |
| ozon_017_humidifier_medium | ozon | Бытовая техника | 90 | 0 | - | too_few_characteristics |
| ozon_018_table_medium | ozon | Мебель | 100 | 0 | - | - |
| ozon_019_vitamin_medium | ozon | Аптека | 100 | 0 | - | - |
| ozon_020_yoga_mat_medium | ozon | Спорт и отдых | 100 | 0 | - | - |
| ozon_021_cleaner_short | ozon | Бытовая химия | 90 | 0 | description_too_long | too_few_characteristics |
| ozon_022_notebook_medium | ozon | Канцелярские товары | 100 | 0 | - | - |
| ozon_023_decor_tape_medium | ozon | Хобби и творчество | 100 | 0 | - | - |
| ozon_024_tea_medium | ozon | Продукты питания | 90 | -10 | - | too_few_characteristics |
| ozon_025_hourglass_detailed | ozon | Дом и сад | 100 | 0 | - | - |
