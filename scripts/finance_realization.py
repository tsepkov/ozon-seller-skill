# POST /v2/finance/realization
# Rate limit: TBD
# Monthly realization report: delivered and returned items. Excludes cancellations and non-pickups.
# Available by the 5th of the following month.
# Usage: python finance_realization.py --month 5 --year 2025

import argparse
import json
import sys
from init import get_session, BASE_URL


def main():
    parser = argparse.ArgumentParser(description="Отчёт о реализации товаров за месяц")
    parser.add_argument("--month", type=int, required=True, help="Месяц (1–12)")
    parser.add_argument("--year", type=int, required=True, help="Год")
    args = parser.parse_args()

    session = get_session()
    response = session.post(
        f"{BASE_URL}/v2/finance/realization",
        json={"month": args.month, "year": args.year},
    )
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
