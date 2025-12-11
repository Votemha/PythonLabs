import sys
import io
import functools

def trace(func=None, *, handle=sys.stdout):
    """
    Декоратор для трассировки функций
    Args:
        func: Функция для трассировки
        handle: Поток для записи трассировки (по умолчанию sys.stdout)
    Returns:
        Обернутая функция с трассировкой
    """
    if func is None:
        return lambda func: trace(func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        handle.write(f"Using handling output\n")
        return func(*args, **kwargs)

    return inner

# Пример использования функции
if __name__ == '__main__':
    nonstandardstream = io.StringIO()
    @trace(handle=nonstandardstream)
    def increm(x):
        """Инкремент"""
        # print("Инкремент")
        return x+1

    increm(2)

    nonstandardstream.getvalue()

# Логирование
import logging

log = logging.getLogger("currency")
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
log.addHandler(handler)
log.addHandler(logging.FileHandler("currency.log"))

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

import requests

@logger(handle=log)
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
        if isinstance(handle, logging.Logger):
            log.error(f"Ошибка при запросе к API: {e}")
        else:
            handle.write(f"Ошибка при запросе к API: {e}")
        raise requests.exceptions.RequestException('Упали с исключением')

# Пример использования функции:
if __name__ == '__main__':
    currency_list = ['USD', 'EUR', 'GBP', 'NNZ']

    currency_data = get_currencies(currency_list, url='https://www.cbr-xml-daily.ru/daily_json.js')
    if currency_data:
         print(currency_data)



# Пример функции с логированием и обработкой ошибок
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