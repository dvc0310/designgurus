from notifications import NotificationStrategy
# Decorator Pattern: Notification Decorator
class NotificationDecorator(NotificationStrategy):
    def __init__(self, notification):
        self.notification = notification

    def send(self, user, message):
        self.notification.send(user, message)

# Concrete Decorator: Header Decorator
class HeaderDecorator(NotificationDecorator):
    def send(self, user, message):
        message = f"*** Header ***\n{message}"
        super().send(user, message)

# Concrete Decorator: Footer Decorator
class FooterDecorator(NotificationDecorator):
    def send(self, user, message):
        message = f"{message}\n*** Footer ***"
        super().send(user, message)
