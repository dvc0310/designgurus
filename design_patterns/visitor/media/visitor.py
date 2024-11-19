from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visit_book(self, book):
        pass
    
    @abstractmethod
    def visit_DVD(self, DVD):
        pass
    
    @abstractmethod
    def visit_magazine(self, magazine):
        pass

    @abstractmethod
    def visit_library(self, library):
        pass