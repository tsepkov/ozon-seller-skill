# POST /v1/rating/summary
# Rate limit: TBD
# Current seller ratings across all quality indicators.
# Usage: python rating_summary.py

import json
import sys
from init import get_session, BASE_URL


def main():
    session = get_session()
    r = session.post(f"{BASE_URL}/v1/rating/summary", json={})
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
