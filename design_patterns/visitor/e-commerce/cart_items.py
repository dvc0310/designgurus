from interface import CartItem, Visitor

class Electronics(CartItem):
    def __init__(self, name, price, warranty_period):
        self.name = name
        self.price = price
        self.warranty_period = warranty_period

    def accept(self, visitor: Visitor):
        visitor.visit_electronics(self)

class Groceries(CartItem):
    def __init__(self, name, price, expiration_date):
        self.name = name
        self.price = price
        self.expiration_date = expiration_date

    def accept(self, visitor: Visitor):
        visitor.visit_groceries(self)

class Clothing(CartItem):
    def __init__(self, name, price, size):
        self.name = name
        self.price = price
        self.size = size

    def accept(self, visitor: Visitor):
        visitor.visit_clothing(self)