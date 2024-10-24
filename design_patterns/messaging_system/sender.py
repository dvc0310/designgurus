from abc import ABC, abstractmethod
from content import Content, TextContent, ImageContent
from editable import ImageEditable, TextEditable

class Sender(ABC):
    @abstractmethod
    def send(self, recipient, content: Content):
        pass

class TextSender(Sender, TextEditable, ABC):
    @abstractmethod
    def send(self, recipient, content: TextContent):
        pass  # The actual sending logic will vary in subclasses

    def spell_check(self, message):
        print("Spell Checking Message...")
        print(f"{message}")

        return message

    def check_keywords(self, message, keywords):
        found_keywords = [kw for kw in keywords if kw in message]
        return found_keywords

class ImageSender(Sender, ImageEditable, ABC):
    @abstractmethod
    def send(self, recipient, content: ImageContent):
        # This method will be implemented by concrete subclasses
        pass

    def resize_image(self, image_path, dimensions):
        print(f"Resizing Image to {dimensions}...")
        return image_path

    def add_watermark(self, image_path, watermark):
        print("Adding Watermark...")
        print(f"{watermark} added!")
        return image_path

    
