from abc import ABC, abstractmethod

# Strategy
class PaymentStrategy(ABC):
    @abstractmethod
    def payMoney(self, money):
        pass
    
    @abstractmethod
    def calculate_transaction_fee(self, amount, rate):
        pass
    
    @abstractmethod
    def apply_discount(self, amount, discount_rate):
        pass
    