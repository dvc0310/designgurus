from media import MediaItem, Element
from visitor import Visitor

class Library(Element):
    def __init__(self, name):
        self.name = name
        self.children: list[MediaItem] = []  

    def add(self, element):
        self.children.append(element)

    def get_library(self):
        return self.children

    def accept(self, visitor):
        visitor.visit_library(self)

class Book(MediaItem):
    def __init__(self, title, author, cost):
        super().__init__(title, author, cost)
        
    def accept(self, visitor: Visitor):
        visitor.visit_book(self)
    
    def display_media(self):
        super().display_media()
        print("Media Type: Book")

class DVD(MediaItem):
    def __init__(self, title, author, cost):
        super().__init__(title, author, cost)
        
    def accept(self, visitor: Visitor):
        visitor.visit_DVD(self)
    
    def display_media(self):
        super().display_media()
        print("Media Type: DVD")    
        
class Magazine(MediaItem):
    def __init__(self, title, author, cost):
        super().__init__(title, author, cost)
        
    def accept(self, visitor: Visitor):
        visitor.visit_magazine(self)

    def display_media(self):
        super().display_media()
        print("Media Type: Magazine")