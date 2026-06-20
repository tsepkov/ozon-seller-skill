# POST /v4/product/info/limit
# Rate limit: TBD
# Assortment limits: total SKU cap, daily create/update quotas, per-minute operation limit.
# Usage: python product_quota.py

import json
import sys
from init import get_session, BASE_URL


def main():
    session = get_session()
    r = session.post(f"{BASE_URL}/v4/product/info/limit", json={})
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
