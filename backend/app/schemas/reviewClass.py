from datetime import date

class Review: 
    def __init__(self, review_id: int, user_id: int, product_id: int, created_at: date, rating: float, likes: int, title: str, body: str):
        #since this is a data class, we likely don't need to initialise any of these values
        self._review_id = review_id
        self._user_id = user_id
        self._product_id = product_id
        self._created_at = created_at
        self._rating = rating
        self._likes = likes
        self._title = title
        self._body = body
        

    @property
    def review_id(self):
        return self._review_id
    
    @review_id.setter
    def review_id(self, id:int):
        self._review_id = id

    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, id:int):
        self._user_id = id

    @property
    def product_id(self):
        return self._product_id
    
    @product_id.setter
    def product_id(self, id:int):
        self._product_id = id

    @property
    def created_at(self):
        return self._created_at
    
    @created_at.setter
    def created_at(self, date:date):
        self._created_at = date

    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, rating:float):
        self._rating = rating

    @property
    def likes(self):
        return self._likes
    
    @likes.setter
    def likes(self, likes:int):
        self._likes = likes

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def body(self):
        return self._body
    
    @body.setter
    def body(self, body:str):
        self._body = body

    #Leaving this, as it is distinct from the getters 
    #and setters in that it changes likes by an amount.
    def update_likes(self, amount: int):
        self.likes += amount
    
