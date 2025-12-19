class User():
    __dataUsers = {}
    __idVal = 0

    def __init__(self, id: int, name: str, currencies: list = None):
        self.__id: int = id
        self.__name: str = name
        self.__currencies: list = currencies if currencies is not None else []

    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def currencies(self):
        return self.__currencies
    
    @classmethod
    def userUp(cls, name: str):
        if name is not None:
            user = cls(cls.__idVal, name, [])
            cls.__dataUsers[cls.__idVal] = user
            cls.__idVal += 1
            return user
        return None
    
    @classmethod
    def dataUsers(cls):
        return cls.__dataUsers
    
    def __repr__(self):
        return f"sign(id={self.__id}, name={self.__name})"
    
    def addCurrency(self, currency_data):
        """Добавить валюту в список пользователя"""
        # Поддерживаем разные форматы входных данных: строка (код), объект Currency или dict
        currency_id = None
        from .user_currency import UserCurrency

        if isinstance(currency_data, str):
            currency_id = currency_data
        elif hasattr(currency_data, 'char_code'):
            currency_id = currency_data.char_code
        elif hasattr(currency_data, 'id') and getattr(currency_data, 'id') is not None:
            currency_id = currency_data.id
        elif isinstance(currency_data, dict):
            currency_id = currency_data.get('char_code') or currency_data.get('id') or currency_data.get('code')

        if currency_id is None:
            return False

        # Создаём связь в таблице
        UserCurrency.create_link(self.__id, currency_id)

        if currency_id not in self.__currencies:
            self.__currencies.append(currency_id)
        return True
    
    def subscribeCurrency(self, currency_code: str):
        """Подписаться на валюту по коду (USD, EUR и т.д.)"""
        from .user_currency import UserCurrency

        if currency_code not in self.__currencies:
            UserCurrency.create_link(self.__id, currency_code)
            self.__currencies.append(currency_code)
            return True
        return False
    
    def unsubscribeCurrency(self, currency_code: str):
        """Отписаться от валюты"""
        try:
            from .user_currency import UserCurrency
        except Exception:
            from models.user_currency import UserCurrency

        removed = False
        if currency_code in self.__currencies:
            self.__currencies.remove(currency_code)
            removed = True

        # Удаляем связь
        link_removed = UserCurrency.remove_link(self.__id, currency_code)
        return removed or link_removed
    
    @classmethod
    def checkUser(cls, id: str, curr):
        """Проверить пользователя и добавить ему валюты"""
        try:
            user_id = int(id)
            if user_id in cls.__dataUsers:
                user = cls.__dataUsers[user_id]
                if isinstance(curr, dict):
                    user.addCurrency(curr)
                elif isinstance(curr, list):
                    for currency in curr:
                        user.addCurrency(currency)
                return user
        except (ValueError, TypeError):
            pass
        return None
    
    @classmethod
    def authenticate(cls, name: str):
        """Авторизовать пользователя по имени"""
        for user_id, user in cls.__dataUsers.items():
            if user.name == name:
                return user
        return None

