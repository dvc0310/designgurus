# factories.py
from authentication import PasswordAuthentication, OAuthAuthentication, BiometricAuthentication
from notifications import EmailNotification, SMSNotification, InAppNotification

class AuthenticationFactory:
    @staticmethod
    def get_authentication(method):
        if method == 'password':
            return PasswordAuthentication()
        elif method == 'oauth':
            return OAuthAuthentication()
        elif method == 'biometric':
            return BiometricAuthentication()
        else:
            raise ValueError(f"Unknown authentication method: {method}")

class NotificationFactory:
    @staticmethod
    def get_notification(method):
        if method == 'email':
            return EmailNotification()
        elif method == 'sms':
            return SMSNotification()
        elif method == 'in_app':
            return InAppNotification()
        else:
            raise ValueError(f"Unknown notification method: {method}")
