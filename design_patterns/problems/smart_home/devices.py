from abc import ABC, abstractmethod

class Command(ABC):
    def execute(self):
        pass

class Light:
    def __init__(self, room):
        self.room = room
        
    def turn_on(self):
        print(f"Light Turned On for {self.room}")

    def turn_off(self):
        print(f"Light Turned Off for {self.room}")

class TurnOnLightCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_on()

class TurnOffLightCommand(Command):
    def __init__(self, light: Light):
        self.light = light

    def execute(self):
        self.light.turn_off()

class Controller(ABC):
    def __init__(self):
        self.command = None
    
    @abstractmethod
    def choose_button(self, command):
        pass
    
    @abstractmethod
    def press_button(self):
        pass
        
class Remote(Controller):
    def choose_button(self, command: Command):
        self.command = command
        
    def press_button(self):
        self.command.execute()
        
# Client Code
if __name__ == "__main__":
    light = Light("David's room")
    turn_on = TurnOnLightCommand(light)
    turn_off = TurnOffLightCommand(light)

    remote = Remote()
    remote.choose_button(turn_on)
    remote.press_button()

    remote.choose_button(turn_off)
    remote.press_button()