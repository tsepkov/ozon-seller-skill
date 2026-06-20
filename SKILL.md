---
name: ozon-seller-skill
description: Query Ozon Seller API to help sellers analyze their performance — sales, analytics, stocks, orders, and more.
---

# ozon-seller-skill

Scripts for querying the Ozon Seller API. Each script in `scripts/` covers one API method and prints JSON to stdout.

## Required environment variables

| Variable | Description |
|---|---|
| `OZON_API_KEY` | API key from Ozon Seller personal account (Settings → API keys) |
| `OZON_CLIENT_ID` | Numeric client ID shown next to the API key |

Both must be present or any script will exit with an error.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in OZON_API_KEY and OZON_CLIENT_ID
```

## Running a script

Each script is a standalone CLI tool. Pass arguments as flags; run with `--help` for details.

```bash
python scripts/<method>.py [options]
```

Output is always JSON on stdout. Errors go to stderr with a non-zero exit code.

## Scripts

### Информация о кабинете продавца (`references/about.me.md`)

| Script | Method | Endpoint | Description |
|---|---|---|---|
| `scripts/seller_info.py` | POST | `/v1/seller/info` | Компания, рейтинги, подписка |
| `scripts/seller_logistics_info.py` | POST | `/v1/seller/ozon-logistics/info` | Статус подключения Ozon Доставки, доступные схемы (FBO/FBS) |

### Аналитические отчёты (`references/analytics.md`)

| Script | Method | Endpoint | Description |
|---|---|---|---|
| `scripts/analytics_stock_on_warehouses.py` | POST | `/v2/analytics/stock_on_warehouses` | Остатки и товары в перемещении по складам. Флаги: `--limit`, `--offset`, `--warehouse-type` |
| `scripts/analytics_stocks_turnover.py` | POST | `/v1/analytics/turnover/stocks` | Оборачиваемость: среднесуточные продажи, дней остатка. **Лимит: 1 запрос/мин.** Флаги: `--limit`, `--offset`, `--sku` |
| `scripts/analytics_stocks.py` | POST | `/v1/analytics/stocks` | Детальная аналитика остатков по кластерам. `--sku` обязателен (до 100). `--cluster-id` и `--macrolocal-cluster-id` взаимоисключающие |

### Финансовые отчёты (`references/finance.md`)

| Script | Method | Endpoint | Description |
|---|---|---|---|
| `scripts/finance_realization.py` | POST | `/v2/finance/realization` | Отчёт о реализации за месяц. Флаги: `--month`, `--year` |
| `scripts/finance_realization_posting.py` | POST | `/v1/finance/realization/posting` | Позаказный отчёт о реализации (только до авг. 2023). Флаги: `--month`, `--year` |
| `scripts/finance_transactions.py` | POST | `/v3/finance/transaction/list` | Список транзакций (макс. 1 месяц). `--from`/`--to` или `--posting-number`. Пагинация: `--page`, `--page-size` |
| `scripts/finance_transaction_totals.py` | POST | `/v3/finance/transaction/totals` | Итоговые суммы по транзакциям. `--from`/`--to` или `--posting-number` |

### Товары (`references/products.md`)

| Script | Method | Endpoint | Description |
|---|---|---|---|
| `scripts/product_list.py` | POST | `/v3/product/list` | Список товаров с cursor-пагинацией. Фильтр: `--visibility`, `--offer-id`, `--product-id` |
| `scripts/product_info.py` | POST | `/v3/product/info/list` | Детальная информация: комиссии, статус, видимость, ошибки. `--offer-id` / `--sku` / `--product-id` (один тип, до 1000) |
| `scripts/product_content_rating.py` | POST | `/v1/product/rating-by-sku` | Контент-рейтинг карточки (0–100) с разбивкой по группам. `--sku` обязателен |
| `scripts/product_prices.py` | POST | `/v5/product/info/prices` | Цены, % комиссии FBO/FBS, прайс-индекс (GREEN/YELLOW/RED). Cursor-пагинация |
| `scripts/product_quota.py` | POST | `/v4/product/info/limit` | Лимиты ассортимента: общий лимит SKU, суточные квоты на создание/обновление |

### Отзывы (`references/reviews.md`)

| Script | Method | Endpoint | Description |
|---|---|---|---|
| `scripts/review_count.py` | POST | `/v2/review/count` | Количество отзывов по статусам (new / viewed / processed / total) |
| `scripts/review_list.py` | POST | `/v2/review/list` | Список отзывов. Фильтры: `--sku`, `--status`, `--order-status`, `--from`, `--to`. Cursor-пагинация |
| `scripts/review_info.py` | POST | `/v2/review/info` | Детальная информация по отзыву с фото и видео. `--id` обязателен |
| `scripts/review_change_status.py` | POST | `/v2/review/change-status` | Изменить статус отзывов (до 100 за раз). `--status`, `--id` |

## Rate limits

Rate limits per method are documented in the script's header comment. The Ozon API enforces limits per `Client-Id`; scripts do not add extra throttling unless noted.

## Auth

`scripts/init.py` exports `get_session()` which returns a `requests.Session` pre-configured with the required headers. All method scripts import from it — do not inline credentials.
