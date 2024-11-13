from interface import CartItem
from cart_items import Electronics, Groceries, Clothing
from concrete_visitors import DiscountVisitor, TaxVisitor

    
# Create some cart items
cart: list[CartItem] = [
    Electronics("Smartphone", 1000, 2),
    Groceries("Apples", 5, "2024-12-01"),
    Clothing("Jeans", 42, "M")
]

# Create the visitors
discount_visitor = DiscountVisitor()
tax_visitor = TaxVisitor()

# Apply visitors to each item in the cart
print("Applying Discount Visitor:")
for item in cart:
    item.accept(discount_visitor)

print("\nApplying Tax Visitor:")
for item in cart:
    item.accept(tax_visitor)