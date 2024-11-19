from abc import ABC, abstractmethod

class Subject(ABC):
    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass

class Stock(Subject):
    def __init__(self):
        self._observers = []
        self._price = 0

    def attach(self, observer):
        self._observers.append(observer)
        print(f"{observer.name} has subscribed.")

    def detach(self, observer):
        self._observers.remove(observer)
        print(f"{observer.name} has unsubscribed.")

    def notify(self):
        for observer in self._observers:
            observer.update(self._price)

    def set_price(self, price):
        self._price = price
        self.notify()
