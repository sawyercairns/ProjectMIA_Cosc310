class Address:
    """Address class to store delivery/profile address information"""
    
    def __init__(self,
                 line1: str,
                 line2: str = "",
                 city: str = "",
                 province: str = "",
                 country: str = ""):
        self.line1 = line1
        self.line2 = line2
        self.city = city
        self.province = province
        self.country = country
    
    @property
    def line1(self):
        return self._line1
    
    @line1.setter
    def line1(self, value: str):
        self._line1 = value
    
    @property
    def line2(self):
        return self._line2
    
    @line2.setter
    def line2(self, value: str):
        self._line2 = value
    
    @property
    def city(self):
        return self._city
    
    @city.setter
    def city(self, value: str):
        self._city = value
    
    @property
    def province(self):
        return self._province
    
    @province.setter
    def province(self, value: str):
        self._province = value
    
    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self, value: str):
        self._country = value
    
    def to_dict(self):
        """Convert address to dictionary for JSON serialization"""
        return {
            "line1": self.line1,
            "line2": self.line2,
            "city": self.city,
            "province": self.province,
            "country": self.country
        }
