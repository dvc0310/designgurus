# notification.py
from abc import ABC, abstractmethod

class NotificationObserver(ABC):
    @abstractmethod
    def update(self, user, message):
        pass

class EmailNotification(NotificationObserver):
    def update(self, user, message):
        print(f"Sending Email to {user.email}: {message}")

class SMSNotification(NotificationObserver):
    def update(self, user, message):
        print(f"Sending SMS to {user.phone}: {message}")

class InAppNotification(NotificationObserver):
    def update(self, user, message):
        print(f"Showing In-App Notification to {user.user_id}: {message}")

# Subject: Notification Manager
class NotificationManager:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)
        print(f"Attached {observer.__class__.__name__}")

    def detach(self, observer):
        self.observers.remove(observer)
        print(f"Detached {observer.__class__.__name__}")

    def notify(self, user, message):
        for observer in self.observers:
            observer.update(user, message)
