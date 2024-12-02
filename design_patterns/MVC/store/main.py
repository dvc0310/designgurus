from store_mvc import *
# -----------------------------
# Main Application
# -----------------------------

def main():
    model = GroceryModel()
    controller = GroceryController(model)

    controller.run()


if __name__ == "__main__":
    main()