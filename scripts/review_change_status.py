# POST /v2/review/change-status
# Rate limit: TBD
# Mark reviews as viewed or processed. Up to 100 IDs per request.
# Usage: python review_change_status.py --status PROCESSED --id ID1 ID2 ...

import argparse
import json
import sys
from init import get_session, BASE_URL


def main():
    parser = argparse.ArgumentParser(description="Изменить статус отзывов")
    parser.add_argument("--status", required=True, choices=["NEW", "VIEWED", "PROCESSED"])
    parser.add_argument("--id", nargs="+", required=True, metavar="REVIEW_ID", help="До 100 ID отзывов")
    args = parser.parse_args()

    session = get_session()
    r = session.post(
        f"{BASE_URL}/v2/review/change-status",
        json={"review_ids": args.id, "status": args.status},
    )
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps({"ok": True, "status": args.status, "count": len(args.id)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
