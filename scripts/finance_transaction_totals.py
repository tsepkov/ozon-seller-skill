# POST /v3/finance/transaction/totals
# Rate limit: TBD
# Aggregated transaction totals for a period. Wrong posting_number returns zeros.
# Usage: python finance_transaction_totals.py --from 2025-05-01 --to 2025-05-31 [--type all]
#        python finance_transaction_totals.py --posting-number 1234567890

import argparse
import json
import sys
from init import get_session, BASE_URL

TRANSACTION_TYPES = ["all", "orders", "returns", "services", "compensation", "transferDelivery", "other"]


def main():
    parser = argparse.ArgumentParser(description="Итоговые суммы транзакций за период")
    filter_group = parser.add_mutually_exclusive_group(required=True)
    filter_group.add_argument("--from", dest="date_from", metavar="DATE", help="Начало периода (YYYY-MM-DD)")
    filter_group.add_argument("--posting-number", metavar="NUMBER", help="Номер отправления")
    parser.add_argument("--to", dest="date_to", metavar="DATE", help="Конец периода (YYYY-MM-DD), обязателен с --from")
    parser.add_argument("--type", dest="transaction_type", default="all", choices=TRANSACTION_TYPES, help="Тип транзакции")
    args = parser.parse_args()

    if args.date_from and not args.date_to:
        parser.error("--to обязателен при использовании --from")

    if args.date_from:
        body = {
            "date": {
                "from": f"{args.date_from}T00:00:00.000Z",
                "to": f"{args.date_to}T23:59:59.000Z",
            },
            "posting_number": "",
            "transaction_type": args.transaction_type,
        }
    else:
        body = {
            "posting_number": args.posting_number,
            "transaction_type": args.transaction_type,
        }

    session = get_session()
    response = session.post(f"{BASE_URL}/v3/finance/transaction/totals", json=body)
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
