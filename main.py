import eel
from mail_parse import MainPage

# from jinja2 import Environment, PackageLoader, select_autoescape, Template

# env = Environment(
#     loader=PackageLoader("eel"),
#     autoescape=select_autoescape()
# )

# template = Template("My name is {{ name }} and I am {{ age }}")

# data = template.render(name = 'that say nih', age = 2)

eel.init('front')

@eel.expose
def summer(x, y):
    return x + y

@eel.expose
def coupons(enrollments=None):
    data, cash = MainPage().enrollments(enrollments)
    return data, cash

@eel.expose
def transactions(types = 'Покупка'):
    data, cash = MainPage().transactions(types)
    return data, cash

@eel.expose
def moex_data():
    lst = MainPage().get_bonds_sql()
    return lst



eel.start('templates/main_page.html', jinja_templates='templates')