"""Synthetic edge cases, no customer data or external download needed for CI."""
import csv
from pathlib import Path
from catalog import TABLES

def main():
    out = Path('data/fixture')
    out.mkdir(parents=True, exist_ok=True)
    data = {
      'orders': [
        ['o1','c1','delivered','2018-01-01 10:00:00','','','2018-01-03 12:00:00','2018-01-03 00:00:00'],
        ['o2','c2','delivered','2018-01-02 10:00:00','','','2018-01-06 00:00:00','2018-01-04 00:00:00'],
        ['o3','c3','canceled','2018-02-01 10:00:00','','','','2018-02-08 00:00:00'],
        ['o4','c4','delivered','2018-02-02 10:00:00','','','2018-02-15 00:00:00','2018-02-07 00:00:00']],
      'customers':[['c'+str(i),'person'+str(i),'SP','city'] for i in range(1,5)],
      'sellers':[['s1','SP','city']],
      'products':[['p1','known','100'],['p2','untranslated','200'],['p3','','']],
      'categories':[['known','known_english']],
      'items':[['o1','1','p1','s1','100','10'],['o1','2','p2','s1','50','30'],['o2','1','p3','s1','20','0'],['o4','1','p1','s1','30','5']],
      'payments':[['o1','1','credit_card','100'],['o1','2','voucher','90'],['o2','1','credit_card','20'],['o4','1','credit_card','35']],
      'reviews':[['r1','o1','5'],['r2','o1','3'],['r3','o2','2'],['r4','o4','1']]}
    headers = {
      'orders':'order_id customer_id order_status order_purchase_timestamp order_approved_at order_delivered_carrier_date order_delivered_customer_date order_estimated_delivery_date',
      'customers':'customer_id customer_unique_id customer_state customer_city',
      'sellers':'seller_id seller_state seller_city',
      'products':'product_id product_category_name product_weight_g',
      'categories':'product_category_name product_category_name_english',
      'items':'order_id order_item_id product_id seller_id price freight_value',
      'payments':'order_id payment_sequential payment_type payment_value',
      'reviews':'review_id order_id review_score'}
    for key, values in data.items():
        with (out/(TABLES[key]+'.csv')).open('w', newline='') as f:
            writer=csv.writer(f);writer.writerow(headers[key].split());writer.writerows(values)
    print(out)
if __name__ == '__main__':main()
