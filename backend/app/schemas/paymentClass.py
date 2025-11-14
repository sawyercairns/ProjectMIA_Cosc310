
class Payment:

    def __init__(self, 
                 user_id: str, 
                 card_number: str, 
                 CVV: str, 
                 expiration_date: str):
        self._user_id = user_id
        self._card_number = card_number
        self._CVV = CVV
        self._expiration_date = expiration_date

    @property
    def user_id(self):
        return self._user_id

    @property
    def card_number(self):
        return self._card_number
    
    @property
    def CVV(self):
        return self._CVV
    
    @property
    def expiration_date(self):
        return self._expiration_date
    
    def update_payment_info(self, card_number: str, CVV: str, expiration_date: str):
        """Update payment info — all three fields are required."""
        if not all([card_number, CVV, expiration_date]):
            raise ValueError("All fields (card_number, CVV, expiration_date) are required.")
        self._card_number = card_number
        self._CVV = CVV
        self._expiration_date = expiration_date    

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "card_number": self.card_number,
            "CVV": self.CVV,
            "expiration_date": self.expiration_date
        }