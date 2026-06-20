# POST /v1/rating/history
# Rate limit: TBD
# Seller rating history for a given date range and set of rating indicators.
# Usage: python rating_history.py --from 2026-01-01 --to 2026-06-20
#        python rating_history.py --from 2026-01-01 --to 2026-06-20 --ratings rating_on_time rating_review_avg_score_total

import argparse
import json
import sys
from init import get_session, BASE_URL

ALL_RATINGS = [
    "rating_on_time",
    "rating_review_avg_score_total",
    "rating_ssl",
    "rating_on_time_supply_delivery",
    "rating_order_accuracy",
    "rating_on_time_supply_cancellation",
    "rating_reaction_time",
    "rating_average_response_time",
    "rating_replied_dialogs_ratio",
    "rating_price_green",
    "rating_price_yellow",
    "rating_price_red",
    "rating_price_super",
]


def main():
    parser = argparse.ArgumentParser(description="История рейтингов продавца за период")
    parser.add_argument("--from", dest="date_from", required=True, metavar="DATE", help="Начало периода (YYYY-MM-DD)")
    parser.add_argument("--to", dest="date_to", required=True, metavar="DATE", help="Конец периода (YYYY-MM-DD)")
    parser.add_argument(
        "--ratings",
        nargs="+",
        default=ALL_RATINGS,
        metavar="RATING",
        help=f"Коды рейтингов. По умолчанию все: {', '.join(ALL_RATINGS)}",
    )
    parser.add_argument("--with-premium-scores", action="store_true", help="Включить штрафные баллы Premium")
    args = parser.parse_args()

    session = get_session()
    body = {
        "date_from": f"{args.date_from}T00:00:00Z",
        "date_to": f"{args.date_to}T23:59:59Z",
        "ratings": args.ratings,
        "with_premium_scores": args.with_premium_scores,
    }
    r = session.post(f"{BASE_URL}/v1/rating/history", json=body)
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
