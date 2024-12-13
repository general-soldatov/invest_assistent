import eel
import json
from mail_parse import MainPage
from database.db_forms import FormParseReport, DBForm
import base64
# from models.graph_plots import graph_bytes
from models.graph_plots import ByteGraph
from models.moex_parser import InfoPaper

eel.init('front')

@eel.expose
def import_table(table: str, name: str) -> dict:
    with open('front/static/table.json', encoding='utf-8') as js_file:
        data = json.load(js_file)
        return data[table][name]

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

@eel.expose
def brief_case():
    lst = MainPage().get_briefcase()
    return lst

@eel.expose
def get_image():
    data = ByteGraph()
    to_data = {
        'my_cash': MainPage().get_cash('cash'),
        'coupons': MainPage().get_cash('coupons'),
        'enrollments': MainPage().get_cash('enrollments'),
        'get_cash': MainPage().get_cash('get_cash')
    }
    result = {}
    for key, value in to_data.items():
        data.graph_1(value)
        result[key] = data.graph_bytes()
    data.graph_cash(*InfoPaper().get_exchange_rate())
    result['money_cb'] = data.graph_bytes()
    return result

@eel.expose
def get_transaction(data, name):
    if name == 'report':
        report = DBForm(data)
        lst = report()
        return lst
    print(name)
    for key, value in data:
        print(key, value)

@eel.expose
def get_form(data, file):
    print(data)
    with open('report.html', 'wb') as fls:
        fls.write(base64.b64decode(file))

@eel.expose
def get_papers():
    data = MainPage().get_papers()
    return data


eel.start('templates/main_page.html', jinja_templates='templates', size=(800, 600))