from datetime import datetime, timedelta
from app.services.orderInteractor import get_orders_all

def get_popular_products():
    orders_by_user = get_orders_all()
    ordered_products = {}
    
    for user_id in orders_by_user:
        for order in orders_by_user[user_id]:
            order_date = datetime.fromisoformat(order["order_date"])
            if order_date > datetime.now() - timedelta(weeks=1):
                for item in order["order_items"]:
                    product_name = item["product_name"]
                    if product_name not in ordered_products:
                        ordered_products[product_name] = 0
                    ordered_products[product_name] += 1
    
    top_3_items = sorted(ordered_products.items(), key=lambda item: item[1], reverse=True)[:3]
    return top_3_items
