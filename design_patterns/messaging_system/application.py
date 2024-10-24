from messaging_factory import MessagingFactory, SMSFactory, EmailFactory
from content import TextContent, ImageContent
class Application():
    def __init__(self, factory: MessagingFactory):
        self.factory = factory
        self.text_sender = self.factory.create_text_sender()
        self.image_sender = self.factory.create_image_sender()
        
    def run(self):
        self.text_sender.send("David", TextContent("Hi David!"))
        self.image_sender.send("David", ImageContent("photo.jpg"))
        
def get_factory(type) -> MessagingFactory:
    
    if type == "SMS":
        return SMSFactory()
    elif type == "Email":
        return EmailFactory()
    #elif os_name == "Linux":
    #    return LinuxFactory()
    else:
        raise Exception(f"Unsupported type: {type}")
    

if __name__ == "__main__":
    factory = get_factory("SMS")
    app = Application(factory)
    app.run()
    print("=============================================================================================")
    factory = get_factory("Email")
    app = Application(factory)
    app.run()
