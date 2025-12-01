from datetime import datetime, timedelta
from app.services.orderInteractor import get_orders_all

#Returns the top 3 products by sales in a given week
def get_popular_products():
    orders = get_orders_all()
    ordered_products = {}
    for order in orders:
        if orders[order]["order_date"] > datetime.now() - timedelta(weeks = 1):
            for item in orders[order]["order_items"]:
                if item.product_name not in ordered_products:
                    ordered_products[item.product_name] = 0
                ordered_products[item.product_name] += 1
    top_3_items = sorted(ordered_products.items(), key=lambda item: item[1], reverse=True)[:3]
    return top_3_items
