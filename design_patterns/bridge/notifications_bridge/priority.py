from abc import ABC, abstractmethod

class Priority(ABC):
    @abstractmethod
    def set_priority(self):
        pass
    
    @abstractmethod
    def get_type(self):
        pass
    
    @abstractmethod
    def turn_on_priority(self):
        pass
    
    @abstractmethod
    def turn_off_priority(self):
        pass    
    
    @abstractmethod
    def get_status(self):
        pass
    
class UrgentNotification(Priority):
    def __init__(self):
        super().__init__()
        self.active = False
        
    def set_priority(self, switch):
        if switch:
            self.turn_on_priority()
        else:
            self.turn_off_priority()
    
    def turn_on_priority(self):
        self.active = True
        print("Urgent Priority On!")

    def turn_off_priority(self):
        self.active = False
        print("Urgent Priority Off!")
    
    def get_type(self):
        return "Urgent!!!"
    
    def get_status(self):
        if self.active:
            return "Active"
        return "Not Active"
    
class NormalNotification(Priority):
    def __init__(self):
        super().__init__()
        self.active = False

    def set_priority(self, switch):
        if switch:
            self.turn_on_priority()
        else:
            self.turn_off_priority()
            
    def turn_on_priority(self):
        self.active = True
        print("Normal Priority On!")

    def turn_off_priority(self):
        self.active = False
        print("Normal Priority Off!")
        
    def get_type(self):
        return "Normal"

    def get_status(self):
        if self.active:
            return "Active"
        return "Not Active"