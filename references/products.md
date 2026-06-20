# ProductAPI — Товары (read-only)

Источник: `about.me.md` → tag/ProductAPI  
Write-методы (import, update, archive) пропущены — не нужны для анализа.

---

## POST /v3/product/list

Список всех товаров. Пагинация через `last_id` (cursor).  
Фильтр по `offer_id`/`product_id` — до 1000 за раз, остальные параметры игнорируются.

**Rate limit:** TBD

### Тело запроса

```json
{
  "filter": {
    "offer_id": [],
    "product_id": [],
    "visibility": "ALL"
  },
  "last_id": "",
  "limit": 1000
}
```

`visibility`: `ALL` | `VISIBLE` | `INVISIBLE` | `EMPTY_STOCK` | `NOT_MODERATED` | `MODERATED` | `DISABLED` | `BANNED` | `OVERPRICED` | `IN_SALE` | `REMOVED_FROM_SALE`

### Ответ

```json
{
  "result": {
    "items": [
      {
        "product_id": 3397917680,
        "offer_id": "Loft 2 b",
        "has_fbo_stocks": true,
        "has_fbs_stocks": false,
        "archived": false,
        "is_discounted": false
      }
    ],
    "total": 26,
    "last_id": "WzMzOTc5..."
  }
}
```

---

## POST /v3/product/info/list

Детальная информация о товарах по идентификаторам.  
Передавать только один тип идентификатора за раз. До 1000 за запрос.

**Rate limit:** TBD

### Тело запроса

```json
{ "offer_id": ["Loft 2 b"] }
{ "product_id": ["223681945"] }
{ "sku": ["3880823891"] }
```

### Ответ (ключевые поля)

```json
{
  "items": [
    {
      "id": 223681945,
      "offer_id": "Loft 2 b",
      "name": "...",
      "sku": 3880823891,
      "created_at": "2026-04-10T...",
      "updated_at": "2026-06-01T...",
      "price": "899",
      "old_price": "1200",
      "min_price": "800",
      "currency_code": "RUB",
      "vat": "0.2",
      "is_archived": false,
      "is_autoarchived": false,
      "is_discounted": false,
      "is_super": false,
      "is_kgt": false,
      "commissions": [
        { "sale_schema": "fbo", "percent": 15, "value": 200, "delivery_amount": 150, "return_amount": 50 }
      ],
      "price_indexes": { "... see /v5/product/info/prices": "" },
      "stocks": { "coming": 0, "present": 368, "reserved": 0 },
      "status": { "state": "processed", "state_description": "..." },
      "visibility_details": { "has_price": true, "has_stock": true, "active_product": true },
      "errors": []
    }
  ]
}
```

---

## POST /v1/product/rating-by-sku

Контент-рейтинг карточки товара (0–100) с разбивкой по группам.

**Rate limit:** TBD

### Тело запроса

```json
{ "skus": ["3880823891"] }
```

### Ответ

```json
{
  "products": [
    {
      "sku": 3880823891,
      "rating": 42.5,
      "groups": [
        {
          "key": "media",
          "name": "Медиа",
          "rating": 70,
          "weight": 25,
          "conditions": [
            { "key": "media_images_2", "description": "Добавлено 2 изображения", "fulfilled": true, "cost": 50 },
            { "key": "media_video", "description": "Добавлено видео", "fulfilled": false, "cost": 15 }
          ],
          "improve_attributes": [{ "id": 4080, "name": "3D-изображение" }],
          "improve_at_least": 2
        },
        { "key": "important_attributes", "name": "Важные атрибуты", "weight": 30 }
      ]
    }
  ]
}
```

---

## POST /v5/product/info/prices

Цены и прайс-индексы. Cursor-пагинация.

**Rate limit:** TBD

### Тело запроса

```json
{
  "cursor": "",
  "filter": { "offer_id": [], "product_id": [], "visibility": "ALL" },
  "limit": 1000
}
```

### Ответ (ключевые поля)

```json
{
  "items": [
    {
      "product_id": 1000123456,
      "offer_id": "Loft 2 b",
      "price": {
        "price": 899.0,
        "old_price": 1200.0,
        "min_price": 800.0,
        "net_price": 650.0,
        "currency_code": "RUB",
        "auto_action_enabled": true
      },
      "commissions": {
        "sales_percent_fbo": 15,
        "sales_percent_fbs": 12,
        "fbo_deliv_to_customer_amount": 14.75,
        "fbo_return_flow_amount": 50
      },
      "price_indexes": {
        "color_index": "GREEN",
        "ozon_index_data": {
          "min_price": 850.0,
          "price_index_value": 0.95
        },
        "external_index_data": {
          "min_price": 820.0,
          "price_index_value": 0.93
        }
      },
      "marketing_actions": {
        "ozon_actions_exist": true,
        "actions": [{ "title": "...", "value": 15, "date_from": "...", "date_to": "..." }]
      },
      "acquiring": 1.5
    }
  ],
  "cursor": "next_cursor_string",
  "total": 26
}
```

`color_index`: `GREEN` (супервыгодная) | `YELLOW` (выгодная) | `RED` (дорогая) | не установлен

---

## POST /v4/product/info/limit

Лимиты ассортимента. Тело запроса пустое.

**Rate limit:** TBD

### Ответ

```json
{
  "daily_create": { "limit": 500, "usage": 3, "reset_at": "2026-06-21T00:00:00Z" },
  "daily_update": { "limit": 1000, "usage": 12, "reset_at": "2026-06-21T00:00:00Z" },
  "operation_limits": { "limit": 10, "limit_type": "PER_MINUTE" },
  "total": { "limit": 100000, "usage": 26 }
}
```
