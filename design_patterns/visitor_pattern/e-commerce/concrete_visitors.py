from interface import Visitor
from cart_items import Electronics, Groceries, Clothing

class DiscountVisitor(Visitor):
    def visit_electronics(self, electronics: Electronics):
        discount_price = electronics.price * 0.9
        print(f"Electronics item '{electronics.name}' after discount: ${discount_price:.2f}")

    def visit_groceries(self, groceries: Groceries):
        discount_price = groceries.price * 0.95
        print(f"Groceries item '{groceries.name}' after discount: ${discount_price:.2f}")

    def visit_clothing(self, clothing: Clothing):
        discount_price = clothing.price * 0.95
        print(f"Clothing item '{clothing.name}' after discount: ${discount_price:.2f}")

    
class TaxVisitor(Visitor):
    def visit_electronics(self, electronics: Electronics):
        tax_price = electronics.price * 1.15
        print(f"Electronics item '{electronics.name}' after tax: ${tax_price:.2f}")

    def visit_groceries(self, groceries: Groceries):
        tax_price = groceries.price * 1.08
        print(f"Groceries item '{groceries.name}' after tax: ${tax_price:.2f}")

    def visit_clothing(self, clothing: Clothing):
        tax_price = clothing.price * 1.05
        print(f"Clothing item '{clothing.name}' after tax: ${tax_price:.2f}")