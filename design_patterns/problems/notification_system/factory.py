from notifications import EmailNotification, SMSNotification, PushNotification

# Factory Method Pattern: Notification Factory
class NotificationFactory:
    @staticmethod
    def get_notification(method):
        if method == 'email':
            return EmailNotification()
        elif method == 'sms':
            return SMSNotification()
        elif method == 'push':
            return PushNotification()
        else:
            raise ValueError(f"Unknown notification method: {method}")
