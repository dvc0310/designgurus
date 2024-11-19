# main.py
from user import User
from facade import AuthenticationSystem
from database import user_data

def main():
    # Create users
    user1 = User(
        user_id="user1",
        email="user1@example.com",
        phone="1234567890",
        auth_preferences=['password', 'oauth'],
        notification_preferences=['email', 'sms']
    )

    user2 = User(
        user_id="user2",
        email="user2@example.com",
        phone="0987654321",
        auth_preferences=['biometric', 'password'],
        notification_preferences=['in_app']
    )

    # Create the authentication system facade
    auth_system = AuthenticationSystem()

    # Authenticate user1
    print("\nAuthenticating user1:")
    credential = "password123"  # Correct password
    auth_system.authenticate_user(user1, credential)

    # Authenticate user2 with incorrect password
    print("\nAuthenticating user2 with incorrect password:")
    credential = "wrong_password"  # Incorrect password
    auth_system.authenticate_user(user2, credential)

    # Authenticate user2 with biometric data
    print("\nAuthenticating user2 with biometric data:")
    credential = "biometric_data_user2"  # Correct biometric data
    auth_system.authenticate_user(user2, credential)

if __name__ == "__main__":
    main()
