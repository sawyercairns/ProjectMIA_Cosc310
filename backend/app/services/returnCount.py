# Function for admin to check how many returns a user has made to see if they spam return.
# Param is the requesting User to check for admin and user they want to see returns for.
# Returns the count.

from app.services.orderInteractor import load_orders
from app.schemas.userClass import User

def trackUserReturns(admin: User, user_id: str) -> int:

    if not admin.is_admin:
        raise PermissionError("Access denied, only admins can view return stats.")
   
    orders = load_orders(user_id)
    return_count = sum(1 for order in orders if order.returned is True)


    return return_count