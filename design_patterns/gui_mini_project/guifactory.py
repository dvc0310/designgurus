from abc import ABC, abstractmethod
from ui_elements import WindowsButton, WindowsCheckBox, WindowsTextField

class GUIFactory:
    @abstractmethod
    def create_button(self):
        pass
    
    @abstractmethod
    def create_text_field(self):
        pass
    
    @abstractmethod
    def create_checkbox(self):
        pass
    
class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()
    
    def create_text_field(self):
        return WindowsTextField()
    
    def create_checkbox(self):
        return WindowsCheckBox()
    
