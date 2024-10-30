from notifications import NotificationSender, EmailSender, Priority, SMSSender, PushSender 
from priority import NormalNotification, UrgentNotification
class NotificationFactory:
    @staticmethod
    def create_priority(priority_type: str) -> Priority:
        if priority_type == "urgent":
            return UrgentNotification()
        elif priority_type == "normal":
            return NormalNotification()
        else:
            raise ValueError("Unknown notification type")

    @staticmethod
    def create_sender(sender_type: str, priority_type: str) -> NotificationSender:
        # Use the factory method to create a transmission
        priority = NotificationFactory.create_priority(priority_type)
        
        # Create the vehicle with the selected transmission
        if sender_type == "email":
            return EmailSender(priority)
        elif sender_type == "SMS":
            return SMSSender(priority)
        elif sender_type == "push":
            return PushSender(priority)
        else:
            raise ValueError("Unknown Sender type")