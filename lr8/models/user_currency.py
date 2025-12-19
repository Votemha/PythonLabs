class UserCurrency:
    """Модель связывания пользователя и валюты

    Поля:
    - id: уникальный идентификатор
    - user_id: id пользователя (внешний ключ к User)
    - currency_id: идентификатор валюты

    Хранится в памяти в виде словаря __data: id -> запись
    """
    __data = {}
    __id_counter = 1

    def __init__(self, id: int, user_id: int, currency_id):
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id

    def __repr__(self):
        return f"UserCurrency(id={self.id}, user_id={self.user_id}, currency_id={self.currency_id})"

    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "currency_id": self.currency_id}

    @classmethod
    def create_link(cls, user_id: int, currency_id):
        """Создать связь user - currency"""
        for rec in cls.__data.values():
            if rec.user_id == user_id and rec.currency_id == currency_id:
                return rec

        rec_id = cls.__id_counter
        inst = cls(rec_id, user_id, currency_id)
        cls.__data[rec_id] = inst
        cls.__id_counter += 1
        return inst

    @classmethod
    def remove_link(cls, user_id: int, currency_id) -> bool:
        """Удаляет связь"""
        for rid, rec in list(cls.__data.items()):
            if rec.user_id == user_id and rec.currency_id == currency_id:
                del cls.__data[rid]
                return True
        return False

    @classmethod
    def get_currencies_for_user(cls, user_id: int):
        """Возвращает список currency_id для данного user_id"""
        return [rec.currency_id for rec in cls.__data.values() if rec.user_id == user_id]

    @classmethod
    def get_users_for_currency(cls, currency_id):
        """Возвращает список user_id, подписанных на указанную валюту"""
        return [rec.user_id for rec in cls.__data.values() if rec.currency_id == currency_id]

    @classmethod
    def all_links(cls):
        return list(cls.__data.values())
