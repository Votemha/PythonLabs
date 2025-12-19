
from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author
from models import App
from models import Currency
from models import User
from utils.currencies_api import get_currencies
from urllib.parse import urlparse
# from models import dataBaseController

from http.server import HTTPServer, BaseHTTPRequestHandler


env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

template = env.get_template("index.html")
curren = env.get_template("./pages/bank/index.html")
sign_template = env.get_template("./pages/sign/index.html")
subscriptions_template = env.get_template("./pages/currencies/index.html")

main_author = Author('Aхметов Артём', 'P3122')
version_app = App('CurrenciesListApp', '1.0', main_author)
print("d", version_app.version)

currency_list = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD']

data = get_currencies(currency_list)
currencies = []
for code, value in data.items():
    c = Currency(id=None, num_code=None, char_code=code, name=None, value=value, nominal=1)
    currencies.append(c)
print(currencies)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        from urllib.parse import parse_qs
        
        path = urlparse(self.path).path.split('/')[1]
        subpath = urlparse(self.path).path.split('/')[2] if len(urlparse(self.path).path.split('/')) > 2 else None
        query_params = parse_qs(urlparse(self.path).query)
        
        # Функция для получения текущего пользователя
        def get_current_user():
            user_id_param = query_params.get('user_id', [''])[0]
            if user_id_param:
                try:
                    user_id = int(user_id_param)
                    if user_id in User.dataUsers():
                        return User.dataUsers()[user_id]
                except ValueError:
                    pass
            return None
        
        try:
            if path == '' or path == 'index.html':
                current_user = get_current_user()
                user_id_param = f"?user_id={current_user.id}" if current_user else ""
                result = template.render(myapp="CurrenciesListApp",
                                     navigation=[{'caption': 'Курсы валют',
                                                  'href': f"/currencies{user_id_param}"},
                                                  {'caption': 'Регистрация',
                                                  'href': f"/sign{user_id_param}"}],
                                     author_name=version_app.author.name,
                                     group=version_app.author.group,
                                     a_variable=currencies,
                                     current_user=current_user,
                                     version=version_app.version,
                                     nameApp=version_app.name
                                     )
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(bytes(result, "utf-8"))
            
            elif path == 'currencies':
                if subpath == 'subscriptions':
                    # Страница управления подписками на валюты
                    current_user = get_current_user()
                    
                    # DEBUG
                    print(f"DEBUG: path='currencies/subscriptions', user_id from params: {query_params.get('user_id', [''])[0]}")
                    print(f"DEBUG: current_user = {current_user}")
                    print(f"DEBUG: query_params = {query_params}")
                    
                    # Обработка подписки
                    if 'subscribe' in query_params and current_user:
                        currency = query_params.get('currency', [''])[0]
                        if currency:
                            print(f"DEBUG: Subscribing {current_user.name} to {currency}")
                            current_user.subscribeCurrency(currency)
                    
                    # Обработка отписки
                    if 'unsubscribe' in query_params and current_user:
                        currency = query_params.get('currency_to_remove', [''])[0]
                        if currency:
                            print(f"DEBUG: Unsubscribing {current_user.name} from {currency}")
                            current_user.unsubscribeCurrency(currency)
                    
                    # Получаем свежие валюты
                    all_currencies = get_currencies(['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD'])
                    
                    # Строим URL с user_id
                    user_id_param = f"?user_id={current_user.id}" if current_user else ""
                    
                    resultSubscriptions = subscriptions_template.render(
                        myapp="CurrenciesListApp",
                        navigation=[
                            {'caption': 'Основная страница', 'href': f"/{user_id_param}"},
                            {'caption': 'Курсы валют', 'href': f"/currencies{user_id_param}"},
                            {'caption': 'Регистрация', 'href': f"/sign{user_id_param}"}
                        ],
                        current_user=current_user,
                        available_currencies=all_currencies
                    )
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(bytes(resultSubscriptions, "utf-8"))
                else:
                    # Обычная страница с курсами валют
                    current_user = get_current_user()
                    
                    # Строим URL с user_id
                    user_id_param = f"?user_id={current_user.id}" if current_user else ""
                    
                    result = curren.render(myapp="CurrenciesListApp",
                                     navigation=[{'caption': 'Основная страница',
                                                  'href': f"/{user_id_param}"},
                                                  {'caption': 'Регистрация',
                                                  'href': f"/sign{user_id_param}"}],
                                     author_name=main_author.name,
                                     group=main_author.group,
                                     a_variable=currencies,
                                     current_user=current_user,
                                     version=version_app.version
                                     )
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(bytes(result, "utf-8"))
            
            elif path == 'sign':
                current_user = get_current_user()  # Проверяем, есть ли уже авторизованный пользователь
                
                if 'signup' in query_params:
                    # Регистрация - парсим параметры из URL
                    name = query_params.get('login', [''])[0]
                    
                    if name:
                        signUp = User.userUp(name)
                        current_user = signUp  # Автоматически авторизуем после регистрации
                
                elif 'signin' in query_params:
                    # Авторизация - парсим параметры из URL
                    name = query_params.get('login_auth', [''])[0]
                    
                    if name:
                        current_user = User.authenticate(name)
                
                # Строим URL с user_id
                user_id_param = f"?user_id={current_user.id}" if current_user else ""
                
                # Показываем страницу со списком пользователей и текущим пользователем
                resultSignCurrent = sign_template.render(myapp="CurrenciesListApp",
                                                navigation=[{'caption': 'Основная страница',
                                                            'href': f"/{user_id_param}"},
                                                            {'caption': 'Курсы валют',
                                                            'href': f"/currencies{user_id_param}"}],
                                                users = User.dataUsers(),
                                                current_user = current_user,
                                                user_id_param = user_id_param,
                                                version=version_app.version
                                                )
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(bytes(resultSignCurrent, "utf-8"))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(bytes("<h1>404 Страница не найдена</h1>", "utf-8"))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes(f"<h1>Ошибка: {e}</h1>", "utf-8"))


httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
print('server is running')
httpd.serve_forever()

