from concrete_payment_methods import PaymentStrategy

class PaymentContext():
    def __init__(self):
        self.payment_strategy = None
    
    def set_payment_strategy(self, payment_strategy: PaymentStrategy):
        self.payment_strategy = payment_strategy
        
    def process_payment(self, money):
        if self.payment_strategy:
            return self.payment_strategy.payMoney(money)
        return "No payment method set!"
