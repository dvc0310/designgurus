from user import *
from notifications import NotificationManager
from factory import NotificationFactory
from notification_decorator import *
# Example Usage
def main():
    # Define user preferences
    builder = UserBuilder()
    user_creator = UserCreator(builder)
    user = user_creator.construct_user_all(
        name="John Doe",
        email="john@example.com",
        phone="1234567890"
    )
    user.remove_preference('push')

    # Create Notification Manager
    notification_manager = NotificationManager()

    # Attach notification methods based on user preferences
    for method in user.preferences:
        notification = NotificationFactory.get_notification(method)
        # Optionally decorate the notification
        notification = HeaderDecorator(notification)
        notification = FooterDecorator(notification)
        notification_manager.attach(notification)

    # Send a notification
    notification_manager.notify(user, "Your order has been shipped!")

if __name__ == "__main__":
    main()
