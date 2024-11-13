# Assume the payment strategies are implemented and imported, such as:
# CreditCardPayment, PayPalPayment, CryptoPayment, and a PaymentContext class.
from concrete_payment_methods import CreditCardPayment, CryptoPayment, PayPalPayment
from context import PaymentContext
def main():
    print("Welcome to the Payment Processing System")
    
    # Create a dictionary with user input mapped to (strategy instance, description)
    payment_methods = {
        "1": (CreditCardPayment(), "Credit Card"),
        "2": (PayPalPayment(), "PayPal"),
        "3": (CryptoPayment(), "Cryptocurrency")
    }
        
    # Create the payment context (the client chooses which strategy to use)
    payment_context = PaymentContext()

    # Print the payment method options
    print("Select a payment method:")
    for key, (_, description) in payment_methods.items():
        print(f"{key}. {description}")
        
    choice = input("Enter the number of your choice: ")

    # Check if the choice is valid and set the strategy
    if choice in payment_methods:
        payment_context.set_payment_strategy(payment_methods[choice][0])
    else:
        print("Invalid choice")
        return

    # Process payment
    amount = float(input("Enter the amount to be paid: $"))
    payment_context.process_payment(amount)

if __name__ == "__main__":
    main()
