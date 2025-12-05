
class App():
    def __init__(self, name: str, version: str, author: object):
        self.__name: str = name
        self.__version: str = version
        self.__author: object = author

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        """Задаем название приложения"""
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании названия приложения')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        """Задаем версию приложения"""
        if type(version) is str and len(version) > 0:
            self.__version = version
        else:
            raise ValueError('Ошибка при задании версии приложения')
    
    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, author: object):
        """Задаем автора приложения"""
        if type(author) is object:
            self.__author = author
        else:
            raise ValueError('Ошибка при задании автора приложения')

