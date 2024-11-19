from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, price):
        pass

class Investor(Observer):
    def __init__(self, name, notification_handler):
        self.name = name
        self.notification_handler = notification_handler

    def update(self, price):
        message = f"Investor {self.name} notified of current price: ${price}"
        self.notification_handler.send(self.name, message)

class NewsAgency(Observer):
    def __init__(self, name, notification_handler):
        self.name = name
        self.notification_handler = notification_handler

    def update(self, price):
        message = f"News Agency {self.name} reports new price: ${price}"
        self.notification_handler.send(self.name, message)

class PortfolioManager(Observer):
    def __init__(self, name, notification_handler):
        self.name = name
        self.notification_handler = notification_handler

    def update(self, price):
        message = f"Portfolio Manager {self.name} updates portfolio based on price: ${price}"
        self.notification_handler.send(self.name, message)
