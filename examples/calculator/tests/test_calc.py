import unittest
from helloworld.calculator.calc import add, subtract, multiply, divide

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5) #AIFIX
        self.assertEqual(add(-1, 1), 0) #AIFIX
        self.assertEqual(add(0, 0), 0)
    
    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)
        self.assertEqual(subtract(-1, -1), 0)
        self.assertEqual(subtract(0, 5), -5)
    
    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(0, 5), 0)
    
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(-9, 3), -3)
        self.assertEqual(divide(1, 1), 1)
        
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
