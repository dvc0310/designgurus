from abc import ABC, abstractmethod

class FileSystemElement(ABC):
    def __init__(self):
        self._visitor = None
    
    @abstractmethod
    def accept(self, visitor):
        pass
    
class Visitor(ABC):
    @abstractmethod
    def visitFile(self, element):
        pass
    
    @abstractmethod
    def visitDirectory(self, element):
        pass
