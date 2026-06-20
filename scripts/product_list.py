# POST /v3/product/list
# Rate limit: TBD
# List all products with cursor pagination via last_id.
# Usage: python product_list.py [--visibility ALL] [--limit 1000] [--offer-id ID ...] [--product-id ID ...]

import argparse
import json
import sys
from init import get_session, BASE_URL

VISIBILITY = ["ALL", "VISIBLE", "INVISIBLE", "EMPTY_STOCK", "NOT_MODERATED", "MODERATED",
              "DISABLED", "BANNED", "OVERPRICED", "IN_SALE", "REMOVED_FROM_SALE"]


def fetch_all(session, filter_body, limit):
    items, last_id = [], ""
    while True:
        body = {"filter": filter_body, "limit": limit, "last_id": last_id}
        r = session.post(f"{BASE_URL}/v3/product/list", json=body)
        if not r.ok:
            print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
            sys.exit(1)
        result = r.json()["result"]
        batch = result.get("items", [])
        items.extend(batch)
        last_id = result.get("last_id", "")
        if len(batch) < limit or not last_id:
            break
    return items


def main():
    parser = argparse.ArgumentParser(description="Список всех товаров")
    parser.add_argument("--visibility", default="ALL", choices=VISIBILITY)
    parser.add_argument("--limit", type=int, default=1000, help="Строк на страницу (макс. 1000)")
    parser.add_argument("--offer-id", nargs="+", metavar="ID", help="Фильтр по артикулам (до 1000, без пагинации)")
    parser.add_argument("--product-id", nargs="+", metavar="ID", help="Фильтр по product_id (до 1000, без пагинации)")
    parser.add_argument("--no-paginate", action="store_true", help="Вернуть только первую страницу")
    args = parser.parse_args()

    filter_body = {"visibility": args.visibility}
    if args.offer_id:
        filter_body["offer_id"] = args.offer_id
    if args.product_id:
        filter_body["product_id"] = args.product_id

    session = get_session()

    if args.no_paginate or args.offer_id or args.product_id:
        body = {"filter": filter_body, "limit": args.limit, "last_id": ""}
        r = session.post(f"{BASE_URL}/v3/product/list", json=body)
        if not r.ok:
            print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))
    else:
        items = fetch_all(session, filter_body, args.limit)
        print(json.dumps({"result": {"items": items, "total": len(items)}}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
