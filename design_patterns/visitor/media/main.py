from concrete_media import *
from concrete_visitor import *

library_items = [
    Book("Python 101", "John Doe", 5.99),
    DVD("The Matrix", 120, 3.99),
    Magazine("Tech Weekly", 42, 2.50),
    Book("Data Science Handbook", "Jane Smith", 7.49)
]

visitor = LibraryVisitor()

# Visit each item with the same visitor instance
for item in library_items:
    item.accept(visitor)


print("\n--- Calculating Total Size ---")
print(f"\nTotal size: ${visitor.get_total_cost()}")