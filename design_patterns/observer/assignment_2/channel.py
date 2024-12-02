from subject import Subject
from observer import Observer
from follower import *

class Channel(Subject):
    def __init__(self, channel_name: str):
        self.__observers: list[Observer] = []
        self.__channel_name: str = channel_name
        self.__status: str = "N/A"
        
    def getStatus(self) -> str:
        return self.__status
    
    def setStatus(self, status: str) -> None:
        self.__status = status
        
    def notifyObservers(self) -> None:
        for observer in self.__observers:
            observer.update(self.__status)
    
    def registerObserver(self, observer: Observer) -> None:
        self.__observers.append(observer)
    
    def removeObserver(self, observer: Observer) -> None:
        self.__observers.remove(observer)