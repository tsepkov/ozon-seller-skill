# POST /v1/product/rating-by-sku
# Rate limit: TBD
# Content rating (0-100) per product with per-group breakdown and improvement hints.
# Usage: python product_content_rating.py --sku 3880823891 3880823899

import argparse
import json
import sys
from init import get_session, BASE_URL


def main():
    parser = argparse.ArgumentParser(description="Контент-рейтинг карточек товаров")
    parser.add_argument("--sku", nargs="+", required=True, metavar="SKU")
    args = parser.parse_args()

    session = get_session()
    r = session.post(f"{BASE_URL}/v1/product/rating-by-sku", json={"skus": args.sku})
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
