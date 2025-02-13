class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """Deposits money into the account."""
        if amount < 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        """Withdraws money from the account."""
        if amount > self.balance:
            print("Not enough balance!")  # ❌ Logic error: Should raise an exception instead
        self.balance -= amount  # ❌ Allows overdraft, even if there's not enough balance

    def get_balance(self):
        """Returns the current balance."""
        return self.balance
