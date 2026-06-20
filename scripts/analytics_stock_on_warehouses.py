# POST /v2/analytics/stock_on_warehouses
# Rate limit: TBD
# Stock report across Ozon warehouses with pagination.
# Usage: python analytics_stock_on_warehouses.py [--limit N] [--offset N] [--warehouse-type ALL|EXPRESS_DARK_STORE|NOT_EXPRESS_DARK_STORE]

import argparse
import json
import sys
from init import get_session, BASE_URL


def main():
    parser = argparse.ArgumentParser(description="Отчёт по остаткам и товарам на складах Ozon")
    parser.add_argument("--limit", type=int, default=100, help="Строк на странице (по умолчанию 100)")
    parser.add_argument("--offset", type=int, default=0, help="Сколько строк пропустить")
    parser.add_argument(
        "--warehouse-type",
        default="ALL",
        choices=["ALL", "EXPRESS_DARK_STORE", "NOT_EXPRESS_DARK_STORE"],
        help="Тип склада (по умолчанию ALL)",
    )
    args = parser.parse_args()

    session = get_session()
    response = session.post(
        f"{BASE_URL}/v2/analytics/stock_on_warehouses",
        json={"limit": args.limit, "offset": args.offset, "warehouse_type": args.warehouse_type},
    )
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
