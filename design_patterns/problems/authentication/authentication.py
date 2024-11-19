# authentication.py
from abc import ABC, abstractmethod
from database import *
class AuthenticationStrategy(ABC):
    @abstractmethod
    def authenticate(self, user, credential):
        pass

# Concrete Strategies
class PasswordAuthentication(AuthenticationStrategy):
    def authenticate(self, user, credential):
        stored_password = user_data[user.user_id]['password']
        if credential == stored_password:
            return True
        return False

class OAuthAuthentication(AuthenticationStrategy):
    def authenticate(self, user, credential):
        stored_token = user_data[user.user_id]['oauth_token']
        if credential == stored_token:
            return True
        return False

class BiometricAuthentication(AuthenticationStrategy):
    def authenticate(self, user, credential):
        stored_biometric = user_data[user.user_id]['biometric']
        if credential == stored_biometric:
            return True
        return False
