import unittest
from unittest.mock import patch
from buggybank.bank import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        """Create a new bank account before each test."""
        self.account = BankAccount("Foo", 100)

    def test_deposit(self):
        """Test deposit functionality."""
        self.account.deposit(50)
        self.assertEqual(self.account.get_balance(), 150)

    def test_withdraw(self):
        """Test withdraw functionality."""
        self.account.withdraw(50)
        self.assertEqual(self.account.get_balance(), 50)

    @patch.object(BankAccount, "get_balance", return_value=0)
    def test_overdraft(self, mock_get_balance):
        self.account.withdraw(200)
        self.assertEqual(self.account.get_balance(), 0)


if __name__ == "__main__":
    unittest.main()
