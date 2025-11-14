from fastapi import APIRouter, HTTPException
from backend.app.services.paymentInteractor import load_payment, update_payment
from pydantic import BaseModel

router = APIRouter(prefix="/payment", tags=["Payment"])


@router.get("", response_model = dict)
def get_user_payment(user_id: str):
    try:
        payment = load_payment(user_id)
        return payment.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AddPaymentRequest(BaseModel):
    user_id: str
    card_number: str
    CVV: str
    expiration_date: str


@router.put("", response_model = dict)
def update_user_payment(request: AddPaymentRequest):
    """Card Number, CVV, and Expiration date Required"""
    try:
        payment = update_payment(request.user_id,
                             request.card_number,
                             request.CVV,
                             request.expiration_date)
        return payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

