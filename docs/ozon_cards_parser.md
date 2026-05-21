# Ozon Cards Parser

Цель: собрать референсные карточки Ozon с рейтингом от `4.7` и отзывами от `1000` в JSON-датасет для CardBot.

## Браузерный сбор

1. Открой карточку товара Ozon в браузере, где доступна страница товара.
2. Выполни JavaScript из `tools/ozon_browser_extract.js` в консоли страницы.
3. Сохрани JSON из консоли или буфера обмена в `data/ozon_raw/<product-id>.json`.
4. Повтори для нужных карточек.

## Сборка датасета

```powershell
py -3.11 tools\ozon_cards_parser.py --input-dir data\ozon_raw --output data\ozon_cards_dataset.json
```

Скрипт пропускает карточки ниже порогов `--min-rating 4.7` и `--min-reviews 1000`.

## Формат записи

```json
{
  "source_url": "https://www.ozon.ru/product/example-123/",
  "product_id": "123",
  "category": "Электроника / Наушники",
  "title": "Название товара",
  "description": "Описание товара",
  "rating": 4.8,
  "review_count": 2400,
  "characteristics": {
    "Тип": "Наушники"
  },
  "hashtags": ["#наушники"],
  "scraped_at": "2026-05-20T20:00:00.000Z"
}
```

## Анализ датасета

После сбора запускаем анализатор, чтобы получить статистику по длинам, категориям, частым характеристикам и правила для промптов:

```powershell
py -3.11 tools\ozon_dataset_analyzer.py --dataset data\ozon_cards_dataset.json --output-md data\ozon_dataset_analysis.md --output-json data\ozon_dataset_analysis.json
```

Результаты:

- `data/ozon_dataset_analysis.md` — человекочитаемый отчет;
- `data/ozon_dataset_analysis.json` — машинный отчет, который можно использовать для генерации prompt-rules.
