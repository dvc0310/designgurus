from abc import ABC, abstractmethod
from concrete_senders import SMSTextSender, MMSImageSender, EmailImageSender, EmailTextSender

class MessagingFactory(ABC):
    @abstractmethod
    def create_text_sender(self):
        pass
    
    @abstractmethod
    def create_image_sender(self):
        pass 
    

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