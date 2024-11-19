from subject import Stock
from notification_handlers import *
from observer import *
def main():
    # Create the stock subject
    stock = Stock()

    # Create notification handlers
    email_handler = EmailNotificationHandler()
    sms_handler = SMSNotificationHandler()
    push_handler = PushNotificationHandler()

    # Create observers with different notification handlers
    investor1 = Investor("John", email_handler)
    investor2 = Investor("Alice", sms_handler)
    news_agency1 = NewsAgency("Finance Today", push_handler)
    portfolio_manager1 = PortfolioManager("Sarah", email_handler)

    # Attach observers to the stock
    stock.attach(investor1)
    stock.attach(investor2)
    stock.attach(news_agency1)
    stock.attach(portfolio_manager1)

    # Simulate price changes
    print("\nSetting stock price to $100")
    stock.set_price(100)

    print("\nSetting stock price to $105")
    stock.set_price(105)

    # Detach an observer
    print("\nDetaching the Portfolio Manager")
    stock.detach(portfolio_manager1)

    # Simulate another price change
    print("\nSetting stock price to $110")
    stock.set_price(110)

if __name__ == "__main__":
    main()
