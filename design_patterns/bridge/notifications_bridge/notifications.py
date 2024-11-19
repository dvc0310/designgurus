from abc import ABC, abstractmethod
from priority import Priority

class NotificationSender(ABC):
    def __init__(self, priority: Priority):
        self.priority = priority
        
    @abstractmethod
    def send_message(self, recipient, message):
        pass
    
    @abstractmethod
    def set_priority_status(self, switch):
        pass

class EmailSender(NotificationSender):
    def send_message(self, recipient, message):
        
        print(f"Email Message\n")
        print(f"Type: {self.priority.get_type()}\n")
        print(f"Status: {self.priority.get_status()}\n")

        print(message)
        print(f"Email Message sent to: {recipient}!")
    
    def set_priority_status(self, switch):
        if switch:
            self.priority.turn_on_priority()
        else:
            self.priority.turn_off_priority()
    
class SMSSender(NotificationSender):
    def send_message(self, recipient, message):
        print(f"SMS Message\n")
        print(f"Type: {self.priority.get_type()}\n")
        print(f"Status: {self.priority.get_status()}\n")

        print(message)
        print(f"SMS Message sent to: {recipient}!")
    
    def set_priority_status(self, switch):
        if switch:
            self.priority.turn_on_priority()
        else:
            self.priority.turn_off_priority()    
            
class PushSender(NotificationSender):
    def send_message(self, recipient, message):
        print(f"Push Message\n")
        print(f"Type: {self.priority.get_type()}\n")
        print(f"Status: {self.priority.get_status()}\n")

        print(message)
        print(f"Push Message sent to: {recipient}!")
        
    def set_priority_status(self, switch):
        if switch:
            self.priority.turn_on_priority()
        else:
            self.priority.turn_off_priority()