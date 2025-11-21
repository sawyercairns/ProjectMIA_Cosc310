# Function to calculate the star review of a product based on user ratings
# Input product_id and return integer star review.

from app.services.reviewInteractor import get_product_reviews


def calculate_star_review(product_id: int) -> int:
    reviews = get_product_reviews(product_id)
    if not reviews:
        return 0  

    total_rating = sum(review["rating"] for review in reviews)
    average_rating = total_rating / len(reviews)
    
    return round(average_rating)