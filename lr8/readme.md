# Лабораторная работа 8. Клиент-серверное приложение на Python с использованием Jinja2
## 1. Цель работы
1. Создать простое клиент-серверное приложение на Python без серверных фреймворков.

2. Освоить работу с HTTPServer и маршрутизацию запросов.

3. Применять шаблонизатор Jinja2 для отображения данных.

4. Реализовать модели предметной области (User, Currency, UserCurrency, App, Author) с геттерами и сеттерами.

5. Структурировать код в соответствии с архитектурой MVC.

6. Получать данные о курсах валют через функцию get_currencies и отображать их пользователям.

7. Реализовать функциональность подписки пользователей на валюты и отображение динамики их изменения.

8. Научиться создавать тесты для моделей и серверной логики.

## 2. Описание предметной области
### Модели
1. Author

        name — имя автора

        group — учебная группа

2. App

        name — название приложения

        version — версия приложения

        author — объект Author

3. User

        id — уникальный идентификатор

        name — имя пользователя

4. Currency

        id — уникальный идентификатор

        num_code — цифровой код

        char_code — символьный код

        name — название валюты

        value — курс

        nominal — номинал (за сколько единиц валюты указан курс)

Пример XML:

```
<Valute ID="R01280">
 <NumCode>360</NumCode>
 <CharCode>IDR</CharCode>
 <Nominal>10000</Nominal>
 <Name>Рупий</Name>
 <Value>48,6178</Value>
</Valute>
```
1. UserCurrency

        id — уникальный идентификатор

        user_id — внешний ключ к User

        currency_id — внешний ключ к Currency

        Реализует связь «много ко многим» между пользователями и валютами.

## 3. Архитектура проекта (MVC)
Cтруктура папок:
```
lr8/
├── myapp.py # основной файл с роутами и подключениями
├── models/
│   ├── __init__.py
│   ├── app.py
│   ├── author.py
│   ├── currency.py
│   ├── user.py
│   ├── user_currency.py
│   └── testModels.py # тест моделей
├── templates/
│   ├── index.html # основной файл html
│   └── pages/
│       ├── bank/
│       │   └── index.html
│       ├── currencies/
│       │   └── index.html
│       └── sign/
│           └── index.html
├── utils/
│   ├── currencies_api.py # реализация get_currency
│   └── testCurrencies.py # тест api
├── testController.py # тетс роутов и контролеров
├── currency.log # файл с логами ф-ии get_currency
└── readme.md
```
Разделение ответственности (MVC):

Models — классы предметной области, геттеры и сеттеры.

Views (шаблоны Jinja2) — отображение данных для пользователя (templates/).

Controller (HTTPServer) — маршрутизация, обработка запросов, вызов моделей и шаблонов.
## 4. Описание реализации:

### 4.1. Реализация моделей и их свойств (геттеры/сеттеры)
Модели реализованы как классы в папке `models/`. Каждый класс имеет:
- Конструктор `__init__` для инициализации атрибутов.
- Геттеры (`@property`) для чтения приватных атрибутов (начинаются с `_` или `__`).
- Сеттеры (`@property_name.setter`) для записи с валидацией (например, проверка типов, длин строк, допустимых значений).

Примеры:
- `Currency`: сеттеры для `char_code` проверяют код из списка валют; сеттеры для `id`, `num_code`, `name` автоматически заполняют поля на основе `char_code`.
- `User`: методы для подписки/отписки на валюты, хранение списка валют в атрибуте `currencies`.

### 4.2. Реализация маршрутов и обработка запросов
Маршруты реализованы в классе `SimpleHTTPRequestHandler` в `myapp.py` методом `do_GET()`.
- Парсинг URL: `urlparse(self.path)` для пути и query-параметров.
- Определение маршрута: проверка `path` (например, `if path == '' or path == 'index.html'`).
- Обработка query-параметров: `parse_qs()` для извлечения данных (например, `user_id`, параметры форм).
- Вызов моделей: получение данных из `User`, `Currency`.
- Рендеринг шаблонов: передача данных в Jinja2 и отправка HTML-ответа.

### 4.3. Использование шаблонизатора Jinja2
Jinja2 инициализируется в `myapp.py`:
```python
env = Environment(
    loader=PackageLoader("myapp"),  # Загружает шаблоны из пакета "myapp" (папка templates/)
    autoescape=select_autoescape()   # Автоматическое экранирование HTML для безопасности
)
```
- Загрузка шаблона: `template = env.get_template("index.html")`.
- Рендеринг: `template.render(**data)` — передача словаря `data` с переменными (например, `navigation`, `current_user`).
- В шаблонах: `{{ variable }}` для вывода, `{% for %}` для циклов, `{% if %}` для условий.

### 4.4. Интеграция функции get_currencies
Функция `get_currencies` из `utils/currencies_api.py` получает курсы с API ЦБ РФ.
- Вызов: `data = get_currencies(currency_list)` в начале `myapp.py`.
- Создание объектов `Currency`: цикл по `data.items()` для инициализации списка `currencies`.
- Передача в шаблоны: `currencies` передаётся как `a_variable` для отображения курсов.
- Обновление: в маршруте `/currencies/subscriptions` курсы запрашиваются заново для актуальности.
## 5. Примеры работы приложения:
    /
![/](./static/Снимок%20экрана%202025-12-20%20в%2000.17.55.png)

    /currencies
![/currencies](./static/Снимок%20экрана%202025-12-20%20в%2000.18.04.png)

    /sign
![/sign](./static/Снимок%20экрана%202025-12-20%20в%2000.18.14.png)

    /currencies/subscriptions
![/currencies/subscriptions](./static/Снимок%20экрана%202025-12-20%20в%2000.18.28.png)
## 7. Тестирование
Вывод результатов тестирования

testCurrencies:
```
test_currency_usd (__main__.TestGetCurrencies.test_currency_usd)
Проверяет наличие ключа в словаре и значения этого ключа ... INFO: INFO: Старт вызова get_currencies с аргументами: args=(['USD'],), kwargs={}
INFO: INFO: Успешное завершение get_currencies с результатом: {'USD': 80.722}

ok
test_get_currency_error (__main__.TestGetCurrencies.test_get_currency_error) ... INFO: INFO: Старт вызова get_currencies с аргументами: args=(['USD'],), kwargs={'url': 'https://', 'handle': <_io.StringIO object at 0x107b3b580>}
ERROR: ERROR: Ошибка в get_currencies: RequestException: Упали с исключением

ok
test_nonexist_code (__main__.TestGetCurrencies.test_nonexist_code) ... INFO: INFO: Старт вызова get_currencies с аргументами: args=(['XYZ'],), kwargs={}
INFO: INFO: Успешное завершение get_currencies с результатом: {'XYZ': "Код валюты 'XYZ' не найден."}

INFO: INFO: Старт вызова get_currencies с аргументами: args=(['XYZ'],), kwargs={}
INFO: INFO: Успешное завершение get_currencies с результатом: {'XYZ': "Код валюты 'XYZ' не найден."}

INFO: INFO: Старт вызова get_currencies с аргументами: args=(['XYZ'],), kwargs={}
INFO: INFO: Успешное завершение get_currencies с результатом: {'XYZ': "Код валюты 'XYZ' не найден."}

ok
test_logging_error (__main__.TestStreamWrite.test_logging_error) ... INFO: INFO: Старт вызова get_currencies с аргументами: args=(['USD'],), kwargs={'url': 'https://invalid'}
ERROR: ERROR: Ошибка в get_currencies: RequestException: Упали с исключением

ok

----------------------------------------------------------------------
Ran 4 tests in 1.163s

OK
Ошибка при запросе к API: HTTPSConnectionPool(host='invalid', port=443): Max retries exceeded with url: / (Caused by NameResolutionError("HTTPSConnection(host='invalid', port=443): Failed to resolve 'invalid' ([Errno 8] nodename nor servname provided, or not known)"))
```

testController.py
```
..
----------------------------------------------------------------------
Ran 2 tests in 0.003s

OK
```

testModels.py
```
....................
----------------------------------------------------------------------
Ran 20 tests in 0.002s

OK
```
## 8. Выводы:
В ходе работы возникали проблемы с правильными настройками роутов, правильно прописанных тестов и работы с модулями, в итоге все решить удалось, как показано в работе. Принципы MVC удалось применить на практике засчет четкой структуры приложения, разделения по различным блокам частей кода и четкого разграничения систем ответственности. Из нового оказалась работа с роутами, jinja2 и подключения курса валют через api в графический интерфейс.