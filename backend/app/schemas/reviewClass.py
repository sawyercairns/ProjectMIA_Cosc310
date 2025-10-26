from datetime import date

class Review: 
    def __init__(self, review_id: int, user_id: int, product_id: int, created_at: date, price: float, rating: float, likes: int, title: str, body: str):
        #since this is a data class, we likely don't need to initialise any of these values
        self.review_id = review_id
        self.user_id = user_id
        self.product_id = product_id
        self.created_at = created_at
        self.price = price
        self.rating = rating
        self.likes = likes
        self.title = title
        self.body = body
    
    def update_title(self, _new_title: str):
        self.title = _new_title

    def update_body(self, _new_body: str):
        self.body = _new_body
    
    def update_rating(self, _new_rating: float):
        self.rating = _new_rating
    
    def update_likes(self, amount: int):
        self.likes += amount
    
