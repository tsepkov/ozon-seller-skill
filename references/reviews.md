# ReviewAPI — Работа с отзывами

Источник: `about.me.md` → tag/ReviewAPI  
Deprecated v1-методы пропущены. Используем только v2.

---

## POST /v2/review/count

Количество отзывов по статусам. Тело запроса пустое.

**Rate limit:** TBD

### Ответ

```json
{ "total": 3, "new": 1, "viewed": 1, "processed": 1 }
```

---

## POST /v2/review/list

Список отзывов с фильтрами и cursor-пагинацией (`last_id`).  
Лимит: 20–100 за запрос.

**Rate limit:** TBD

### Тело запроса

```json
{
  "filters": {
    "sku": [148591503],
    "order_status": "DELIVERED",
    "status": "NEW",
    "published_from": "2026-01-01T00:00:00Z",
    "published_to": "2026-06-20T23:59:59Z"
  },
  "last_id": "",
  "limit": 100,
  "sort_dir": "DESC"
}
```

| Поле | Описание |
|---|---|
| `filters.sku` | Фильтр по SKU товаров |
| `filters.status` | Статус отзыва: `NEW` \| `VIEWED` \| `PROCESSED` |
| `filters.order_status` | Статус заказа: `DELIVERED` \| `CANCELLED` |
| `filters.published_from/to` | Диапазон дат публикации |
| `sort_dir` | `ASC` \| `DESC` |
| `limit` | 20–100 |

### Ответ

```json
{
  "reviews": [
    {
      "id": "017c0d1c-66d3-b838-3d29-cf9b95a6ac48",
      "sku": "148591503",
      "text": "Не лучший товар, встречал и получше за те же деньги.",
      "published_at": "2024-10-10T07:23:55.970Z",
      "rating": 2,
      "status": "NEW",
      "order_status": "DELIVERED",
      "comments_amount": 0,
      "photos_amount": 0,
      "videos_amount": 0,
      "is_rating_participant": true
    }
  ],
  "has_next": true,
  "last_id": "017c0d53-a7c8-81ef-53de-7d32fcbd7421"
}
```

---

## POST /v2/review/info

Детальная информация по одному отзыву, включая фото и видео.

**Rate limit:** TBD

### Тело запроса

```json
{ "review_id": "017c0d1c-66d3-b838-3d29-cf9b95a6ac48" }
```

### Ответ

```json
{
  "id": "string",
  "sku": 0,
  "text": "string",
  "rating": 5,
  "status": "NEW",
  "order_status": "DELIVERED",
  "published_at": "2026-06-01T12:00:00Z",
  "is_rating_participant": true,
  "likes_amount": 0,
  "dislikes_amount": 0,
  "comments_amount": 0,
  "photos_amount": 0,
  "videos_amount": 0,
  "photos": [{ "url": "string", "width": 0, "height": 0 }],
  "videos": [{ "url": "string", "preview_url": "string", "width": 0, "height": 0 }]
}
```

---

## POST /v2/review/change-status

Пометить отзывы как просмотренные или обработанные. До 100 за раз.

**Rate limit:** TBD

### Тело запроса

```json
{
  "review_ids": ["017c0d1c-66d3-b838-3d29-cf9b95a6ac48"],
  "status": "PROCESSED"
}
```

`status`: `NEW` | `VIEWED` | `PROCESSED`  
Ответ: 200 без тела при успехе, иначе ошибка.
