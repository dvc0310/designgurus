from abc import ABC, abstractmethod

class Content(ABC):
    @abstractmethod
    def get_content(self):
        pass

class TextContent(Content):
    def __init__(self, text):
        self.text = text
    
    def get_content(self):
        return self.text

class ImageContent(Content):
    def __init__(self, image_path):
        self.image_path = image_path
    
    def get_content(self):
        return self.image_path
