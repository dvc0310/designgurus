# facade.py
from factory import AuthenticationFactory, NotificationFactory
from notifications import NotificationManager

class AuthenticationSystem:
    def __init__(self):
        self.notification_manager = NotificationManager()

    def authenticate_user(self, user, credential):
        for method in user.auth_preferences:
            auth_strategy = AuthenticationFactory.get_authentication(method)
            if auth_strategy.authenticate(user, credential):
                self.send_notifications(user, f"Successfully authenticated using {method}.")
                return True
        self.send_notifications(user, "Authentication failed.")
        return False

    def send_notifications(self, user, message):
        self.notification_manager.observers.clear()
        for method in user.notification_preferences:
            notification = NotificationFactory.get_notification(method)
            self.notification_manager.attach(notification)
        self.notification_manager.notify(user, message)
