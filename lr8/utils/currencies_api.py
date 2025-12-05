import sys
import functools
import io

def trace(func=None, *, handle=sys.stdout):
      print(f"decorated func: {func}, {handle}")
      if func is None:
          print('func is None')
          return lambda func: trace(func, handle=handle)
      else:
          print(f'{func.__name__}, {handle}')

      @functools.wraps(func)
      def inner(*args, **kwargs):
          handle.write(f"Using handling output\n")
          # print(func.__name__, args, kwargs)
          return func(*args, **kwargs)

      # print('return inner')
      return inner

nonstandardstream = io.StringIO()

@trace(handle=nonstandardstream)
def increm(x):
    """Инкремент"""
    # print("Инкремент")
    return x+1
@trace(handle=nonstandardstream)
def increm(x):
    """Инкремент"""
    # print("Инкремент")
    return x+1

increm(2)

nonstandardstream.getvalue()

import functools
import requests
import sys
import io

def get_currencies(currency_codes: list, url:str = "https://www.cbr-xml-daily.ru/daily_json.js", handle=sys.stdout)->dict:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """
    try:

        response = requests.get(url)

        # print(response.status_code)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        # print(data)
        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    currencies[code] = data["Valute"][code]["Value"]
                else:
                    currencies[code] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        # print(f"Ошибка при запросе к API: {e}", file=handle)
        handle.write(f"Ошибка при запросе к API: {e}")
        # raise ValueError('Упали с исключением')
        raise requests.exceptions.RequestException('Упали с исключением')

# Пример использования функции:
currency_list = ['USD', 'EUR', 'GBP', 'NNZ']

try:
    currency_data = get_currencies(currency_list, url='https://www.cbr-xml-daily.ru/daily_json.js')
    if currency_data:
         print(currency_data)
except:
    pass

import unittest
from requests import exceptions

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

    with self.assertRaises(requests.exceptions.RequestException):
      currency_data = get_currencies(currency_list, url="https://")

  def test_error_message_in_stream(self):
    error_phrase_regex = "Ошибка при запросе к API"
    stream = io.StringIO()
    currency_list = ['USD']

    try:
      get_currencies(currency_list, url="https://", handle=stream)
    except requests.exceptions.RequestException:
      pass

    stream_content = stream.getvalue()
    self.assertRegex(stream_content, error_phrase_regex)





# Запуск тестов
if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

import sys

def trace(func=None, *, handle=sys.stdout):
    # print(f"decorated func: {func}, {handle}")
    if func is None:
        # print('func is None')
        return lambda func: trace(func, handle=handle)
    # else:
    #   print(f'{func.__name__}, {handle}')

    @functools.wraps(func)
    def inner(*args, **kwargs):
        handle.write(f"Using handling output\n")
        # print(func.__name__, args, kwargs)
        return func(*args, **kwargs)

    # print('return inner')
    return inner

import io
f = io.StringIO()

f.write("Hello from teacher!\n")
f.write('This is second line')

# f.seek(0)
# print(f.read())

# f.seek(0)
# print(f.read())

f.getvalue()

import unittest
import io


# Тесты
class TestStreamWrite(unittest.TestCase):


  def setUp(self):
    self.nonstandardstream = io.StringIO()


    try:
      self.get_currencies = get_currencies(['USD'],
                                         url="https://www.cbr-xml-daily.ru/daily_json.js",
                                         handle=self.nonstandardstream)
    except:
      pass
    # self.trace = trace(get_currencies, handle=self.nonstandardstream)


  def test_writing_stream(self):
    stream_content = self.nonstandardstream.getvalue()
    self.assertIn("Ошибка при запросе к API", stream_content)


  def tearDown(self):
    del self.nonstandardstream
