from abc import ABC, abstractmethod
from concrete_senders import SMSTextSender, MMSImageSender, EmailImageSender, EmailTextSender

class MessagingFactory(ABC):
    @abstractmethod
    def create_text_sender(self):
        pass
    
    @abstractmethod
    def create_image_sender(self):
        pass

    @staticmethod
    def get_factory(factory_type: str) -> 'MessagingFactory':
        if factory_type == "SMS":
            return SMSFactory()
        elif factory_type == "Email":
            return EmailFactory()
        else:
            raise ValueError(f"Unsupported factory type: {factory_type}")

class SMSFactory(MessagingFactory):
    def create_text_sender(self):
        return SMSTextSender()
    
    def create_image_sender(self):
        return MMSImageSender()
    
class EmailFactory(MessagingFactory):
    def create_text_sender(self):
        return EmailTextSender()
    
    def create_image_sender(self):
        return EmailImageSender()