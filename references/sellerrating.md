# SellerRating — Рейтинг продавца

Источник: `about.me.md` → tag/SellerRating  
FBS-специфичные методы (`/rating/index/fbs/*`) пропущены.

---

## POST /v1/rating/summary

Текущие рейтинги продавца по всем показателям.  
Соответствует разделу «Рейтинги → Рейтинги продавца» в личном кабинете.

**Тело запроса:** `{}` (пустой объект)

**Rate limit:** TBD

### Ответ

```json
{
  "groups": [
    {
      "group_name": "string",
      "items": [
        {
          "name": "string",
          "current_value": 0,
          "past_value": 0,
          "rating": "string",
          "rating_direction": "string",
          "status": "string",
          "value_type": "string",
          "change": {
            "direction": "string",
            "meaning": "string"
          }
        }
      ]
    }
  ],
  "localization_index": [
    { "calculation_date": "2019-08-24T14:15:22Z", "localization_percentage": 0 }
  ],
  "penalty_score_exceeded": false,
  "premium": false,
  "premium_plus": false
}
```

---

## POST /v1/rating/history

История рейтингов за заданный период.

**Rate limit:** TBD  
**Ограничение:** диапазон не более ~30 дней (API возвращает 400 `too wide range` при большем интервале)

### Тело запроса

```json
{
  "date_from": "2026-01-01T00:00:00Z",
  "date_to": "2026-06-20T00:00:00Z",
  "ratings": ["rating_on_time", "rating_review_avg_score_total"],
  "with_premium_scores": false
}
```

| Поле | Описание |
|---|---|
| `date_from` | Начало периода (ISO 8601) |
| `date_to` | Конец периода (ISO 8601) |
| `ratings` | Список рейтингов для запроса (см. ниже) |
| `with_premium_scores` | Вернуть штрафные баллы Premium-программы |

### Доступные значения `ratings`

| Код | Описание |
|---|---|
| `rating_on_time` | % заказов выполненных вовремя (30 дней) |
| `rating_review_avg_score_total` | Средняя оценка всех товаров |
| `rating_ssl` | Сводная оценка FBO |
| `rating_on_time_supply_delivery` | % поставок в срок (60 дней) |
| `rating_order_accuracy` | % поставок без излишков/недостач/брака (60 дней) |
| `rating_on_time_supply_cancellation` | % заявок без опоздания (60 дней) |
| `rating_reaction_time` | Время первого ответа в чате (сек, 30 дней) |
| `rating_average_response_time` | Среднее время ответа (сек, 30 дней) |
| `rating_replied_dialogs_ratio` | Доля диалогов с ответом за 24ч (30 дней) |
| `rating_price_green` | % товаров с выгодным индексом цен |
| `rating_price_yellow` | % товаров с умеренным индексом цен |
| `rating_price_red` | % товаров с невыгодным индексом цен |
| `rating_price_super` | % товаров с супер-выгодным индексом цен |

### Ответ

```json
{
  "ratings": [
    {
      "rating": "rating_on_time",
      "danger_threshold": 0,
      "warning_threshold": 0,
      "premium_threshold": 0,
      "values": [
        {
          "date_from": "2026-01-01T00:00:00Z",
          "date_to": "2026-01-07T00:00:00Z",
          "value": 95.5,
          "status": { "danger": false, "warning": false, "premium": true }
        }
      ]
    }
  ],
  "premium_scores": []
}
```
