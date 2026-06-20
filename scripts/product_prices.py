# POST /v5/product/info/prices
# Rate limit: TBD
# Prices, commissions (FBO/FBS %), and price index (GREEN/YELLOW/RED) per product.
# Cursor pagination — auto-fetches all pages by default.
# Usage: python product_prices.py [--visibility ALL] [--offer-id ID ...] [--product-id ID ...]

import argparse
import json
import sys
from init import get_session, BASE_URL

VISIBILITY = ["ALL", "VISIBLE", "INVISIBLE", "EMPTY_STOCK", "NOT_MODERATED", "MODERATED",
              "DISABLED", "BANNED", "OVERPRICED", "IN_SALE", "REMOVED_FROM_SALE"]


def main():
    parser = argparse.ArgumentParser(description="Цены и прайс-индексы товаров")
    parser.add_argument("--visibility", default="ALL", choices=VISIBILITY)
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--offer-id", nargs="+", metavar="ID")
    parser.add_argument("--product-id", nargs="+", metavar="ID")
    parser.add_argument("--no-paginate", action="store_true", help="Вернуть только первую страницу")
    args = parser.parse_args()

    filter_body = {"visibility": args.visibility}
    if args.offer_id:
        filter_body["offer_id"] = args.offer_id
    if args.product_id:
        filter_body["product_id"] = args.product_id

    session = get_session()
    items, cursor = [], ""

    while True:
        body = {"cursor": cursor, "filter": filter_body, "limit": args.limit}
        r = session.post(f"{BASE_URL}/v5/product/info/prices", json=body)
        if not r.ok:
            print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
            sys.exit(1)
        data = r.json()
        batch = data.get("items", [])
        items.extend(batch)
        cursor = data.get("cursor", "")
        if args.no_paginate or len(batch) < args.limit or not cursor:
            break

    print(json.dumps({"items": items, "total": len(items)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
