import eel
import json
from mail_parse import MainPage

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


eel.start('templates/main_page.html', jinja_templates='templates')