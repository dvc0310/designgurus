from content import TextContent, ImageContent
from sender import TextSender, ImageSender

class SMSTextSender(TextSender):
    def send(self, recipient, content: TextContent):
        message = content.get_content()
        corrected_message = self.spell_check(message)
        print(f"Sending SMS to {recipient}: {corrected_message}")

class MMSImageSender(ImageSender):
    def send(self, recipient, content: ImageContent):
        # Implementation of image sending via MMS
        image_path = content.get_content()
        print(f"Sending MMS to {recipient}: Image at {image_path}")
        
        # Optionally, you can resize or watermark the image before sending
        watermarked_image = self.add_watermark(image_path, "Sample Watermark")
        print(f"Watermarked image path: {watermarked_image}")

class EmailTextSender(TextSender):
    def send(self, recipient, content: TextContent):
        message = content.get_content()
        corrected_message = self.spell_check(message)
        print(f"Sending Email to {recipient}: {corrected_message}")

class EmailImageSender(ImageSender):
    def send(self, recipient, content: ImageContent):
        # Implementation of image sending via MMS
        image_path = content.get_content()
        print(f"Sending Email Image to {recipient}: Image at {image_path}")
        
        # Optionally, you can resize or watermark the image before sending
        watermarked_image = self.add_watermark(image_path, "Sample Watermark")
        print(f"Watermarked image path: {watermarked_image}")
