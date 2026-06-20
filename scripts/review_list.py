# POST /v2/review/list
# Rate limit: TBD
# List reviews with filters and cursor pagination. Limit: 20-100 per request.
# Usage: python review_list.py [--sku SKU ...] [--status NEW|VIEWED|PROCESSED]
#                               [--order-status DELIVERED|CANCELLED]
#                               [--from DATE] [--to DATE] [--sort DESC|ASC]

import argparse
import json
import sys
from init import get_session, BASE_URL


def main():
    parser = argparse.ArgumentParser(description="Список отзывов")
    parser.add_argument("--sku", nargs="+", type=int, metavar="SKU", help="Фильтр по SKU")
    parser.add_argument("--status", choices=["NEW", "VIEWED", "PROCESSED"], help="Статус отзыва")
    parser.add_argument("--order-status", choices=["DELIVERED", "CANCELLED"], help="Статус заказа")
    parser.add_argument("--from", dest="date_from", metavar="DATE", help="Дата публикации от (YYYY-MM-DD)")
    parser.add_argument("--to", dest="date_to", metavar="DATE", help="Дата публикации до (YYYY-MM-DD)")
    parser.add_argument("--sort", default="DESC", choices=["ASC", "DESC"])
    parser.add_argument("--limit", type=int, default=100, help="Строк за запрос (20–100)")
    parser.add_argument("--no-paginate", action="store_true", help="Только первая страница")
    args = parser.parse_args()

    filters = {}
    if args.sku:
        filters["sku"] = args.sku
    if args.status:
        filters["status"] = args.status
    if args.order_status:
        filters["order_status"] = args.order_status
    if args.date_from:
        filters["published_from"] = f"{args.date_from}T00:00:00Z"
    if args.date_to:
        filters["published_to"] = f"{args.date_to}T23:59:59Z"

    session = get_session()
    reviews, last_id = [], ""

    while True:
        body = {"filters": filters, "last_id": last_id, "limit": args.limit, "sort_dir": args.sort}
        r = session.post(f"{BASE_URL}/v2/review/list", json=body)
        if not r.ok:
            print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
            sys.exit(1)
        data = r.json()
        reviews.extend(data.get("reviews", []))
        last_id = data.get("last_id", "")
        if args.no_paginate or not data.get("has_next"):
            break

    print(json.dumps({"reviews": reviews, "total": len(reviews)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
