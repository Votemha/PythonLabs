class Currency():
    def __init__(self, id: int, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.__id: str = id
        self.__num_code: str = num_code
        self.__char_code: str = char_code
        self.__name: str = name
        self.__value: float = value
        self.__nominal: int = nominal

    @property
    def id(self):
        return self.__id
    
    @property
    def num_code(self):
        return self.__num_code
    
    @property
    def char_code(self):
        return self.__char_code
    
    @char_code.setter
    def char_code(self, char_code: str):
        if type(char_code) == str and char_code in ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD"]:
            self.__char_code = char_code
        else:
            raise ValueError('Ошибка при задании кода валюты')
    
    @property
    def name(self):
        return self.__name
    
    @property
    def value(self):
        return self.__value
    
    @property
    def nominal(self):
        return self.__nominal
    
    @id.setter
    def id(self, id: str):
        if self.__char_code == "USD":
            id = "R01235"
            self.__id = id
        elif self.__char_code == "EUR":
            id = "R01239"
            self.__id = id
        elif self.__char_code == "GBP":
            id = "R01035"
            self.__id = id
        elif self.__char_code == "JPY":
            id = "R01820"
            self.__id = id
        elif self.__char_code == "CHF":
            id = "R01775"
            self.__id = id
        elif self.__char_code == "CAD":
            id = "R01535"
            self.__id = id
        elif self.__char_code == "AUD":
            id = "R01625"
            self.__id = id
        else:
            raise ValueError('Ошибка при задании id валюты')
    
    @num_code.setter
    def num_code(self, num_code: str):
        if self.__char_code == "USD":
            num_code = "840"
            self.__num_code = num_code
        elif self.__char_code == "EUR":
            num_code = "978"
            self.__num_code = num_code
        elif self.__char_code == "GBP":
            num_code = "826"
            self.__num_code = num_code
        elif self.__char_code == "JPY":
            num_code = "392"
            self.__num_code = num_code
        elif self.__char_code == "CHF":
            num_code = "756"
            self.__num_code = num_code
        elif self.__char_code == "CAD":
            num_code = "124"
            self.__num_code = num_code
        elif self.__char_code == "AUD":
            num_code = "036"
            self.__num_code = num_code
        else:
            raise ValueError('Ошибка при задании num_code валюты')
    
    @name.setter
    def name(self, name: str):
        if self.__char_code == "USD":
            name = "Доллар США"
            self.__name = name
        elif self.__char_code == "EUR":
            name = "Евро"
            self.__name = name
        elif self.__char_code == "GBP":
            name = "Фунт стерлингов"
            self.__name = name
        elif self.__char_code == "JPY":
            name = "Японская иена"
            self.__name = name
        elif self.__char_code == "CHF":
            name = "Швейцарский франк"
            self.__name = name
        elif self.__char_code == "CAD":
            name = "Канадский доллар"
            self.__name = name
        elif self.__char_code == "AUD":
            name = "Австралийский доллар"
            self.__name = name
        else:
            raise ValueError('Ошибка при задании name валюты')

    @nominal.setter
    def nominal(self, nominal: str):
        if self.__char_code == "USD":
            nominal = "1"
            self.__nominal = nominal
        elif self.__char_code == "EUR":
            nominal = "1"
            self.__nominal = nominal
        elif self.__char_code == "GBP":
            nominal = "1"
            self.__nominal = nominal
        elif self.__char_code == "JPY":
            nominal = "100"
            self.__nominal = nominal
        elif self.__char_code == "CHF":
            nominal = "1"
            self.__nominal = nominal
        elif self.__char_code == "CAD":
            nominal = "1"
            self.__nominal = nominal
        elif self.__char_code == "AUD":
            nominal = "1"
            self.__nominal = nominal
        else:
            raise ValueError('Ошибка при задании nominal валюты')
    