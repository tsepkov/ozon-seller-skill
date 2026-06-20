# POST /v1/seller/ozon-logistics/info
# Rate limit: TBD
# Returns whether Ozon Delivery is connected and which schemas (FBO/FBS) are available.

import json
import sys
from init import get_session, BASE_URL


def main():
    session = get_session()
    response = session.post(f"{BASE_URL}/v1/seller/ozon-logistics/info", json={})
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
