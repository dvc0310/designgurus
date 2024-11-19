from abc import ABC, abstractmethod

class CartItem(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass
    
class Visitor:
    @abstractmethod
    def visit_electronics(self, electronics):
        pass

    @abstractmethod
    def visit_groceries(self, groceries):
        pass
    
    @abstractmethod
    def visit_clothing(self, clothing):
        pass
