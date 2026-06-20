# SellerInfo — Информация по кабинету продавца

Источник: `about.me.md` → tag/SellerInfo

---

## POST /v1/seller/info

Информация о кабинете продавца.

**Заголовки:** `Client-Id`, `Api-Key`  
**Тело запроса:** пустое `{}`  
**Rate limit:** TBD

### Ответ

```json
{
  "company": {
    "country": "Россия",
    "currency": "RUB",           // RUB | EUR | USD | CNY | BYN | KZT | KGS
    "inn": "7707083893",
    "legal_name": "ООО 'Ромашка'",
    "name": "ООО 'Ромашка'",
    "ogrn": "1027700132195",
    "ownership_form": "Частная собственность",
    "tax_system": "ОСНО"         // UNKNOWN | UNSPECIFIED | OSNO | USN | NPD | AUSN | PSN
  },
  "ratings": [
    {
      "name": "Финансовая устойчивость",
      "rating": "Высокий уровень",
      "status": "OK",            // UNKNOWN | OK | WARNING | CRITICAL
      "value_type": "INDEX",     // UNKNOWN | INDEX | PERCENT | TIME | RATIO | REVIEW_SCORE | COUNT
      "current_value": {
        "date_from": "2023-01-15T09:00:00Z",
        "date_to": "2023-12-31T23:59:59Z",
        "formatted": "AA+",
        "value": 85,
        "status": { "danger": false, "premium": true, "warning": false }
      },
      "past_value": { "..." : "аналогичная структура" }
    }
  ],
  "subscription": {
    "is_premium": true,
    "type": "PREMIUM"            // UNKNOWN | UNSPECIFIED | PREMIUM | PREMIUM_LITE | PREMIUM_PLUS | PREMIUM_PRO
  }
}
```

---

## POST /v1/seller/ozon-logistics/info

Статус подключения Ozon Доставки.

**Заголовки:** `Client-Id`, `Api-Key`  
**Тело запроса:** пустое `{}`  
**Rate limit:** TBD

### Ответ

```json
{
  "available_schemas": ["FBO"],  // UNKNOWN | FBO | FBS
  "ozon_logistics_enabled": true
}
```
