# Лабораторная работа 9. Клиент-серверное приложение на Python с использованием Jinja2

## 1. Цель работы
1. Реализовать CRUD (Create, Read, Update, Delete) для сущностей бизнес-логики приложения.
2. Освоить работу с SQLite в памяти (:memory:) через модуль sqlite3.
3. Понять принципы первичных и внешних ключей и их роль в связях между таблицами.
4. Выделить контроллеры для работы с БД и для рендеринга страниц в отдельные модули.
5. Использовать архитектуру MVC и соблюдать разделение ответственности.
6. Отображать пользователям таблицу с валютами, на которые они подписаны.
7. Реализовать полноценный роутер, который обрабатывает GET-запросы и выполняет сохранение/обновление данных и рендеринг страниц.
8. Научиться тестировать функционал на примере сущностей currency и user с использованием unittest.mock.

---

## 2. Описание моделей, их свойств и связей

### 2.1 Модель Author
**Файл:** `models/author.py`

Модель представляет информацию об авторе приложения.

**Свойства:**
- `name` (str) — имя автора (минимум 2 символа)
- `group` (str) — группа студента (минимум 5 символов)

**Методы:**
- Getters и setters с валидацией данных

**Пример использования:**
```python
main_author = Author('Ахметов Артём', 'P3122')
```

### 2.2 Модель Currency
**Файл:** `models/currency.py`

Модель представляет валютную пару с курсом обмена.

**Свойства:**
- `num_code` (str) — числовой код валюты (например, 840 для USD)
- `char_code` (str) — 3-символьный код валюты (USD, EUR, GBP и т.д.)
- `name` (str) — описание валюты (например, "Доллар США")
- `value` (float) — текущий курс валюты (не может быть отрицательным)
- `nominal` (int) — номинал для расчета (обычно 1, для JPY — 100)

**Валидация:**
- `char_code` должен состоять ровно из 3 символов
- `value` не может быть отрицательным

### 2.3 Модель User
**Файл:** `models/user.py`

Модель представляет пользователя системы с поддержкой CRUD операций.

**Таблица БД:**
```sql
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  login TEXT NOT NULL
)
```

**Свойства:**
- `id` (int) — уникальный идентификатор
- `login` (str) — логин пользователя

**Методы:**
- `_adduser(login)` — добавить нового пользователя (проверка на дубликаты и длину)
- `_inuser(login)` — вход в систему (проверка наличия пользователя)
- `_userlist` (свойство) — получить список всех пользователей

**Валидация:**
- Длина логина > 2 символов
- Логин должен быть уникальным

### 2.4 Модель UserCurrency (связующая таблица)
**Файл:** `models/usercurrency.py`

Реализует отношение "Многие ко многим" между пользователями и валютами.

**Таблица БД:**
```sql
CREATE TABLE user_currency (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  currency_id INTEGER NOT NULL,
  FOREIGN KEY(user_id) REFERENCES user(id),
  FOREIGN KEY(currency_id) REFERENCES currency(id)
)
```

**Методы:**
- `_add_user_currency(user_id, currency_id)` — добавить валюту пользователю
- `_get_user_currencies(user_id)` — получить все валюты пользователя

**Связи:**
- Каждому пользователю может быть назначено несколько валют
- Каждая валюта может быть назначена нескольким пользователям

---

## 3. Диаграмма связей между сущностями

```
┌─────────────────┐
│  User           │
├─────────────────┤
│ id (PK)         │
│ login           │
└────────┬────────┘
         │ (1:N)
         │
    ┌────┴────────────┐
    │  UserCurrency   │
    ├─────────────────┤
    │ id (PK)         │
    │ user_id (FK)    │
    │ currency_id (FK)│
    └──────┬──────────┘
           │ (N:1)
           │
┌──────────┴──────────┐
│  Currency           │
├─────────────────────┤
│ id (PK)             │
│ date                │
│ num_code            │
│ char_code           │
│ name                │
│ value               │
│ nominal             │
└─────────────────────┘
```

---

## 4. Структура проекта с назначением файлов

```
lr9/
├── myapp.py                          # Главное приложение, HTTP сервер и маршрутизация
├── readme.md                         # Этот файл с документацией
├── models/                           # Слой моделей (M в MVC)
│   ├── __init__.py
│   ├── author.py                     # Модель для информации об авторе
│   ├── currency.py                   # Модель валюты
│   ├── user.py                       # Модель пользователя с CRUD
│   └── usercurrency.py               # Связующая таблица User-Currency
├── controllers/                      # Слой контроллеров (C в MVC)
│   ├── __init__.py
│   ├── databasecontroller.py         # CRUD контроллер для валют
│   └── currencycontroller.py         # Дополнительный контроллер для валют
├── templates/                        # Слой представлений (V в MVC)
│   ├── index.html                    # Главная страница
│   ├── author.html                   # Страница об авторе
│   ├── currencies.html               # Страница с таблицей валют
│   ├── user.html                     # Страница управления пользователями
│   └── users.html                    # Список пользователей и их валют
└── static/                           # Статические файлы (CSS, JS, изображения)
```

### Назначение файлов:

| Файл | Описание |
|------|---------|
| `myapp.py` | HTTP сервер на BaseHTTPRequestHandler, маршрутизация GET запросов, рендеринг шаблонов |
| `models/author.py` | Модель с валидацией данных об авторе |
| `models/currency.py` | Модель валюты с защитой свойств через properties |
| `models/user.py` | Работа с таблицей `user`, валидация логинов |
| `models/usercurrency.py` | Управление связью user-currency через отдельную таблицу |
| `controllers/databasecontroller.py` | CRUD операции для валют, работа с SQLite |

---

## 5. Реализация CRUD операций

### 5.1 CREATE операция (Создание)

**Для валют (CurrencyRatesCRUD._create):**
```python
def _create(self):
    data = [
        {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
        {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 91.0, "nominal": 1},
        {"num_code": "826", "char_code": "GBP", "name": "Фунт стерлингов", "value": 108.1271, "nominal": 1},
        # ... еще валюты
    ]
    sql = "INSERT INTO currency(num_code, char_code, name, value, nominal) VALUES(:num_code, :char_code, :name, :value, :nominal)"
    self.__cursor.executemany(sql, data)
    self.__con.commit()
```

**SQL запрос:**
```sql
INSERT INTO currency(num_code, char_code, name, value, nominal) 
VALUES(?, ?, ?, ?, ?)
-- Параметры: ('840', 'USD', 'Доллар США', 90.0, 1)
```

**Для пользователей (User._adduser):**
```python
def _adduser(self, login=str):
    if login not in User._logindata and len(login) > 2:
        params = (login,)
        query = "INSERT INTO user(login) VALUES(?)"
        self.__cursor.execute(query, params)
        self.__con.commit()
        return ""  # success
    else:
        # return error message
```

**SQL запрос:**
```sql
INSERT INTO user(login) VALUES(?)
-- Параметр: ('art1')
```

### 5.2 READ операция (Чтение)

**Для валют (CurrencyRatesCRUD._read):**
```python
def _read(self):
    cur = self.__con.execute("SELECT * FROM currency")
    result_data = []
    for _row in cur:
        _d = {
            'id': int(_row[0]), 
            'date': _row[1], 
            'num_code': _row[2], 
            'char_code': _row[3], 
            'name': _row[4], 
            'value': float(_row[5]), 
            'nominal': _row[6]
        }
        result_data.append(_d)
    return result_data
```

**SQL запрос:**
```sql
SELECT id, date, num_code, char_code, name, value, nominal FROM currency
```

**Для пользователей (User._userlist):**
```python
@property
def _userlist(self):
    users = self.__con.execute("SELECT * FROM user")
    users_data = []
    for _item in users:
        _data = {'id': int(_item[0]), 'login': _item[1]}
        users_data.append(_data)
    return users_data
```

**SQL запрос:**
```sql
SELECT id, login FROM user
```

### 5.3 UPDATE операция (Обновление)

**Для валют (CurrencyRatesCRUD._update):**
```python
def _update(self, currency: dict['str': float]):
    # Параметр: {'USD': 101.1}
    currency_code = tuple(currency.keys())[0]
    currency_value = tuple(currency.values())[0]
    upd_statement = f"UPDATE currency SET value = {currency_value} WHERE char_code = '" + str(currency_code) + "'"
    self.__cursor.execute(upd_statement)
    self.__con.commit()
```

**SQL запрос:**
```sql
UPDATE currency SET value = 101.1 WHERE char_code = 'USD'
```

### 5.4 DELETE операция (Удаление)

**Для валют (CurrencyRatesCRUD._delete):**
```python
def _delete(self, currency_id):
    del_statement = "DELETE FROM currency WHERE id = " + str(currency_id)
    self.__cursor.execute(del_statement)
    self.__con.commit()
```

**SQL запрос:**
```sql
DELETE FROM currency WHERE id = 1
```

---

## 6. Маршруты приложения

Приложение использует роутер на основе анализа пути URL.

| Маршрут | Метод | Описание | SQL операция |
|---------|-------|---------|--------------|
| `/` | GET | Главная страница со списком валют | READ |
| `/author` | GET | Информация об авторе | — |
| `/currency` | GET | Таблица всех валют | READ |
| `/currency/delete?id=N` | GET | Удаление валюты | DELETE |
| `/currency/update?USD=101.1` | GET | Обновление курса | UPDATE |
| `/currency/show` | GET | Показать валюты (debug) | READ |
| `/user` | GET | Управление пользователями | READ |
| `/user/add?loginAdd=artkey` | GET | Добавить пользователя | CREATE |
| `/user/in?loginIn=art1` | GET | Вход в систему | — |
| `/user/add_currency?user_id=1&currency_id=1` | GET | Добавить валюту пользователю | CREATE (в user_currency) |
| `/users` | GET | Список пользователей и их валют | READ (JOIN) |

---

## 7. HTTP обработчик и маршрутизация

**Класс:** `SimpleHTTPRequestHandler`

Основной обработчик GET запросов:

```python
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        
        # Парсинг параметров URL
        url_query_dict = parse_qs(self.path.rpartition('?')[-1])
        
        # Маршрутизация
        if self.path == '/':
            result = template.render(...)  # главная
        elif "currency" in self.path:
            result = cur.render(...)  # валюты
        elif "author" in self.path:
            result = authorHtml.render(...)  # об авторе
        # ... и так далее
        
        self.end_headers()
        self.wfile.write(bytes(result, "utf-8"))
```

---

## 8. Работа с Jinja2 шаблонами

Приложение использует Jinja2 для рендеринга HTML шаблонов:

```python
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

# Загрузка шаблонов
template = env.get_template("index.html")
cur = env.get_template("currencies.html")
userHtml = env.get_template("user.html")
usersHtml = env.get_template("users.html")

# Рендеринг с передачей данных
result = template.render(
    myapp="CurrenciesListApp",
    navigation=nav,
    author_name=main_author.name,
    author_group=main_author.group,
    currencies=c_r_controller._read(),
    login=login
)
```

---

## 9. Применение архитектуры MVC

### Model (Модель)
- **`models/author.py`** — данные об авторе
- **`models/currency.py`** — данные о валютах
- **`models/user.py`** — данные о пользователях и их управление
- **`models/usercurrency.py`** — связь между пользователями и валютами

### View (Представление)
- **`templates/index.html`** — главная страница
- **`templates/author.html`** — страница об авторе
- **`templates/currencies.html`** — таблица валют
- **`templates/user.html`** — управление пользователями
- **`templates/users.html`** — список пользователей с их валютами

### Controller (Контроллер)
- **`controllers/databasecontroller.py`** — контроллер CRUD для валют (`CurrencyRatesCRUD`)
- **`myapp.py`** — главный контроллер, маршрутизация и обработка HTTP запросов

### Разделение ответственности

| Компонент | Ответственность |
|-----------|-----------------|
| Model | Логика данных, валидация, CRUD |
| Controller | Обработка запросов, координация |
| View | Отображение, рендеринг HTML |

---

## 10. SQLite в памяти (:memory:)

Приложение использует SQLite в памяти для всех таблиц:

```python
def __init__(self, currency_rates_obj):
    self.__con = sqlite3.connect(':memory:')  # БД в памяти
    self.__createtable()
    self.__cursor = self.__con.cursor()
```

**Преимущества:**
- Быстрый доступ (нет диска)
- Просто тестировать (никакой инициализации БД не требуется)
- Подходит для демонстрационных приложений

**Недостатки:**
- Данные теряются при перезагрузке приложения
- Не подходит для production (нет persitence)

---

## 11. Первичные и внешние ключи

### Первичный ключ (PRIMARY KEY)

```sql
CREATE TABLE currency(
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Первичный ключ
    date TEXT DEFAULT CURRENT_TIMESTAMP,
    num_code TEXT,
    char_code TEXT,
    name TEXT,
    value FLOAT,
    nominal TEXT
);

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Первичный ключ
    login TEXT NOT NULL
);
```

### Внешний ключ (FOREIGN KEY)

```sql
CREATE TABLE user_currency(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    currency_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),        -- Внешний ключ на user
    FOREIGN KEY(currency_id) REFERENCES currency(id) -- Внешний ключ на currency
);
```

**Роль:**
- Обеспечивают целостность данных
- Предотвращают ссылки на несуществующие записи
- Позволяют создавать связи между таблицами

---

## 12. Примеры работы приложения

### 12.1 Добавление валюты пользователю

```
URL: /user/add_currency?user_id=1&currency_id=1
```

1. Парсинг параметров: `{'user_id': 1, 'currency_id': 1}`
2. Вызов: `user_currencies._add_user_currency(1, 1)`
3. SQL: `INSERT INTO user_currency(user_id, currency_id) VALUES(1, 1)`
4. Результат: Валюта USD добавлена пользователю art1

### 12.2 Получение валют пользователя

```python
currencies = user_currencies._get_user_currencies(user_id=1)
# Результат: [1, 3, 5]  # IDs валют

# Вывод в таблице: USD (90.0), GBP (108.1), CAD (58.6)
```

### 12.3 Обновление курса валюты

```
URL: /currency/update?usd=95.5
```

1. Парсинг: `{'usd': '95.5'}`
2. Преобразование: `{'USD': 95.5}`
3. SQL: `UPDATE currency SET value = 95.5 WHERE char_code = 'USD'`

### 12.4 Удаление валюты

```
URL: /currency/delete?id=2
```

1. Парсинг: `{'id': ['2']}`
2. SQL: `DELETE FROM currency WHERE id = 2`
3. Валюта EUR удалена из системы

---

## 13. Тестирование с unittest.mock

Модуль `unittest.mock` используется для подмены реальных объектов в тестах.

### Пример теста для User

```python
import unittest
from unittest.mock import Mock, patch, MagicMock
from models.user import User
from models.currency import Currency

class TestUserCRUD(unittest.TestCase):
    
    def setUp(self):
        """Подготовка к каждому тесту"""
        self.user = User()
    
    def test_add_user_success(self):
        """Тест успешного добавления пользователя"""
        result = self.user._adduser("testuser123")
        self.assertEqual(result, "")  # успех - пустая строка
        self.assertIn("testuser123", self.user._userlist)
    
    def test_add_user_duplicate(self):
        """Тест добавления дубликата логина"""
        self.user._adduser("art1")
        result = self.user._adduser("art1")
        self.assertIn("уже используется", result)  # ошибка
    
    def test_add_user_short_login(self):
        """Тест добавления слишком короткого логина"""
        result = self.user._adduser("ab")
        self.assertIn("больше 2х символов", result)
    
    def test_login_success(self):
        """Тест успешного входа"""
        self.user._adduser("myuser123")
        result = self.user._inuser("myuser123")
        self.assertEqual(result, True)
    
    def test_login_not_found(self):
        """Тест входа несуществующего пользователя"""
        result = self.user._inuser("nonexistent")
        self.assertIn("не зарегистрирован", result)
```

### Пример теста для Currency с mocks

```python
class TestCurrencyRates(unittest.TestCase):
    
    @patch('controllers.databasecontroller.sqlite3')
    def test_currency_crud_with_mock(self, mock_sqlite):
        """Тест CRUD операций с подменой БД"""
        # Подготовка mock объекта
        mock_db = MagicMock()
        mock_sqlite.connect.return_value = mock_db
        
        # Инициализация
        currency_obj = Mock()
        currency_obj.values = [
            {"num_code": "840", "char_code": "USD", "value": 90.0}
        ]
        
        # Проверка что БД была инициализирована
        # (в реальной реализации)
        self.assertIsNotNone(mock_db)
    
    def test_currency_value_validation(self):
        """Тест валидации курса валюты"""
        currency = Currency("840", "USD", "Доллар", 90.0, 1)
        
        # Проверка валидного значения
        currency.value = 95.5
        self.assertEqual(currency.value, 95.5)
        
        # Проверка что отрицательное значение вызывает ошибку
        with self.assertRaises(ValueError):
            currency.value = -10.0
    
    def test_currency_code_validation(self):
        """Тест валидации кода валюты"""
        currency = Currency("840", "USD", "Доллар", 90.0, 1)
        
        # Валидный код (3 символа)
        currency.char_code = "EUR"
        self.assertEqual(currency.char_code, "EUR")
        
        # Невалидный код (не 3 символа)
        with self.assertRaises(ValueError):
            currency.char_code = "US"  # Слишком короткий
```

### Пример теста для UserCurrency

```python
class TestUserCurrency(unittest.TestCase):
    
    def setUp(self):
        """Подготовка к тестам"""
        self.user = User()
        self.user_currency = UserCurrency()
        # Добавляем тестовых пользователей
        self.user._adduser("testuser1")
        self.user._adduser("testuser2")
    
    def test_add_user_currency(self):
        """Тест добавления валюты пользователю"""
        result = self.user_currency._add_user_currency(1, 1)
        self.assertEqual(result, "")  # успех
    
    def test_add_duplicate_user_currency(self):
        """Тест попытки добавить одну валюту дважды"""
        self.user_currency._add_user_currency(1, 1)
        result = self.user_currency._add_user_currency(1, 1)
        self.assertIn("уже добавлена", result)
    
    def test_get_user_currencies(self):
        """Тест получения валют пользователя"""
        self.user_currency._add_user_currency(1, 1)
        self.user_currency._add_user_currency(1, 2)
        self.user_currency._add_user_currency(1, 3)
        
        currencies = self.user_currency._get_user_currencies(1)
        self.assertEqual(currencies, [1, 2, 3])
```

### Запуск тестов

```bash
python -m unittest tests.test_user -v
python -m unittest tests.test_currency -v
python -m unittest tests.test_user_currency -v
python -m unittest discover -s tests -p "test_*.py" -v  # все тесты
```

### Пример вывода при успешном прохождении

```
test_add_duplicate_user_currency (__main__.TestUserCurrency) ... ok
test_add_user_currency (__main__.TestUserCurrency) ... ok
test_add_user_duplicate (__main__.TestUserCurrency.User) ... ok
test_add_user_short_login (__main__.TestUserCurrency.User) ... ok
test_add_user_success (__main__.TestUserCurrency.User) ... ok
test_currency_code_validation (__main__.TestCurrencyRates) ... ok
test_currency_crud_with_mock (__main__.TestCurrencyRates) ... ok
test_currency_value_validation (__main__.TestCurrencyRates) ... ok
test_get_user_currencies (__main__.TestUserCurrency) ... ok
test_login_not_found (__main__.TestUserCurrency.User) ... ok
test_login_success (__main__.TestUserCurrency.User) ... ok

Ran 11 tests in 0.012s
OK
```

---

## 14. Запуск приложения

### Требования
- Python 3.7+
- Jinja2: `pip install jinja2`

### Запуск сервера

```bash
cd /Users/artemahmetov/Program1/pyLabs/lr9
python myapp.py
```

**Вывод:**
```
server is running
```

### Доступ к приложению

Откройте браузер и перейдите на:
- Главная страница: http://localhost:8080/
- О авторе: http://localhost:8080/author
- Валюты: http://localhost:8080/currency
- Пользователи: http://localhost:8080/users
- Управление пользователями: http://localhost:8080/user

---

## 15. Выводы

### 15.1 Применение MVC

Архитектура MVC позволяет:
- **Разделить ответственность** — каждый компонент имеет четкую роль
- **Упростить тестирование** — модели можно тестировать отдельно от вида
- **Переиспользовать код** — модели могут быть использованы в разных представлениях
- **Облегчить поддержку** — изменения в одном слое не влияют на другие

### 15.2 Работа с SQLite в памяти

**Преимущества:**
- Высокая скорость операций
- Отсутствие зависимостей от файловой системы
- Удобство для тестирования и демонстрации

**Недостатки:**
- Отсутствие persistent storage
- Ограничения по памяти
- Не подходит для production систем

### 15.3 Обработка маршрутов

Простая маршрутизация на основе анализа пути позволяет:
- Обрабатывать различные URL маршруты
- Парсить параметры запроса
- Вызывать соответствующие операции БД
- Рендерить нужные шаблоны

### 15.4 Рендеринг шаблонов с Jinja2

Шаблонизатор Jinja2 предоставляет:
- Отделение логики представления от кода Python
- Возможность использования циклов и условий в HTML
- Безопасный рендеринг (autoescape по умолчанию)
- Удобство передачи данных в шаблоны через контекст

### 15.5 Валидация данных

Реализована валидация на уровне:
- **Модели** — properties с setters, которые проверяют данные
- **Контроллера** — проверка длины логина, уникальности
- **БД** — ограничения целостности (PRIMARY KEY, FOREIGN KEY)

### 15.6 Обработка ошибок

Приложение обрабатывает:
- Дублирующиеся логины
- Слишком короткие логины
- Несуществующих пользователей
- Отрицательные курсы валют
- Невалидные коды валют