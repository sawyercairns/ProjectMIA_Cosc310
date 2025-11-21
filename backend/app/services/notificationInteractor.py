import json
import os
from typing import List
from pathlib import Path
from backend.app.schemas.notificationClass import Notification

"""
Notification interactor for managing user notifications.
Handles creating, retrieving, and dismissing notifications.
"""

path = Path(__file__).resolve().parents[1] / "data" / "notifications.json"


def create_notification(user_id: str, notification: Notification) -> dict:
    """
    Create a new notification for a user.
    Automatically assigns notification_id and saves to JSON.
    Returns the created notification as dict.
    """

    all_data = _load_all_notifications()
    user_notifications = all_data.get(user_id, [])

    notification_dict = notification.to_dict()
    user_notifications.append(notification_dict)
    
    all_data[user_id] = user_notifications
    _save_all_notifications(all_data)
    
    return notification_dict


def get_user_notifications(user_id: str) -> List[dict]:
    """
    Load all active notifications for a user.
    """
    if not os.path.exists(path):
        return []
    
    all_data = _load_all_notifications()
    return all_data.get(user_id, [])


def dismiss_notification(user_id: str, notification_id: int) -> None:
    """
    Delete a notification from the system.
    """
    all_data = _load_all_notifications()
    user_notifications = all_data.get(user_id, [])
    
    user_notifications = [
        n for n in user_notifications 
        if n.get("notification_id") != notification_id
    ]
    
    all_data[user_id] = user_notifications
    _save_all_notifications(all_data)


def get_notification_by_id(user_id: str, notification_id: int) -> dict:
    """
    Get a specific notification by ID.
    Returns None if not found.
    """
    notifications = get_user_notifications(user_id)
    for notification in notifications:
        if notification.get("notification_id") == notification_id:
            return notification
    return None


def _get_next_notification_id(user_id: str) -> int:
    """
    Get next notification ID for this user.
    """
    notifications = get_user_notifications(user_id)
    if not notifications:
        return 1
    
    max_id = max(n.get("notification_id", 0) for n in notifications)
    return max_id + 1


def _load_all_notifications() -> dict:
    """
    Load entire notifications.json file.
    """
    if not os.path.exists(path):
        return {}
    
    try:
        with open(path, "r", encoding="UTF-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def _save_all_notifications(data: dict) -> None:
    """
    save all notifications to JSON.
    """
    tmp_path = path.with_suffix(".tmp")
    with tmp_path.open("w", encoding="UTF-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)