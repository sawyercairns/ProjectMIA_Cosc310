import decimal
from typing import List

from app.schemas.yearInReviewClass import YearInReview
from app.schemas.orderClass import Order
from app.services.orderInteractor import load_orders
from app.services.reviewInteractor import get_reviews


def get_year_in_review(user_id: str, year: int) -> YearInReview:
    all_orders = load_orders(user_id)
    year_orders = _filter_orders_by_year(all_orders, year)
    
    all_reviews = get_reviews(int(user_id))
    year_reviews = _filter_reviews_by_year(all_reviews, year)
    
    total_spent = _calculate_total_spent(year_orders)
    total_orders = len(year_orders)
    avg_order_amount = _calculate_avg_order_amount(total_spent, total_orders)
    items_purchased = _calculate_items_purchased(year_orders)
    biggest_order = _find_biggest_order(year_orders)
    orders_returned = _count_returned_orders(year_orders)
    
    reviews_written = len(year_reviews)
    likes_received = _calculate_likes_received(year_reviews)
    
    return YearInReview(
        user_id=int(user_id),
        year=year,
        total_spent=total_spent,
        total_orders=total_orders,
        avg_order_amount=avg_order_amount,
        items_purchased=items_purchased,
        reviews_written=reviews_written,
        likes_received=likes_received,
        biggest_order=biggest_order,
        orders_returned=orders_returned
    )


def _filter_orders_by_year(orders: List[Order], year: int) -> List[Order]:
    year_str = str(year)
    return [o for o in orders if o.order_date and o.order_date.startswith(year_str)]


def _filter_reviews_by_year(reviews: List[dict], year: int) -> List[dict]:
    year_str = str(year)
    return [r for r in reviews if str(r.get("created_at", "")).startswith(year_str)]


def _calculate_total_spent(orders: List[Order]) -> decimal.Decimal:
    total = decimal.Decimal("0.00")
    for order in orders:
        total += order.calculate_total_price()
    return total


def _calculate_avg_order_amount(total_spent: decimal.Decimal, total_orders: int) -> decimal.Decimal:
    if total_orders == 0:
        return decimal.Decimal("0.00")
    return (total_spent / total_orders).quantize(decimal.Decimal("0.01"))


def _calculate_items_purchased(orders: List[Order]) -> int:
    total_items = 0
    for order in orders:
        for item in order.order_items:
            total_items += item.quantity
    return total_items


def _find_biggest_order(orders: List[Order]) -> decimal.Decimal:
    if not orders:
        return decimal.Decimal("0.00")
    
    max_total = decimal.Decimal("0.00")
    for order in orders:
        order_total = order.calculate_total_price()
        if order_total > max_total:
            max_total = order_total
    return max_total


def _count_returned_orders(orders: List[Order]) -> int:
    return sum(1 for order in orders if order.returned)


def _calculate_likes_received(reviews: List[dict]) -> int:
    return sum(r.get("likes", 0) for r in reviews)
