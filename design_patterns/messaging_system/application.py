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
        

if __name__ == "__main__":
    factory = MessagingFactory.get_factory("SMS")
    app = Application(factory)
    app.run()
    print("=============================================================================================")
    factory = MessagingFactory.get_factory("Email")
    app = Application(factory)
    app.run()
