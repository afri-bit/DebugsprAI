from buggybank.bank import BankAccount
from buggybank.logger import setup_logger

logger = setup_logger(__name__)

if __name__ == "__main__":
    # Create a new account
    account = BankAccount("Foo", 100)

    # Show initial balance
    logger.info(f"Initial Balance: {account.get_balance()}")

    # Perform transactions
    account.deposit(50)
    logger.info(f"Balance after deposit: {account.get_balance()}")

    account.withdraw(200)  # ❌ This should fail, but logic allows it!
    logger.info(f"Balance after withdrawal: {account.get_balance()}")  # ❌ Wrong balance!
