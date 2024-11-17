from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()
PATH = getenv('PATH')

headers = {}
with open('headers.json', 'r', encoding='utf-8') as head:
    headers: dict = json.load(head)


with open(PATH, 'r', encoding='utf-8') as page:
    soup = BeautifulSoup(page.read(), "html.parser")
    tables = soup.findAll('table')


    def convert_tab(tab: BeautifulSoup, column, rule = None):
        table = [item.text for item in tab.find_all('td')]
        if rule == 'actives':
            tab = table.copy()
            table = [tab[0], *tab[4:]]
        if rule == 'briefcase':
            table = [*table[5:41], *table[42:]]
        data = [[table[i] for i in range(column*j, column*(j + 1))] for j in range(int(len(table) / column))]
        return data

    def get_header(table: BeautifulSoup):
        return table.previous_sibling.previous_sibling.text.strip().replace('\n', '')

    data = {}
    for i, table in enumerate(tables):
        header = get_header(table)
        for key, value in headers.items():
            if header.startswith(value['name']):
                data[key] = convert_tab(table, value['column'], rule=key)

    with open('stack_data/data.json', 'w', encoding='utf-8') as data_set:
        json.dump(data, data_set, ensure_ascii=False, indent=4)