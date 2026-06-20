# POST /v2/review/info
# Rate limit: TBD
# Full review details including photos and videos.
# Usage: python review_info.py --id 017c0d1c-66d3-b838-3d29-cf9b95a6ac48

import argparse
import json
import sys
from init import get_session, BASE_URL


def main():
    parser = argparse.ArgumentParser(description="Детальная информация по отзыву")
    parser.add_argument("--id", required=True, metavar="REVIEW_ID")
    args = parser.parse_args()

    session = get_session()
    r = session.post(f"{BASE_URL}/v2/review/info", json={"review_id": args.id})
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
