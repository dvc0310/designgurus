from notifications_factory import NotificationFactory

urgent_email = NotificationFactory.create_sender("email", "urgent")
urgent_email.send_message(recipient="sjchun0310@gmail.com", message="You're the GOAT!")

urgent_email.set_priority_status(True)
urgent_email.send_message(recipient="sjchun0310@gmail.com", message="You're the GOAT!")

normal_email = NotificationFactory.create_sender("email", "normal")
normal_email.send_message(recipient="sjchun0310@gmail.com", message="You're the GOAT!")
normal_email.set_priority_status(True)
normal_email.send_message(recipient="sjchun0310@gmail.com", message="You're the GOAT!")
