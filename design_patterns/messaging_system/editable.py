from abc import ABC, abstractmethod

class TextEditable(ABC):
    @abstractmethod
    def spell_check(self, message):
        pass
    
    @abstractmethod
    def check_keywords(self, message, keywords):
        pass
    
class ImageEditable(ABC):
    @abstractmethod
    def resize_image(self, image_path, dimensions):
        pass
   
    @abstractmethod
    def add_watermark(self, image_path, watermark):
        pass