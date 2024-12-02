from abc import ABC, abstractmethod
from observer import Observer

class Subject(ABC):
    @abstractmethod
    def registerObserver(self, observer: Observer) -> None:
        pass
    
    @abstractmethod
    def removeObserver(self, observer: Observer) -> None:
        pass
    
    @abstractmethod
    def notifyObservers(self) -> None:
        pass