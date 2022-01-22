from django.test import TestCase
from .calc import add, subtract


class CalcTests(TestCase):
    
    def test_add_numbers(self):
        """Function that test addition of two numbers"""
        self.assertEqual(add(1, 2), 3)

    def test_subtract_numbers(self):
        """Test to check subtraction of two numbers"""
        self.assertEqual(subtract(1, 2), 1)