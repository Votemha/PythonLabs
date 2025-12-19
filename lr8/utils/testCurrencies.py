import unittest
from requests import exceptions
import io
from currencies_api import get_currencies
from currencies_api import logger

MAX_R_VALUE = 1000


# Тесты
class TestGetCurrencies(unittest.TestCase):

  def test_currency_usd(self):
    """
      Проверяет наличие ключа в словаре и значения этого ключа
    """
    currency_list = ['USD']
    currency_data = get_currencies(currency_list)

    self.assertIn(currency_list[0], currency_data)
    self.assertIsInstance(currency_data['USD'], float)
    self.assertGreaterEqual(currency_data['USD'], 0)
    self.assertLessEqual(currency_data['USD'], MAX_R_VALUE)

  def test_nonexist_code(self):
    self.assertIn("Код валюты", get_currencies(['XYZ'])['XYZ'])
    self.assertIn("XYZ", get_currencies(['XYZ'])['XYZ'])
    self.assertIn("не найден", get_currencies(['XYZ'])['XYZ'])

  def test_get_currency_error(self):
    error_phrase_regex = "Ошибка при запросе к API"
    currency_list = ['USD']
    output_stream = io.StringIO()

    with self.assertRaises(exceptions.RequestException):
      currency_data = get_currencies(currency_list, url="https://", handle=output_stream)

    output_content = output_stream.getvalue()
    self.assertIn(error_phrase_regex, output_content)


# Тесты
class TestStreamWrite(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")

        self.wrapped = wrapped

    def test_logging_error(self):
        with self.assertRaises(exceptions.RequestException):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("RequestException", logs)



# Запуск тестов
unittest.main(argv=[''], verbosity=2, exit=False)