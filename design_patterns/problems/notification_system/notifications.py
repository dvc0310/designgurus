from abc import ABC, abstractmethod

# Strategy Pattern: Notification Strategy Interface
class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, user, message):
        pass

# Concrete Strategy: Email Notification
class EmailNotification(NotificationStrategy):
    def send(self, user, message):
        print(f"Sending Email to {user.email}: {message}")

# Concrete Strategy: SMS Notification
class SMSNotification(NotificationStrategy):
    def send(self, user, message):
        print(f"Sending SMS to {user.phone}: {message}")

# Concrete Strategy: Push Notification
class PushNotification(NotificationStrategy):
    def send(self, user, message):
        print(f"Sending Push Notification to {user.name}: {message}")

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
            observer.send(user, message)
