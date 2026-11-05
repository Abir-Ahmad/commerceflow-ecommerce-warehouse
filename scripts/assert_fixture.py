"""Known expected answers detect join fan-out, null loss and deadline errors."""
import os
from decimal import Decimal
import duckdb
c=duckdb.connect(os.environ.get('COMMERCEFLOW_DB','data/commerceflow.duckdb'),read_only=True)
rows={r[0]:r[1:] for r in c.execute('select order_id,item_count,merchandise_value,payment_value,avg_review_score,delivery_band from analytics.fct_orders').fetchall()}
assert rows['o1'] == (2,Decimal('150.00'),Decimal('190.00'),4.0,'on_time'), rows
assert rows['o2'][-1] == '1_3_days_late'
assert rows['o3'] == (0,Decimal('0.00'),None,None,'not_observed')
assert rows['o4'][-1] == '8_plus_days_late'
assert c.execute("select category_english from analytics.dim_products where product_id='p2'").fetchone()[0] == 'untranslated'
assert c.execute("select category_english from analytics.dim_products where product_id='p3'").fetchone()[0] == 'unknown'
assert c.execute('select sum(ordered_merchandise_value) from analytics.mart_monthly_revenue').fetchone()[0] == Decimal('200.00')
print('PASS: synthetic edge cases (multi-item/payment/review, same-day delivery, missing item/payment/review, untranslated/null category).')
