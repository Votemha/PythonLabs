import sqlite3
import logging

class UserCurrency():
    _con = None
    _cursor = None

    def __init__(self):
        # initialize shared in-memory connection once
        if UserCurrency._con is None:
            UserCurrency._con = sqlite3.connect(':memory:')
            UserCurrency._cursor = UserCurrency._con.cursor()
            UserCurrency._cursor.execute(
                "CREATE TABLE IF NOT EXISTS user_currency ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "user_id INTEGER NOT NULL,"
                "currency_id INTEGER NOT NULL,"
                "FOREIGN KEY(user_id) REFERENCES user(id),"
                "FOREIGN KEY(currency_id) REFERENCES currency(id));")
            UserCurrency._con.commit()

        # instance uses shared connection/cursor
        self.__con = UserCurrency._con
        self.__cursor = UserCurrency._cursor

    def _add_user_currency(self, user_id, currency_id):
        # check if already exists
        self.__cursor.execute("SELECT id FROM user_currency WHERE user_id = ? AND currency_id = ?", (user_id, currency_id))
        if self.__cursor.fetchone():
            return "Валюта уже добавлена к пользователю"

        query = "INSERT INTO user_currency(user_id, currency_id) VALUES(?, ?)"
        logging.info(f"INSERT INTO user_currency(user_id={user_id}, currency_id={currency_id})")
        self.__cursor.execute(query, (user_id, currency_id))
        self.__con.commit()
        return ""  # success

    def _get_user_currencies(self, user_id):
        self.__cursor.execute("SELECT currency_id FROM user_currency WHERE user_id = ?", (user_id,))
        return [row[0] for row in self.__cursor.fetchall()]