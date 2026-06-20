# POST /v1/finance/realization/posting
# Rate limit: TBD
# Per-order realization report with posting_number and document details.
# Available from current date back to August 2023 only.
# Usage: python finance_realization_posting.py --month 5 --year 2025

import argparse
import json
import sys
from init import get_session, BASE_URL


def main():
    parser = argparse.ArgumentParser(description="Позаказный отчёт о реализации товаров (до авг. 2023)")
    parser.add_argument("--month", type=int, required=True, help="Месяц (1–12)")
    parser.add_argument("--year", type=int, required=True, help="Год")
    args = parser.parse_args()

    session = get_session()
    response = session.post(
        f"{BASE_URL}/v1/finance/realization/posting",
        json={"month": args.month, "year": args.year},
    )
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
