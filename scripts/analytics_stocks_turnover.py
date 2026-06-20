# POST /v1/analytics/turnover/stocks
# Rate limit: 1 запрос в минуту на Client-Id
# Stock turnover: avg daily sales (60d), days of stock remaining, turnover grade.
# Usage: python analytics_stocks_turnover.py [--limit N] [--offset N] [--sku SKU1 SKU2 ...]

import argparse
import json
import sys
from init import get_session, BASE_URL


def main():
    parser = argparse.ArgumentParser(description="Оборачиваемость товаров")
    parser.add_argument("--limit", type=int, help="Строк в ответе (1–1000)")
    parser.add_argument("--offset", type=int, help="Сколько строк пропустить")
    parser.add_argument("--sku", nargs="+", help="Фильтр по SKU")
    args = parser.parse_args()

    body = {}
    if args.limit is not None:
        body["limit"] = args.limit
    if args.offset is not None:
        body["offset"] = args.offset
    if args.sku:
        body["sku"] = args.sku

    session = get_session()
    response = session.post(f"{BASE_URL}/v1/analytics/turnover/stocks", json=body)
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
