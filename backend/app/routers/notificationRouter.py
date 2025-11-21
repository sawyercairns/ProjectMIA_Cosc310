from fastapi import APIRouter, HTTPException
from backend.app.services import notificationInteractor
from typing import List

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/{user_id}", response_model=List[dict])
def get_notifications(user_id: str):
    try:
        notifications = notificationInteractor.get_user_notifications(user_id)
        return notifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}/{notification_id}")
def dismiss_notification(user_id: str, notification_id: int):
    try:
        notificationInteractor.dismiss_notification(user_id, notification_id)
        return {"message": "Notification dismissed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/{notification_id}", response_model=dict)
def get_notification_by_id(user_id: str, notification_id: int):
    try:
        notification = notificationInteractor.get_notification_by_id(user_id, notification_id)
        if notification is None:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
