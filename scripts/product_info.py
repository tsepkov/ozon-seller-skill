# POST /v3/product/info/list
# Rate limit: TBD
# Detailed product info: commissions, status, visibility, errors, stocks, price indexes.
# Pass exactly one type of identifier. Up to 1000 per request.
# Usage: python product_info.py --offer-id "Loft 2 b" "Loft 1 mini b"
#        python product_info.py --sku 3880823891 3880823899
#        python product_info.py --product-id 223681945

import argparse
import json
import sys
from init import get_session, BASE_URL


def main():
    parser = argparse.ArgumentParser(description="Детальная информация о товарах")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--offer-id", nargs="+", metavar="ID")
    group.add_argument("--sku", nargs="+", metavar="SKU")
    group.add_argument("--product-id", nargs="+", metavar="ID")
    args = parser.parse_args()

    if args.offer_id:
        body = {"offer_id": args.offer_id}
    elif args.sku:
        body = {"sku": args.sku}
    else:
        body = {"product_id": args.product_id}

    session = get_session()
    r = session.post(f"{BASE_URL}/v3/product/info/list", json=body)
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
