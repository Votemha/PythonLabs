import unittest
import os
from models import Author, App, Currency, User
from jinja2 import Environment, FileSystemLoader

class TestTemplates(unittest.TestCase):

    def setUp(self):
        templates_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.template = self.env.get_template("index.html")
        self.author = Author('Test Author', 'P3122')
        self.app = App('TestApp', '1.0', self.author)
        self.currency = Currency(id=None, num_code=None, char_code='USD', name=None, value=75.5, nominal=1)
        self.user = User.userUp('TestUser')

    def test_index_template_render(self):
        data = {
            'myapp': 'TestApp',
            'navigation': [{'caption': 'Test', 'href': '/test'}],
            'author_name': self.author.name,
            'group': self.author.group,
            'a_variable': [self.currency],
            'current_user': self.user,
            'version': self.app.version,
            'nameApp': self.app.name
        }
        result = self.template.render(**data)
        self.assertIn('TestApp', result)
        self.assertIn('Test Author', result)
        self.assertIn('USD', result)
        self.assertIn('TestUser', result)

    def test_template_loops_and_conditions(self):
        # Проверяем цикл в навигации
        data = {
            'navigation': [
                {'caption': 'Home', 'href': '/'},
                {'caption': 'Currencies', 'href': '/currencies'}
            ],
            'current_user': self.user,
            'a_variable': [self.currency, Currency(id=None, num_code=None, char_code='EUR', name=None, value=85.0, nominal=1)]
        }
        result = self.template.render(**data)
        self.assertIn('Home', result)
        self.assertIn('Currencies', result)
        self.assertIn('USD', result)
        self.assertIn('EUR', result)

if __name__ == '__main__':
    unittest.main()