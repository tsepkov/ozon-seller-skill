# POST /v2/review/count
# Rate limit: TBD
# Review counts by status: new / viewed / processed / total.
# Usage: python review_count.py

import json
import sys
from init import get_session, BASE_URL


def main():
    session = get_session()
    r = session.post(f"{BASE_URL}/v2/review/count", json={})
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
