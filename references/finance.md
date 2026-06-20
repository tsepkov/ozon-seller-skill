# FinanceAPI — Финансовые отчёты

Источник: `about.me.md` → tag/FinanceAPI

---

## POST /v2/finance/realization

Отчёт о реализации доставленных и возвращённых товаров за месяц.  
Отмены и невыкупы не включаются. Приходит не позднее 5-го числа следующего месяца.

**Rate limit:** TBD

### Тело запроса

| Поле | Тип | Обязателен | Описание |
|---|---|---|---|
| `month` | int32 | да | Месяц (1–12) |
| `year` | int32 | да | Год |

### Ответ

```json
{
  "result": {
    "header": {
      "number": "string",
      "doc_date": "string",
      "contract_number": "string",
      "contract_date": "string",
      "start_date": "string",
      "stop_date": "string",
      "currency_sys_name": "string",
      "payer_name": "string",
      "payer_inn": "string",
      "payer_kpp": "string",
      "receiver_name": "string",
      "receiver_inn": "string",
      "receiver_kpp": "string"
    },
    "rows": [
      {
        "rowNumber": 0,
        "item": { "sku": 0, "offer_id": "string", "name": "string", "barcode": "string" },
        "seller_price_per_instance": 0,
        "commission_ratio": 0,
        "delivery_commission": {
          "quantity": 0, "price_per_instance": 0, "amount": 0,
          "commission": 0, "standard_fee": 0, "compensation": 0,
          "bonus": 0, "bank_coinvestment": 0, "stars": 0,
          "pick_up_point_coinvestment": 0, "total": 0
        },
        "return_commission": { "...": "аналогичная структура" }
      }
    ]
  }
}
```

---

## POST /v1/finance/realization/posting

Позаказный отчёт о реализации — детализация по каждому заказу.  
Доступен с текущего момента **по август 2023 включительно**.

**Rate limit:** TBD

### Тело запроса

| Поле | Тип | Обязателен | Описание |
|---|---|---|---|
| `month` | int32 | да | Месяц (1–12) |
| `year` | int32 | да | Год |

### Ответ

Аналогично `/v2/finance/realization`, но каждая строка содержит дополнительно:

```json
{
  "order": { "posting_number": "string", "created_date": "string" },
  "legal_entity_document": { "number": "string", "sale_date": "string" }
}
```

---

## POST /v3/finance/transaction/list

Подробная информация по всем начислениям.  
Максимальный период одного запроса — **1 месяц**.  
Пагинация: `page` + `page_size` (≤1000).

**Rate limit:** TBD

### Тело запроса

```json
{
  "filter": {
    "date": { "from": "2021-11-01T00:00:00.000Z", "to": "2021-11-30T23:59:59.000Z" },
    "posting_number": "",
    "operation_type": [],
    "transaction_type": "all"
  },
  "page": 1,
  "page_size": 1000
}
```

| Поле | Обязателен | Описание |
|---|---|---|
| `filter` | да | `date` или `posting_number` |
| `filter.transaction_type` | нет | `all` \| `orders` \| `returns` \| `services` \| `compensation` \| `transferDelivery` \| `other` |
| `page` | да | Номер страницы |
| `page_size` | да | Строк на странице (≤1000) |

### Ответ

```json
{
  "result": {
    "page_count": 1,
    "row_count": 355,
    "operations": [
      {
        "operation_id": 11401182187840,
        "operation_type": "MarketplaceMarketingActionCostOperation",
        "operation_type_name": "Услуги продвижения товаров",
        "operation_date": "2021-11-01 00:00:00",
        "type": "services",
        "amount": -6.46,
        "accruals_for_sale": 0,
        "sale_commission": 0,
        "delivery_charge": 0,
        "return_delivery_charge": 0,
        "posting": { "posting_number": "", "delivery_schema": "", "order_date": "", "warehouse_id": 0 },
        "items": [],
        "services": []
      }
    ]
  }
}
```

---

## POST /v3/finance/transaction/totals

Итоговые суммы по транзакциям за период.

**Rate limit:** TBD  
**Примечание:** при неверных `posting_number` вернутся нули.

### Тело запроса

```json
{
  "date": { "from": "2021-11-01T00:00:00.000Z", "to": "2021-11-30T23:59:59.000Z" },
  "posting_number": "",
  "transaction_type": "all"
}
```

`transaction_type`: `all` | `orders` | `returns` | `services` | `compensation` | `transferDelivery` | `other`

### Ответ

```json
{
  "result": {
    "accruals_for_sale": 96647.58,
    "sale_commission": -11456.65,
    "processing_and_delivery": -24405.68,
    "refunds_and_cancellations": -330.0,
    "services_amount": -1307.57,
    "compensation_amount": 0.0,
    "money_transfer": 0.0,
    "others_amount": 113.05
  }
}
```
