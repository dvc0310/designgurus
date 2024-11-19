from abc import ABC, abstractmethod

class NotificationHandler(ABC):
    @abstractmethod
    def send(self, name, message):
        pass

class EmailNotificationHandler(NotificationHandler):
    def send(self, name, message):
        print(f"Sending email to {name}: {message}")

class SMSNotificationHandler(NotificationHandler):
    def send(self, name, message):
        print(f"Sending SMS to {name}: {message}")

class PushNotificationHandler(NotificationHandler):
    def send(self, name, message):
        print(f"Sending push notification to {name}: {message}")
