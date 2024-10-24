from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def click(self):
        pass

class TextField(ABC):
    @abstractmethod
    def set_text(self, text):
        pass
    
class CheckBox(ABC):
    @abstractmethod
    def check(self):
        pass
    
class WindowsButton(Button):
    def click(self):
        print("Windows Button Clicked!")
        
class WindowsTextField(TextField):
    def set_text(self, text):
        print(f"Text set to {text}")
        
class WindowsCheckBox(CheckBox):
    def check(self):
        print("CheckBox checked!")