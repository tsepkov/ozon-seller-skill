# AnalyticsAPI — Аналитические отчёты

Источник: `about.me.md` → tag/AnalyticsAPI

---

## POST /v2/analytics/stock_on_warehouses

Отчёт по остаткам и товарам в перемещении по складам Ozon.

**Rate limit:** TBD  
**Пагинация:** `limit` (обязателен, по умолч. 100) + `offset`

### Тело запроса

| Поле | Тип | Обязателен | Описание |
|---|---|---|---|
| `limit` | int64 | да | Строк на странице (по умолчанию 100) |
| `offset` | int64 | нет | Сколько строк пропустить |
| `warehouse_type` | string | нет | `ALL` (умолч.) \| `EXPRESS_DARK_STORE` \| `NOT_EXPRESS_DARK_STORE` |

### Ответ

```json
{
  "result": {
    "rows": [
      {
        "sku": 0,
        "item_code": "string",
        "item_name": "string",
        "free_to_sell_amount": 0,
        "promised_amount": 0,
        "reserved_amount": 0,
        "warehouse_name": "string"
      }
    ]
  }
}
```

---

## POST /v1/analytics/turnover/stocks

Оборачиваемость товара и количество дней, на которое хватит остатка.  
Соответствует разделу FBO → Управление остатками в ЛК.

**Rate limit: 1 запрос в минуту на Client-Id**  
Если передаются `sku`, параметры `limit` и `offset` необязательны.

### Тело запроса

| Поле | Тип | Обязателен | Описание |
|---|---|---|---|
| `limit` | int32 [1..1000] | нет | Строк в ответе |
| `offset` | int32 | нет | Сколько строк пропустить |
| `sku` | string[] | нет | Фильтр по SKU |

### Ответ

```json
{
  "items": [
    {
      "sku": 0,
      "offer_id": "string",
      "name": "string",
      "current_stock": 0,
      "ads": 0.0,
      "idc": 0.0,
      "idc_grade": "GRADES_NONE",
      "turnover": 0.0,
      "turnover_grade": "GRADES_NONE"
    }
  ]
}
```

**Grades:** `GRADES_NONE` | `GRADES_NOSALES` | `GRADES_GREEN` | `GRADES_YELLOW` | `GRADES_RED` | `GRADES_CRITICAL`

- `idc` — дней, на которое хватит остатка
- `ads` — среднесуточные продажи за 60 дней
- `turnover` — фактическая оборачиваемость в днях

---

## POST /v1/analytics/stocks

Детальная аналитика по остаткам на складах в разрезе кластеров.  
Соответствует разделу FBO → Управление остатками в ЛК.  
**Обновляется дважды в день: ~07:00 и 16:00 UTC.**

**Rate limit:** TBD  
**Важно:** передавайте только одно из полей `cluster_ids` **или** `macrolocal_cluster_ids` — не оба одновременно.

### Тело запроса

| Поле | Тип | Обязателен | Описание |
|---|---|---|---|
| `skus` | string[] (≤100) | да | Фильтр по SKU |
| `cluster_ids` | string[] | нет | Фильтр по кластерам (взаимоисключает с `macrolocal_cluster_ids`) |
| `macrolocal_cluster_ids` | string[] | нет | Фильтр по макролокальным кластерам |
| `warehouse_ids` | string[] | нет | Фильтр по складам |
| `item_tags` | string[] | нет | `ITEM_ATTRIBUTE_NONE` \| `ECONOM` \| `NOVEL` \| `DISCOUNT` \| `FBS_RETURN` \| `SUPER` |
| `turnover_grades` | string[] | нет | См. enum ниже |

**turnover_grade enum:** `DEFICIT` \| `POPULAR` \| `ACTUAL` \| `SURPLUS` \| `NO_SALES` \| `WAS_NO_SALES` \| `RESTRICTED_NO_SALES` \| `COLLECTING_DATA` \| `WAITING_FOR_SUPPLY` \| `WAS_DEFICIT` \| `WAS_POPULAR` \| `WAS_ACTUAL` \| `WAS_SURPLUS`

### Ответ (ключевые поля на единицу товара × кластер)

```json
{
  "items": [
    {
      "sku": 0,
      "offer_id": "string",
      "name": "string",
      "warehouse_id": 0,
      "warehouse_name": "string",
      "cluster_id": 0,
      "cluster_name": "string",
      "macrolocal_cluster_id": 0,
      "available_stock_count": 0,
      "valid_stock_count": 0,
      "transit_stock_count": 0,
      "requested_stock_count": 0,
      "excess_stock_count": 0,
      "expiring_stock_count": 0,
      "stock_defect_stock_count": 0,
      "transit_defect_stock_count": 0,
      "return_from_customer_stock_count": 0,
      "return_to_seller_stock_count": 0,
      "other_stock_count": 0,
      "waiting_docs_stock_count": 0,
      "ads": 0.0,
      "ads_cluster": 0.0,
      "idc": 0.0,
      "idc_cluster": 0.0,
      "days_without_sales": 0,
      "days_without_sales_cluster": 0,
      "turnover_grade": "UNSPECIFIED",
      "turnover_grade_cluster": "UNSPECIFIED",
      "item_tags": []
    }
  ]
}
```
