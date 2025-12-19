import sqlite3
import logging

class User():
    _logindata = []

    def __init__(self):
        self.__con = sqlite3.connect(':memory:')
        self._createtable()
        self.__cursor = self.__con.cursor()

    def _createtable(self):
        self.__con.execute(
            "CREATE TABLE user ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "login TEXT NOT NULL);")
        self.__con.commit()
    
    @property
    def _userlist(self):
        users = self.__con.execute("SELECT * FROM user")

        users_data = []
        login_data = []
        for _item in users:
            _data = {'id': int(_item[0]), 'login': _item[1]}
            login_data.append(_item[1])
            users_data.append(_data)

        User._logindata = login_data

        return users_data

    def _adduser(self, login=str):
        if not User._logindata:
            try:
                self._loginlist()
            except Exception:
                pass
        
        if login not in User._logindata and len(login) > 2:
            params = (login,)
        else:
            if login in User._logindata: value = "Логин уже используется"
            if len(login) <= 2: value = "Длина логина должна быть больше 2х символов"
            logging.error("Ошибка при создании логина: " + value)
            return value  # return error message to display to user

        query = "INSERT INTO user(login) VALUES(?)"
        logging.info(f"INSERT INTO user(login) VALUES({login})")
        self.__cursor.execute(query, params)
        self.__con.commit()
        return ""  # success, no error message
    
    def _inuser(self, login=str):
        if not User._logindata:
            try:
                self._loginlist()
            except Exception:
                pass

        if login in User._logindata and len(login) > 2:
            params = (login)
        else:
            if login not in User._logindata: value = "Пользователь не зарегистрирован"
            if len(login) <= 2: value = "Длина логина должна быть больше 2х символов"
            logging.error("Ошибка при создании логина: " + value)
            return "Ошибка: " + value

        return True