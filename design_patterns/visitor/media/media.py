from abc import ABC, abstractmethod
from visitor import Visitor

class Element(ABC):
    @abstractmethod    
    def accept(self, visitor: Visitor):
        pass    

class MediaItem(Element):
    def __init__(self, title, author, cost):
        self.title = title
        self.author = author
        self.cost = cost
        
    @abstractmethod    
    def accept(self, visitor: Visitor):
        pass

    def display_media(self):
        print(f"Title: {self.get_title()}")    
        print(f"Author: {self.get_author()}")    
        print(f"Cost: {self.get_cost()}") 
    
    def get_cost(self):
        return self.cost

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author