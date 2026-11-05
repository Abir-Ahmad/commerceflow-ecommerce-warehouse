"""Independent CSV/Decimal reconciliation, without copying model SQL."""
import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import duckdb
from catalog import TABLES

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    def rows(key):
        with (args.input / (TABLES[key] + '.csv')).open(encoding='utf-8-sig', newline='') as f:
            return list(csv.DictReader(f))
    orders, items, payments = rows('orders'), rows('items'), rows('payments')
    total = sum((Decimal(r['price']) for r in items), Decimal(0))
    payment_total = sum((Decimal(r['payment_value']) for r in payments), Decimal(0))
    observed = [o for o in orders if o['order_delivered_customer_date'] and o['order_estimated_delivery_date']]
    late = sum(o['order_delivered_customer_date'][:10] > o['order_estimated_delivery_date'][:10] for o in observed)
    high_freight = sum(Decimal(i['freight_value']) / (Decimal(i['price'])+Decimal(i['freight_value'])) > Decimal('.30') for i in items if Decimal(i['price'])+Decimal(i['freight_value']) > 0)
    c = duckdb.connect(os.environ.get('COMMERCEFLOW_DB','data/commerceflow.duckdb'), read_only=True)
    def scalar(sql):return c.execute(sql).fetchone()[0]
    def equal(actual,expected,label):
        if actual != expected:raise AssertionError(f'{label}: {actual} != {expected}')
    equal(scalar('select count(*) from analytics.fct_orders'),len(orders),'order count')
    equal(scalar('select count(*) from analytics.fct_order_items'),len(items),'item count')
    equal(scalar('select sum(merchandise_value) from analytics.fct_orders'),total,'merchandise')
    equal(scalar('select sum(payment_value) from analytics.fct_orders'),payment_total,'payments')
    equal(scalar("select count(*) from analytics.fct_orders where delivery_band <> 'not_observed'"),len(observed),'observed deliveries')
    equal(scalar("select count(*) from analytics.fct_orders where delivery_band not in ('not_observed','on_time')"),late,'late deliveries')
    equal(scalar('select sum(high_freight_items) from analytics.mart_category_freight'),high_freight,'high freight')
    result = json.loads(Path('target/run_results.json').read_text())
    statuses = {}
    for r in result['results']:statuses[r['status']] = statuses.get(r['status'],0)+1
    report = {'generated_at_utc':datetime.now(timezone.utc).isoformat(), 'target':'DuckDB local; BigQuery execution NOT verified',
      'source_rows':{k:len(rows(k)) for k in TABLES},
      'sha256':{k:hashlib.sha256((args.input/(t+'.csv')).read_bytes()).hexdigest() for k,t in TABLES.items()},
      'orders':len(orders),'items':len(items),'ordered_merchandise_brl':str(total),'payments_brl':str(payment_total),
      'legacy_timestamp_late_deliveries':sum(o['order_delivered_customer_date'] > o['order_estimated_delivery_date'] for o in observed),
      'observed_deliveries':len(observed),'late_deliveries':late,'on_time_deliveries':len(observed)-late,
      'on_time_rate':(len(observed)-late)/len(observed) if observed else None,
      'high_freight_items':high_freight,'independent_reconciliations_passed':7,'dbt_status_counts':statuses,
      'delivery_mart':[dict(zip(['band','orders','avg_order_review_score','avg_delivery_days'],r)) for r in c.execute('select * from analytics.mart_delivery order by delivery_band').fetchall()],
      'monthly_revenue':[dict(zip(['month','orders','delivered_orders','ordered_merchandise','delivered_merchandise','freight','payments'],r)) for r in c.execute('select * from analytics.mart_monthly_revenue order by purchase_month').fetchall()]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,default=str)+'\n')
    print('PASS: 7 independent CSV reconciliations; evidence:',args.output)
if __name__ == '__main__':main()
