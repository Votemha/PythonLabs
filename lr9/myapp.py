from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from controllers.databasecontroller import CurrencyRatesCRUD
from models import Author
from models import User
from models import UserCurrency

from controllers import databasecontroller

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)


class CurrencyRatesMock():
    def __init__(self):
        self.__values = {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
        {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 91.0, "nominal": 1}

        

    @property
    def values(self):
        return self.__values


c_r = CurrencyRatesMock()

c_r_controller = databasecontroller.CurrencyRatesCRUD(c_r)
c_r_controller._create()

users = User()
user_currencies = UserCurrency()
login = None

main_author = Author('Ахметов Артём', 'P3122')

template = env.get_template("index.html")
authorHtml = env.get_template("author.html")
cur = env.get_template("currencies.html")
userHtml = env.get_template("user.html")
usersHtml = env.get_template("users.html")

nav = [{'caption': 'Основная страница', 'href': "/"},
        {'caption': 'Об авторе', 'href': '/author'},
        {'caption': 'Войти в аккаунт', 'href': "/user"},
        {'caption': 'Валюты', 'href': "/currency"},
        {'caption': 'Список пользователей', 'href': "/users"},]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global template
        global cur
        global login
        global c_r_controller
        global authorHtml

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        print(self.path)
        url_query_dict = parse_qs(self.path.rpartition('?')[-1])
        print(self.path.rpartition('?')[-1])
        result = "<html><h1>404!</h1></html>"
        if self.path == '/':
            # root url
            result = template.render(myapp="CurrenciesListApp",
                                        navigation=nav,
                                        author_name=main_author.name,
                                        author_group=main_author.group,
                                        currencies= c_r_controller._read(),
                                        login=login
                                        )
        
        if "currency" in self.path:
            result = cur.render(myapp="CurrenciesListApp",
                                        navigation=nav,
                                        author_name=main_author.name,
                                        author_group=main_author.group,
                                        currencies= c_r_controller._read(),
                                        login=login
                                        )
        if "author" in self.path:
            result = authorHtml.render(myapp="CurrenciesListApp",
                                        navigation=nav,
                                        author_name=main_author.name,
                                        author_group=main_author.group,
                                        currencies= c_r_controller._read(),
                                        login=login
                                        )

        if 'currency/delete' in self.path:
            # print(self.path.rpartition('?')[-1])
            c_r_controller._delete(url_query_dict['id'][0])
            # print(user_params_dict['id'][0])

            # c_r_controller._delete(user_id = )

        if 'currency/show' in self.path:
            result = f"<html><h1>{c_r_controller._read()}</h1></html>"
            print(c_r_controller._read())

        if 'currency/update' in self.path:
            # localhost:8080?usd=100000.100
            if 'usd' or 'eur' or 'gbr' or 'aud' in url_query_dict:
                for key in url_query_dict.keys():
                    print(key, url_query_dict[key][0])
                    c_r_controller._update({key.upper(): url_query_dict[key][0]})
                    result = cur.render(myapp="CurrenciesListApp",
                                        navigation=nav,
                                        author_name=main_author.name,
                                        author_group=main_author.group,
                                        currencies= c_r_controller._read(),
                                        login=login
                                        )
        
        if 'user' in self.path:
            print(url_query_dict)
            result = userHtml.render(myapp="CurrenciesListApp",
                                        navigation=nav,
                                        author_name=main_author.name,
                                        author_group=main_author.group,
                                        user_list=users._userlist,
                                        login=login,
                                        error="",
                                        success="",
                                        errorAdd="",
                                        successAdd="",
                                        errorIn="",
                                        successIn=""
                                        )
        
        if 'user/add' in self.path:
            loginAdd = url_query_dict.get("loginAdd", [""])[0]
            error = users._adduser(loginAdd)
            if error:
                result = userHtml.render(myapp="CurrenciesListApp",
                                            navigation=nav,
                                            author_name=main_author.name,
                                            author_group=main_author.group,
                                            user_list=users._userlist,
                                            errorAdd=error,
                                            login=login
                                            )
            else:
                result = userHtml.render(myapp="CurrenciesListApp",
                                            navigation=nav,
                                            author_name=main_author.name,
                                            author_group=main_author.group,
                                            user_list=users._userlist,
                                            success="Пользователь добавлен",
                                            errorAdd="",
                                            successAdd="",
                                            errorIn="",
                                            successIn=""
                                            )

        if 'user/add_currency' in self.path:
            user_id = int(url_query_dict.get("user_id", ["0"])[0])
            currency_id = int(url_query_dict.get("currency_id", ["0"])[0])
            error = user_currencies._add_user_currency(user_id, currency_id)
            if error:
                result = userHtml.render(myapp="CurrenciesListApp",
                                            navigation=nav,
                                            author_name=main_author.name,
                                            author_group=main_author.group,
                                            user_list=users._userlist,
                                            error=error,
                                            errorAdd="",
                                            successAdd="",
                                            errorIn="",
                                            successIn=""
                                            )
            else:
                result = userHtml.render(myapp="CurrenciesListApp",
                                            navigation=nav,
                                            author_name=main_author.name,
                                            author_group=main_author.group,
                                            user_list=users._userlist,
                                            successAdd="Валюта добавлена к пользователю",
                                            login=login
                                            )
        if 'user/in' in self.path:
            login = url_query_dict.get("loginIn", [""])[0]
            loginValue = users._inuser(login)
            if loginValue is True:
                result = userHtml.render(myapp="CurrenciesListApp",
                                            navigation=nav,
                                            author_name=main_author.name,
                                            author_group=main_author.group,
                                            user_list=users._userlist,
                                            successIn=login,
                                            login=login
                                            )
            else:
                result = userHtml.render(myapp="CurrenciesListApp",
                                            navigation=nav,
                                            author_name=main_author.name,
                                            author_group=main_author.group,
                                            user_list=users._userlist,
                                            errorIn=loginValue,
                                            login=login
                                            )
        if 'users' in self.path:
            currency_data = c_r_controller._read()
            currency_map = {i+1: item for i, item in enumerate(currency_data)}
            user_list_with_currencies = []
            for user in users._userlist:
                currencies = user_currencies._get_user_currencies(user['id'])
                currencies_str = ', '.join([f"{currency_map.get(cid, {}).get('char_code', 'N/A')} ({currency_map.get(cid, {}).get('value', 'N/A')})" for cid in currencies])
                user['currencies'] = currencies_str
                user_list_with_currencies.append(user)
            result = usersHtml.render(myapp="CurrenciesListApp",
                                            navigation=nav,
                                            author_name=main_author.name,
                                            author_group=main_author.group,
                                            user_list=user_list_with_currencies,
                                            login=login
                                            )



        self.end_headers()
        # result = "<html><h1>Hello, world!</h1></html>"
        self.wfile.write(bytes(result, "utf-8"))


httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
print('server is running')
httpd.serve_forever()