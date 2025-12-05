class User():
    __dataUsers = {}
    __idVal = 0

    def __init__(self, id: int, login: str, password: str, currencies: list = None):
        self.__id: int = id
        self.__login: str = login
        self.__password: str = password
        self.__currencies: list = currencies if currencies is not None else []

    @property
    def id(self):
        return self.__id
    
    @property
    def login(self):
        return self.__login
    
    @property
    def password(self):
        return self.__password
    
    @property
    def currencies(self):
        return self.__currencies
    
    @classmethod
    def userUp(cls, name: str, password: str):
        if name is not None and password is not None:
            user = cls(cls.__idVal, name, password, [])
            cls.__dataUsers[cls.__idVal] = user
            cls.__idVal += 1
            return user
        return None
    
    @classmethod
    def dataUsers(cls):
        return cls.__dataUsers
    
    def __repr__(self):
        return f"sign(id={self.__id}, login={self.__login})"
    
    def addCurrency(self, currency_data):
        """Добавить валюту в список пользователя"""
        if currency_data not in self.__currencies:
            self.__currencies.append(currency_data)
        return True
    
    def subscribeCurrency(self, currency_code: str):
        """Подписаться на валюту по коду (USD, EUR и т.д.)"""
        if currency_code not in self.__currencies:
            self.__currencies.append(currency_code)
            return True
        return False
    
    def unsubscribeCurrency(self, currency_code: str):
        """Отписаться от валюты"""
        if currency_code in self.__currencies:
            self.__currencies.remove(currency_code)
            return True
        return False
    
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
    def authenticate(cls, login: str, password: str):
        """Авторизовать пользователя по логину и паролю"""
        for user_id, user in cls.__dataUsers.items():
            if user.login == login and user.password == password:
                return user
        return None

