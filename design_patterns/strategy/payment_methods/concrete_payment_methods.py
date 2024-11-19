from payment_methods import PaymentStrategy
    
# Concrete Strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, transaction_rate=.03, discount_rate=.1):
        self.transaction_rate = transaction_rate
        self.discount_rate = discount_rate
                
    def payMoney(self, money):
        money = self.calculate_transaction_fee(money)
        money = self.apply_discount(money)
        print(f"Paid ${money:.2f} using Credit Card!")
    
    def calculate_transaction_fee(self, amount):
        return amount * (1 + self.transaction_rate)  
    
    def apply_discount(self, amount):
        return amount * (1 - self.discount_rate)  
      
class PayPalPayment(PaymentStrategy):
    def __init__(self, transaction_rate=.05, discount_rate=.1):
        self.transaction_rate = transaction_rate
        self.discount_rate = discount_rate
        
    def payMoney(self, money):
        money = self.calculate_transaction_fee(money)
        money = self.apply_discount(money)
        print(f"Paid ${money:.2f} using PayPal!")
        
    def calculate_transaction_fee(self, amount):
        return amount * (1 + self.transaction_rate)  
    
    def apply_discount(self, amount):
        return amount * (1 - self.discount_rate)  
        
class CryptoPayment(PaymentStrategy):
    def __init__(self, transaction_rate=.1, discount_rate=.05):
        self.transaction_rate = transaction_rate
        self.discount_rate = discount_rate
        
    def payMoney(self, money):
        money = self.calculate_transaction_fee(money)
        money = self.apply_discount(money)
        print(f"Paid ${money:.2f} using Crypto!")
        
    def calculate_transaction_fee(self, amount):
        return amount * (1 + self.transaction_rate)  
    
    def apply_discount(self, amount):
        return amount * (1 - self.discount_rate)