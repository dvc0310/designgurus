import os
import platform
from typing import List, Callable, Optional


# -----------------------------
# Observer Pattern Implementation
# -----------------------------

class Observable:
    def __init__(self):
        self._observers: List[Callable] = []

    def add_observer(self, observer: Callable):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Callable):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer()


# -----------------------------
# Model
# -----------------------------

class GroceryModel(Observable):
    def __init__(self):
        super().__init__()
        self.items: List[dict] = []  # Each item is a dictionary with 'name' and 'price'

    def add_item(self, name: str, price: float):
        self.items.append({'name': name, 'price': price})
        self.notify_observers()

    def delete_item(self, index: int):
        if 0 <= index < len(self.items):
            del self.items[index]
            self.notify_observers()
        else:
            raise IndexError("Item index out of range.")

    def change_price(self, index: int, new_price: float):
        if 0 <= index < len(self.items):
            self.items[index]['price'] = new_price
            self.notify_observers()
        else:
            raise IndexError("Item index out of range.")

    def get_total(self) -> float:
        return sum(item['price'] for item in self.items)


# -----------------------------
# View
# -----------------------------

class GroceryView:
    def __init__(self, controller: 'GroceryController', model: GroceryModel):
        self.controller = controller
        self.model = model
        self.model.add_observer(self.display)

    def clear_console(self):
        """Clears the console based on the operating system."""
        os_name = platform.system()
        if os_name == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    def display(self):
        """Clears the console and displays the current state and commands."""
        self.clear_console()
        print("\nCommands:")
        print("1. Add Item")
        print("2. Delete Item")
        print("3. Change Price")
        print("4. Exit")
        print("\n--- Grocery Order System ---")
        if not self.model.items:
            print("No items in the order.")
        else:
            print("Items in the order:")
            for idx, item in enumerate(self.model.items, start=1):
                print(f"{idx}. {item['name']} - ${item['price']:.2f}")
            print(f"Total: ${self.model.get_total():.2f}")


    def get_user_input(self) -> Optional[str]:
        return input("\nEnter command number: ").strip()

    def prompt_add_item(self) -> Optional[dict]:
        name = input("Enter the item name (or type 'cancel' to abort): ").strip()
        if name.lower() == 'cancel':
            return None
        try:
            price_str = input("Enter the item price: ").strip()
            price = float(price_str)
            if price < 0:
                print("Price cannot be negative.")
                return None
            return {'name': name, 'price': price}
        except ValueError:
            print("Invalid price entered.")
            return None

    def prompt_delete_item(self) -> Optional[int]:
        if not self.model.items:
            print("No items to delete.")
            return None
        try:
            index_str = input("Enter the item number to delete (or type 'cancel' to abort): ").strip()
            if index_str.lower() == 'cancel':
                return None
            index = int(index_str) - 1
            if 0 <= index < len(self.model.items):
                return index
            else:
                print("Invalid item number.")
                return None
        except ValueError:
            print("Invalid input.")
            return None

    def prompt_change_price(self) -> Optional[dict]:
        if not self.model.items:
            print("No items to change price.")
            return None
        try:
            index_str = input("Enter the item number to change price (or type 'cancel' to abort): ").strip()
            if index_str.lower() == 'cancel':
                return None
            index = int(index_str) - 1
            if not (0 <= index < len(self.model.items)):
                print("Invalid item number.")
                return None
            new_price_str = input(f"Enter the new price for '{self.model.items[index]['name']}': ").strip()
            new_price = float(new_price_str)
            if new_price < 0:
                print("Price cannot be negative.")
                return None
            return {'index': index, 'new_price': new_price}
        except ValueError:
            print("Invalid input.")
            return None


# -----------------------------
# Controller
# -----------------------------

class GroceryController:
    def __init__(self, model: GroceryModel):
        self.model = model
        self.view = GroceryView(controller=self, model=self.model)

    def run(self):
        self.view.display()
        while True:
            command = self.view.get_user_input()
            if command == '1':
                self.handle_add_item()
            elif command == '2':
                self.handle_delete_item()
            elif command == '3':
                self.handle_change_price()
            elif command == '4':
                print("Exiting the Grocery Order System. Goodbye!")
                break
            else:
                print("Invalid command. Please try again.")
                self.view.display()  # Only display again if the command was invalid

    def handle_add_item(self):
        item = self.view.prompt_add_item()
        if item:
            self.model.add_item(item['name'], item['price'])
            print(f"Added item: {item['name']} - ${item['price']:.2f}")

    def handle_delete_item(self):
        index = self.view.prompt_delete_item()
        if index is not None:
            try:
                item_name = self.model.items[index]['name']
                self.model.delete_item(index)
                print(f"Deleted item: {item_name}")
            except IndexError as e:
                print(str(e))

    def handle_change_price(self):
        data = self.view.prompt_change_price()
        if data:
            try:
                self.model.change_price(data['index'], data['new_price'])
                print(f"Changed price of '{self.model.items[data['index']]['name']}' to ${data['new_price']:.2f}")
            except IndexError as e:
                print(str(e))


