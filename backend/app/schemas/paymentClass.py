
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
        
        if not card_number.isdigit():
            raise ValueError("Card number must contain only digits.")
  
        if not CVV.isdigit():
            raise ValueError("CVV must contain only digits.")
        
        if len(card_number) < 13 or len(card_number) > 19:
            raise ValueError("Card number must be between 13 and 19 digits.")
        
        if len(CVV) not in [3, 4]:
            raise ValueError("CVV must be 3 or 4 digits.")
        
        if '/' not in expiration_date:
            raise ValueError("Expiration date must be in MM/YY format.")
        
        parts = expiration_date.split('/')
        if len(parts) != 2:
            raise ValueError("Expiration date must be in MM/YY format.")
        
        month, year = parts
        
        if not month.isdigit() or not year.isdigit():
            raise ValueError("Month and year must be numeric.")
        
        if len(month) != 2 or int(month) < 1 or int(month) > 12:
            raise ValueError("Month must be between 01 and 12.")
        
        if len(year) != 2:
            raise ValueError("Year must be 2 digits (YY).")
        
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