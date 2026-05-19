# CardBot — Техническое задание MVP

Статус: готово к реализации
Версия: 1.0
Дата: 2026-05-19

---

## Цель

Реализовать Telegram-бот CardBot — AI-генератор карточек товаров для продавцов на Wildberries и Ozon. Пользователь описывает товар в свободной форме, бот генерирует полную SEO-оптимизированную карточку (название, описание, ключевые слова, характеристики) через DeepSeek V4 Flash API.

---

## Технический стек

- **Язык:** Python 3.11+
- **Telegram-библиотека:** `python-telegram-bot` (async, версия 20+), polling режим через `application.run_polling()`
- **LLM:** DeepSeek V4 Flash через OpenRouter API (OpenAI-compatible endpoint)
- **База данных:** PostgreSQL 16 (существующий инстанс на VPS, порт 5432)
- **Платёжная система:** Robokassa (уже настроена на VPS, знакомый стек)
- **HTTP-клиент для LLM:** `httpx` или `openai` SDK с кастомным base_url
- **Хостинг:** существующий VPS Ubuntu 24.04 (`31.207.76.54`)
- **Деплой:** GitHub Actions + self-hosted runner + systemd (аналогично существующему `alterega-bot`)

---

## Структура файлов проекта

```
cardbot/
├── bot.py                 # точка входа, Application setup, все хэндлеры
├── db.py                  # подключение к PostgreSQL, все SQL-запросы
├── llm.py                 # интеграция с OpenRouter/DeepSeek, генерация карточки
├── payments.py            # Robokassa: формирование ссылки, обработка ResultURL
├── config.py              # чтение переменных окружения
├── prompts.py             # системный промпт и шаблоны
├── requirements.txt
├── env.example
└── .github/
    └── workflows/
        └── deploy.yml     # CI/CD деплой на VPS
```

---

## База данных

### Подключение
Использовать существующую PostgreSQL на `127.0.0.1:5432`.
Создать отдельную базу данных `cardbot`.
Переменная окружения: `CARDBOT_DB_URL` (формат: `postgresql://user:pass@127.0.0.1:5432/cardbot`)

### Таблицы

```sql
-- Пользователи
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,           -- Telegram user_id
    username TEXT,
    first_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    trial_used INT DEFAULT 0,        -- сколько бесплатных генераций использовано
    balance INT DEFAULT 0            -- остаток платных генераций
);

-- История генераций
CREATE TABLE IF NOT EXISTS generations (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    input_text TEXT NOT NULL,        -- что написал пользователь
    output_title TEXT,               -- сгенерированное название
    output_description TEXT,         -- сгенерированное описание
    output_keywords TEXT,            -- сгенерированные ключевые слова
    output_characteristics TEXT,     -- сгенерированные характеристики
    is_trial BOOLEAN DEFAULT FALSE,  -- была ли это триальная генерация
    tokens_used INT,                 -- токены потрачены (для аналитики)
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Платежи
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    inv_id TEXT UNIQUE NOT NULL,     -- Robokassa InvId
    package_code TEXT NOT NULL,      -- 'starter' | 'basic' | 'pro'
    amount_rub INT NOT NULL,         -- сумма в рублях
    generations_count INT NOT NULL,  -- количество генераций в пакете
    status TEXT DEFAULT 'pending',   -- pending | paid | failed
    created_at TIMESTAMPTZ DEFAULT NOW(),
    paid_at TIMESTAMPTZ
);
```

---

## Пакеты и триал

```python
TRIAL_GENERATIONS = 3  # бесплатных генераций при старте

PACKAGES = {
    'starter': {
        'name': 'Старт',
        'generations': 20,
        'price_rub': 390,
        'description': '20 карточек'
    },
    'basic': {
        'name': 'Основной',
        'generations': 100,
        'price_rub': 990,
        'description': '100 карточек'
    },
    'pro': {
        'name': 'Про',
        'generations': 300,
        'price_rub': 1990,
        'description': '300 карточек'
    }
}
```

---

## Telegram-бот: команды и flow

### Команды
- `/start` — приветствие, создание пользователя в БД, показ главного меню
- `/generate` — запустить генерацию карточки
- `/balance` — показать остаток генераций
- `/history` — последние 5 генераций пользователя
- `/buy` — показать пакеты и кнопки оплаты
- `/help` — краткая инструкция

### User flow — генерация

1. Пользователь пишет `/generate` или просто любой текст в главном состоянии
2. Бот проверяет баланс:
   - Если `trial_used < TRIAL_GENERATIONS` → разрешить как триальную
   - Если `balance > 0` → разрешить как платную
   - Иначе → отправить сообщение об исчерпании + кнопки пакетов
3. Бот отправляет сообщение: "Отправьте описание товара. Минимум — название. Можно добавить материал, размер, цвет, особенности."
4. Пользователь отправляет описание (любой текст)
5. Бот отвечает: "⏳ Генерирую карточку..."
6. Бот вызывает LLM (см. раздел LLM)
7. Бот отправляет результат четырьмя отдельными сообщениями:

```
📌 НАЗВАНИЕ:
<сгенерированное название>

📝 ОПИСАНИЕ:
<сгенерированное описание>

🔑 КЛЮЧЕВЫЕ СЛОВА:
<список ключевых слов через запятую>

📋 ХАРАКТЕРИСТИКИ:
<список характеристик>
```

8. После каждого результата — кнопки: [🔄 Сгенерировать ещё] [💳 Купить генерации]
9. Обновить счётчик: `trial_used += 1` или `balance -= 1`
10. Сохранить в `generations`

### User flow — оплата

1. Пользователь нажимает кнопку пакета или пишет `/buy`
2. Бот показывает три пакета с InlineKeyboard
3. Пользователь выбирает пакет
4. Бот генерирует ссылку на оплату Robokassa и отправляет её
5. После оплаты Robokassa делает POST на ResultURL
6. Бот обновляет `payments.status = 'paid'` и `users.balance += generations_count`
7. Бот уведомляет пользователя: "✅ Оплата получена! Добавлено N генераций. Ваш баланс: X."

### Главное меню (InlineKeyboard после /start)

```
[⚡ Сгенерировать карточку]
[💳 Купить генерации] [📊 Мой баланс]
[📋 История] [❓ Помощь]
```

---

## LLM интеграция (llm.py)

### Endpoint
```python
import openai

client = openai.AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "deepseek/deepseek-v4-flash"
```

### Системный промпт (prompts.py)

```python
SYSTEM_PROMPT = """Ты эксперт по SEO-оптимизации карточек товаров для маркетплейсов Wildberries и Ozon.

Твоя задача — по описанию товара сгенерировать полную оптимизированную карточку.

Требования к названию:
- Структура: [основной запрос] + [ключевая характеристика] + [преимущество/уточнение]
- Длина: 40-60 символов
- Не указывай пол и цвет в названии (только в характеристиках)
- Пример: "Коврики автомобильные резиновые Lada Granta с бортиками"

Требования к описанию:
- Длина: 800-1200 символов
- Структура: короткий смысловой блок (2-3 предложения) → преимущества списком (4-6 пунктов) → сценарии применения (2-3 варианта)
- Ключевые слова встроены естественно, без спама
- Написано для людей, не для алгоритма

Требования к ключевым словам:
- 12-15 запросов через запятую
- Микс: высокочастотные (2-3), среднечастотные (6-7), низкочастотные (3-4)
- Без стоп-слов, без дублей, включай синонимы

Требования к характеристикам:
- Формат: "Ключ: Значение" каждая с новой строки
- Извлеки из описания: материал, цвет, размер, совместимость, тип и другие релевантные параметры
- Если параметр неизвестен — не придумывай, пропусти

Отвечай СТРОГО в формате JSON без markdown-блоков:
{
  "title": "...",
  "description": "...",
  "keywords": "...",
  "characteristics": "..."
}"""
```

### Функция генерации

```python
async def generate_card(user_input: str) -> dict:
    """
    Генерирует карточку товара по описанию пользователя.
    Возвращает dict с ключами: title, description, keywords, characteristics.
    При ошибке выбрасывает исключение.
    """
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Товар: {user_input}"}
        ],
        max_tokens=1500,
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    
    raw = response.choices[0].message.content
    result = json.loads(raw)
    
    # Валидация обязательных полей
    required = ["title", "description", "keywords", "characteristics"]
    for field in required:
        if field not in result:
            raise ValueError(f"Missing field: {field}")
    
    return result
```

### Обработка ошибок LLM
- Если API вернул ошибку → сообщить пользователю "Произошла ошибка, попробуйте ещё раз" и **не списывать** генерацию с баланса
- Timeout: 30 секунд
- Retry: 1 повтор при сетевой ошибке

---

## Платёжная система (payments.py)

### Robokassa
Использовать ту же логику что в существующем боте Alterega (файл `deep.py`).

Ключевые параметры:
- `MerchantLogin` = `ROBOKASSA_LOGIN`
- Подпись: MD5 от `MerchantLogin:OutSum:InvId:Password1`
- `Shp_user_id` — передавать Telegram user_id как дополнительный параметр
- `Shp_package` — передавать код пакета

### ResultURL endpoint
Бот должен принимать Robokassa ResultURL. Реализовать через встроенный webhook или отдельный HTTP-сервер на порту (например, 8090, добавить в UFW).

Альтернатива проще для MVP: использовать существующий Next.js сайт как ResultURL proxy (добавить новый endpoint `/api/payment/robokassa/cardbot-result`) который после валидации подписи уведомляет бота через Telegram API.

**Рекомендуемый подход для MVP:** встроенный aiohttp сервер в боте на порту `8090`, маршрут `POST /robokassa/result`.

Логика обработки ResultURL:
1. Получить POST-параметры: `OutSum`, `InvId`, `SignatureValue`, `Shp_user_id`, `Shp_package`
2. Проверить подпись: MD5(`OutSum:InvId:Password2:Shp_package=...:Shp_user_id=...`)
3. Найти payment по `inv_id`
4. Обновить `status = 'paid'`, `paid_at = NOW()`
5. Обновить `users.balance += generations_count`
6. Отправить пользователю уведомление через `bot.send_message(user_id, ...)`
7. Вернуть `OK{InvId}`

---

## Переменные окружения (env.example)

```env
# Telegram
BOT_TOKEN=

# OpenRouter
OPENROUTER_API_KEY=

# PostgreSQL
CARDBOT_DB_URL=postgresql://cardbot_user:password@127.0.0.1:5432/cardbot

# Robokassa
ROBOKASSA_LOGIN=
ROBOKASSA_PASSWORD1=
ROBOKASSA_PASSWORD2=
ROBOKASSA_TEST_MODE=0

# URLs
SITE_URL=https://alterega.ru
CARDBOT_RESULT_URL=https://alterega.ru/api/payment/robokassa/cardbot-result

# Bot settings
TRIAL_GENERATIONS=3
```

---

## Деплой

### Systemd unit
Создать `/etc/systemd/system/cardbot.service`:

```ini
[Unit]
Description=CardBot Telegram Bot
After=network.target postgresql.service

[Service]
Type=simple
User=cardbot
WorkingDirectory=/opt/cardbot
EnvironmentFile=/etc/cardbot.env
ExecStart=/opt/cardbot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### GitHub Actions workflow (.github/workflows/deploy.yml)
Аналогично существующему `deploy-bot.yml` для Alterega:
- Триггер: push в `main`
- Runner: self-hosted на VPS
- Деплой: rsync → `systemctl restart cardbot`

### Nginx
Добавить в существующий nginx конфиг проксирование ResultURL:
```nginx
location /api/payment/robokassa/cardbot-result {
    proxy_pass http://127.0.0.1:8090/robokassa/result;
}
```

---

## Требования к качеству кода

- Все хэндлеры async
- Логирование через стандартный `logging` в `cardbot.log`
- Никаких секретов в коде — только через env
- Все DB-операции через параметризованные запросы (защита от SQL injection)
- `try/except` вокруг LLM-вызовов и DB-операций
- При старте бота — автоматическое создание таблиц если не существуют (`CREATE TABLE IF NOT EXISTS`)

---

## Что НЕ делать в MVP

- Не делать веб-интерфейс
- Не делать интеграцию с API WB/Ozon
- Не делать генерацию изображений
- Не делать реферальную программу
- Не делать аналитику для владельца
- Не усложнять архитектуру — один файл `bot.py` с хэндлерами лучше чем сложная структура

---

## Критические инварианты

- Генерация НЕ списывается с баланса при ошибке LLM или сетевой ошибке
- Платёж НЕ зачисляется без проверки подписи Robokassa
- ResultURL должен возвращать `OK{InvId}` при успехе
- Каждый блок результата (название / описание / ключи / характеристики) — отдельное сообщение для удобного копирования
- `inv_id` в таблице `payments` — уникальный, upsert при повторном ResultURL

---

## Порядок реализации

1. `config.py` — загрузка env
2. `db.py` — подключение к PostgreSQL, создание таблиц, все CRUD-функции
3. `prompts.py` — системный промпт
4. `llm.py` — генерация карточки через OpenRouter
5. `payments.py` — формирование ссылки Robokassa, обработка ResultURL
6. `bot.py` — все хэндлеры, Application setup, запуск
7. `requirements.txt` и `env.example`
8. `.github/workflows/deploy.yml`
