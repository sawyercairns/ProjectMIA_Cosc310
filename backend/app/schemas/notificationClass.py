from abc import ABC, abstractmethod
from datetime import datetime


class Notification(ABC):
    """
    Abstract base class for notifications.
    """
    
    def __init__(self,
                 notification_id: int,
                 user_id: int,
                 notification_type: str,
                 created_at: str = None):
        self._notification_id = notification_id
        self._user_id = user_id
        self._notification_type = notification_type
        self._created_at = created_at or datetime.now().isoformat()
    
    # -- Properties --
    
    @property
    def notification_id(self):
        return self._notification_id
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def notification_type(self):
        return self._notification_type
    
    @property
    def created_at(self):
        return self._created_at
    
    # -- Abstract Methods --
    
    @abstractmethod
    def get_message(self) -> str:
        """
        Generate the notification message.
        """
        pass
    
    # -- Serialization --
    
    def to_dict(self):
        """
        Convert notification to dictionary for JSON serialization.
        Subclasses should extend this method to add their specific fields.
        """
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "notification_type": self.notification_type,
            "message": self.get_message(),
            "created_at": self.created_at
        }
