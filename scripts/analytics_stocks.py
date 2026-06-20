# POST /v1/analytics/stocks
# Rate limit: TBD
# Detailed stock analytics per warehouse/cluster. Updated twice daily ~07:00 and 16:00 UTC.
# Usage: python analytics_stocks.py --sku SKU1 SKU2 ... [--cluster-id ID ...] [--macrolocal-cluster-id ID ...]
#                                    [--warehouse-id ID ...] [--turnover-grade GRADE ...] [--item-tag TAG ...]
# Note: --cluster-id and --macrolocal-cluster-id are mutually exclusive.

import argparse
import json
import sys
from init import get_session, BASE_URL

TURNOVER_GRADES = [
    "TURNOVER_GRADE_NONE", "DEFICIT", "POPULAR", "ACTUAL", "SURPLUS",
    "NO_SALES", "WAS_NO_SALES", "RESTRICTED_NO_SALES", "COLLECTING_DATA",
    "WAITING_FOR_SUPPLY", "WAS_DEFICIT", "WAS_POPULAR", "WAS_ACTUAL", "WAS_SURPLUS",
]
ITEM_TAGS = ["ITEM_ATTRIBUTE_NONE", "ECONOM", "NOVEL", "DISCOUNT", "FBS_RETURN", "SUPER"]


def main():
    parser = argparse.ArgumentParser(description="Аналитика по остаткам на складах (FBO)")
    parser.add_argument("--sku", nargs="+", required=True, metavar="SKU", help="SKU товаров (до 100)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--cluster-id", nargs="+", metavar="ID", help="Идентификаторы кластеров")
    group.add_argument("--macrolocal-cluster-id", nargs="+", metavar="ID", help="Идентификаторы макролокальных кластеров")
    parser.add_argument("--warehouse-id", nargs="+", metavar="ID", help="Идентификаторы складов")
    parser.add_argument("--turnover-grade", nargs="+", choices=TURNOVER_GRADES, metavar="GRADE", help="Фильтр по статусу ликвидности")
    parser.add_argument("--item-tag", nargs="+", choices=ITEM_TAGS, metavar="TAG", help="Фильтр по тегам товара")
    args = parser.parse_args()

    body = {"skus": args.sku}
    if args.cluster_id:
        body["cluster_ids"] = args.cluster_id
    if args.macrolocal_cluster_id:
        body["macrolocal_cluster_ids"] = args.macrolocal_cluster_id
    if args.warehouse_id:
        body["warehouse_ids"] = args.warehouse_id
    if args.turnover_grade:
        body["turnover_grades"] = args.turnover_grade
    if args.item_tag:
        body["item_tags"] = args.item_tag

    session = get_session()
    response = session.post(f"{BASE_URL}/v1/analytics/stocks", json=body)
    if not response.ok:
        print(f"Error {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
