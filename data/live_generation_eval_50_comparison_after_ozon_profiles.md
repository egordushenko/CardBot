# Live eval 50 comparison after Ozon profiles

## Summary
- total_before: 50
- total_after: 50
- passed_before: 24
- passed_after: 27
- failed_before: 26
- failed_after: 23
- avg_score_before: 87.0
- avg_score_after: 89.6
- passed_delta: 3
- failed_delta: -3
- avg_score_delta: 2.6

## Issue deltas
- description_too_long: 0 -> 1 (+1)
- forbidden_characteristic_field:Гарантийный срок: 0 -> 1 (+1)
- generation_error:LLMResponseError: 2 -> 1 (-1)
- hallucinated_characteristic_value:Вес: 1 -> 1 (+0)
- too_few_characteristics: 23 -> 20 (-3)
- too_few_grounded_characteristics: 21 -> 19 (-2)

## Marketplace metrics
| Marketplace | Before passed | After passed | Before score | After score | Before chars | After chars | Before tags | After tags |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ozon | 21/25 | 22/25 | 91.2 | 95.2 | 5.0 | 5.8 | 16.1 | 17.0 |
| wb | 3/25 | 5/25 | 82.8 | 84.0 | 6.3 | 6.7 | 0.0 | 0.0 |

## Fixed cases
- wb_011_kids_pajama_detailed wb: 80 -> 100; ['too_few_characteristics', 'too_few_grounded_characteristics'] -> ok
- wb_021_sport_mat_medium wb: 80 -> 100; ['too_few_characteristics', 'too_few_grounded_characteristics'] -> ok
- ozon_015_dog_leash_short ozon: 0 -> 100; ['generation_error:LLMResponseError'] -> ok
- ozon_020_yoga_mat_medium ozon: 0 -> 100; ['generation_error:LLMResponseError'] -> ok
- ozon_022_notebook_medium ozon: 90 -> 100; ['too_few_characteristics'] -> ok

## Regressed cases
- ozon_011_men_sneakers_medium ozon: 100 -> 0; issues=['generation_error:LLMResponseError']; title=
- ozon_021_cleaner_short ozon: 100 -> 90; issues=['description_too_long']; title=Средство для кухни антижир 500 мл

## Failed after
- wb_001_women_tshirt_short wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Женщинам / Одежда title=Футболка оверсайз женская черная базовая
- wb_002_women_dress_medium wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Женщинам / Одежда title=Платье миди черное трикотажное приталенное офисное
- wb_003_women_pants_detailed wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Женщинам / Одежда title=Брюки палаццо бежевые высокая посадка свободный крой
- wb_004_women_jacket_medium wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Женщинам / Одежда title=Куртка женская демисезонная молочная на легком утеплителе
- wb_006_men_tshirt_short wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Мужчинам / Одежда title=Футболка мужская базовая белая
- wb_007_men_hoodie_medium wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Мужчинам / Одежда title=Мужское худи на молнии черное футер
- wb_008_men_pants_detailed wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Мужчинам / Одежда title=Брюки мужские карго хаки прямые хлопок
- wb_009_shoes_sneakers_medium wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Обувь title=Кроссовки мужские черные весна-лето шнуровка
- wb_010_shoes_slippers_short wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Обувь title=Тапочки женские домашние мягкие розовые
- wb_013_beauty_shampoo_short wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Красота title=Шампунь для волос восстанавливающий 400 мл
- wb_014_beauty_serum_detailed wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Красота title=Сыворотка для лица гиалуроновая 30 мл
- wb_015_home_bath_mat_medium wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Дом / Ванная / Коврики title=Коврик для ванной серый 50x80 см мягкий противоскользящий
- wb_016_home_organizer_detailed wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Дом title=Органайзер складной бежевый 40x30x25 см спанбонд
- wb_018_accessory_sleep_mask_medium wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Аксессуары / Маски для сна title=Маска для сна черная шелковая
- wb_019_electronics_lamp_detailed wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Дом title=Настольная лампа LED спиральная белая USB 5W 35 см
- wb_020_electronics_phone_medium wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Электроника / Смартфоны и телефоны / Смартфоны title=Смартфон 128GB 4GB RAM черный 6.5 дюйма
- wb_022_health_vitamin_medium wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Здоровье title=Витамин D3 2000 МЕ 60 капсул для взрослых
- wb_023_pet_food_medium wb score=90 issues=['hallucinated_characteristic_value:Вес'] category=None title=Сухой корм для кошек с курицей 1 кг
- wb_024_appliance_blender_detailed wb score=70 issues=['forbidden_characteristic_field:Гарантийный срок', 'too_few_characteristics', 'too_few_grounded_characteristics'] category=Бытовая техника title=Блендер погружной белый 600 Вт 2 скорости насадка
- wb_025_repair_faucet_medium wb score=80 issues=['too_few_characteristics', 'too_few_grounded_characteristics'] category=Строительство и ремонт title=Смеситель для раковины хром однорычажный латунный
- ozon_011_men_sneakers_medium ozon score=0 issues=['generation_error:LLMResponseError'] category=Обувь title=
- ozon_017_humidifier_medium ozon score=90 issues=['too_few_characteristics'] category=Бытовая техника title=Увлажнитель воздуха ультразвуковой 2 л USB подсветка для комнаты до 20 м² белый
- ozon_021_cleaner_short ozon score=90 issues=['description_too_long'] category=Бытовая химия title=Средство для кухни антижир 500 мл
