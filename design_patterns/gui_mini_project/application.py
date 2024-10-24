from guifactory import GUIFactory, WindowsFactory
import platform

class Application():
    def __init__(self, factory: GUIFactory):
        self.factory = factory
        self.button = self.factory.create_button()
        self.text_field = self.factory.create_text_field()
        self.checkbox = self.factory.create_checkbox()
        
    def run(self):
        self.button.click()
        self.text_field.set_text("Hello World")
        self.checkbox.check()
        

def get_factory() -> GUIFactory:
    os_name = platform.system()
    if os_name == "Windows":
        return WindowsFactory()
    #elif os_name == "Darwin":
    #    return MacOSFactory()
    #elif os_name == "Linux":
    #    return LinuxFactory()
    else:
        raise Exception(f"Unsupported OS: {os_name}")


if __name__ == "__main__":
    factory = get_factory()
    app = Application(factory)
    app.run()
