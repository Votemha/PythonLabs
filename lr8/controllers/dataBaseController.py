class CurrencyRatesCRUD():
    def __init__(self, currency_rates_obj):
        import sqlite3
        self.__con = sqlite3.connect(':memmory:')
        self.__createtable()
        self.__cursor = self.__con.cursor()
        self.__currency_rates_obj = currency_rates_obj

    def __createtable(self):
        self.__con.execute(
            "CREATE TABLE IF NOT EXISTS currency("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "cur TEXT,"
            "date TEXT,"
            "value FLOAT);")
        self.__con.commit()
        

