# Отчет по лабораторной работе: Декораторы и логирование

## 1. Исходный код декоратора с параметрами

```python
import functools
import logging

def logger(func=None, *, handle=sys.stdout):
    """
    Декоратор для логирования функций
    Args:
        func: Функция для логирования
        handle: Поток для записи логов (по умолчанию sys.stdout)
    Returns:
        Обернутая функция с логированием
    """
    if func is None:
        return lambda func: logger(func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        # Логирование старта вызова
        infoMsg = f"Старт вызова {func.__name__} с аргументами: args={args}, kwargs={kwargs}"
        if isinstance(handle, logging.Logger):
            handle.info(f"INFO: {infoMsg}")
        else:
            handle.write(f"INFO: {infoMsg}")
        
        try:
            result = func(*args, **kwargs)
            # Логирование успешного завершения
            success_msg = f"Успешное завершение {func.__name__} с результатом: {result}\n"
            if isinstance(handle, logging.Logger):
                handle.info(f"INFO: {success_msg}")
            else:
                handle.write(f"INFO: {success_msg}")
            return result
        except Exception as e:
            # Логирование ошибки
            errorMsg = f"Ошибка в {func.__name__}: {type(e).__name__}: {e}\n"
            if isinstance(handle, logging.Logger):
                handle.error(f"ERROR: {errorMsg}")
            else:
                handle.write(f"ERROR: {errorMsg}")
            raise

    return inner
```

## 2. Исходный код get_currencies (без логирования)

```python
import requests

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
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    currencies[code] = data["Valute"][code]["Value"]
                else:
                    currencies[code] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        if isinstance(handle, logging.Logger):
            log.error(f"Ошибка при запросе к API: {e}")
        else:
            handle.write(f"Ошибка при запросе к API: {e}")
        raise requests.exceptions.RequestException('Упали с исключением')
```

## 3. Демонстрационный пример (квадратное уравнение)

```python
import logging
import math

logging.basicConfig(
    filename="quadratic.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

def solve_quadratic(a, b, c):
    """
    Находит корни квадратного уравнения.
    Args:
        a (float): Коэффициент при x^2
        b (float): Коэффициент при x
        c (float): Свободный член
    Returns:
        tuple: Кортеж с корнями уравнения. Если корней нет, возвращает None.
    """
    logging.info(f"Solving equation: {a}x^2 + {b}x + {c} = 0")

    # Ошибка типов
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            logging.critical(f"Parameter '{name}' must be a number, got: {value}")
            raise TypeError(f"Coefficient '{name}' must be numeric")

    # Ошибка: a == 0
    if a == 0:
        logging.error("Coefficient 'a' cannot be zero")
        raise ValueError("a cannot be zero")

    d = b*b - 4*a*c
    logging.debug(f"Discriminant: {d}")

    if d < 0:
        logging.warning("Discriminant < 0: no real roots")
        return None

    if d == 0:
        x = -b / (2*a)
        logging.info("One real root")
        return (x,)

    root1 = (-b + math.sqrt(d)) / (2*a)
    root2 = (-b - math.sqrt(d)) / (2*a)
    logging.info("Two real roots computed")
    return root1, root2
```

## 4. Скриншоты / фрагменты логов

### Логи успешного выполнения get_currencies:
```
INFO: Старт вызова get_currencies с аргументами: args=(['USD'],), kwargs={}
INFO: Успешное завершение get_currencies с результатом: {'USD': 79.3398}
```

### Логи при ошибке:
```
INFO: Старт вызова get_currencies с аргументами: args=(['USD'],), kwargs={'url': 'https://', 'handle': <_io.StringIO object at 0x...>}
ERROR: Ошибка в get_currencies: RequestException: Упали с исключением
```

### Логи из quadratic.log (фрагмент):
```
DEBUG: Discriminant: 16.0
INFO: Two real roots computed
```

## 5. Тесты

### Тесты функции get_currencies

```python
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
```

### Тесты декоратора, StringIO

```python
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
```