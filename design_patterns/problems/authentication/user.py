# user.py
class User:
    def __init__(self, user_id, email, phone, auth_preferences=None, notification_preferences=None):
        self.user_id = user_id
        self.email = email
        self.phone = phone
        self.auth_preferences = auth_preferences or ['password']
        self.notification_preferences = notification_preferences or ['email']
