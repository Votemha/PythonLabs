import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # Добавляем lr8/ в путь
from models.app import App
from models.author import Author
from models.currency import Currency
from models.user import User

class TestApp(unittest.TestCase):
    def setUp(self):
        self.author = Author('Test Author', 'P3122')
        self.app = App('TestApp', '1.0', self.author)

    def test_init(self):
        self.assertEqual(self.app.name, 'TestApp')
        self.assertEqual(self.app.version, '1.0')
        self.assertEqual(self.app.author, self.author)

    def test_name_setter_valid(self):
        self.app.name = 'NewApp'
        self.assertEqual(self.app.name, 'NewApp')

    def test_name_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.app.name = 'A'
        with self.assertRaises(ValueError):
            self.app.name = 123

    def test_version_setter_valid(self):
        self.app.version = '2.0'
        self.assertEqual(self.app.version, '2.0')

    def test_version_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.app.version = ''

class TestAuthor(unittest.TestCase):
    def setUp(self):
        self.author = Author('Test Author', 'P3122')

    def test_init(self):
        self.assertEqual(self.author.name, 'Test Author')
        self.assertEqual(self.author.group, 'P3122')

    def test_name_setter_valid(self):
        self.author.name = 'New Author'
        self.assertEqual(self.author.name, 'New Author')

    def test_name_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.author.name = 'A'
        with self.assertRaises(ValueError):
            self.author.name = 123

    def test_group_setter_valid(self):
        self.author.group = 'P31234'
        self.assertEqual(self.author.group, 'P31234')

    def test_group_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.author.group = 'P3'
        with self.assertRaises(ValueError):
            self.author.group = 123

class TestCurrency(unittest.TestCase):
    def setUp(self):
        self.currency = Currency(id=None, num_code=None, char_code='USD', name=None, value=1.0, nominal=1)

    def test_init(self):
        self.assertEqual(self.currency.char_code, 'USD')
        self.assertEqual(self.currency.value, 1.0)
        self.assertEqual(self.currency.nominal, 1)

    def test_char_code_setter_valid(self):
        self.currency.char_code = 'EUR'
        self.assertEqual(self.currency.char_code, 'EUR')

    def test_char_code_setter_invalid(self):
        with self.assertRaises(ValueError):
            self.currency.char_code = 'INVALID'

    def test_value_getter(self):
        self.assertEqual(self.currency.value, 1.0)

    def test_nominal_getter(self):
        self.assertEqual(self.currency.nominal, 1)

class TestUser(unittest.TestCase):
    def setUp(self):
        # Сбрасываем данные пользователей перед каждым тестом
        User._User__dataUsers = {}
        User._User__idVal = 0
        self.user = User.userUp('TestUser')

    def test_user_creation(self):
        self.assertIsNotNone(self.user)
        self.assertEqual(self.user.name, 'TestUser')

    def test_authenticate_valid(self):
        authenticated = User.authenticate('TestUser')
        self.assertEqual(authenticated, self.user)

    def test_authenticate_invalid(self):
        authenticated = User.authenticate('NonExistent')
        self.assertIsNone(authenticated)

    def test_subscribe_currency(self):
        self.user.subscribeCurrency('USD')
        self.assertIn('USD', self.user.currencies)

    def test_unsubscribe_currency(self):
        self.user.subscribeCurrency('USD')
        self.user.unsubscribeCurrency('USD')
        self.assertNotIn('USD', self.user.currencies)

if __name__ == '__main__':
    unittest.main()