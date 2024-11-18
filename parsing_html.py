from bs4 import BeautifulSoup
from dotenv import load_dotenv
from os import getenv
import json
from models.report import Transactions, Enrollments, WriteDowns, SecurityDirectory
from datetime import datetime
load_dotenv()
PATH = getenv('PATH')

class ParseTable:
    def __init__(self, file_path: str):
        self.data = {}
        with open('headers.json', 'r', encoding='utf-8') as head:
            self.headers: dict = json.load(head)

        with open(file_path, 'r', encoding='utf-8') as page:
            soup = BeautifulSoup(page.read(), "html.parser")
            self.tables = soup.findAll('table')

    @staticmethod
    def convert_tab(tab: BeautifulSoup, column, rule = None):
        table = [item.text for item in tab.find_all('td')]
        if rule == 'actives':
            tab = table.copy()
            table = [tab[0], *tab[4:]]
        elif rule == 'briefcase':
            table = [*table[5:41], *table[42:]]
        elif rule == 'transactions':
            table = [*table[:32], *table[33:]]
        data = [[table[i] for i in range(column*j, column*(j + 1))] for j in range(int(len(table) / column))]
        return data

    @staticmethod
    def get_header(table: BeautifulSoup):
        return table.previous_sibling.previous_sibling.text.strip().replace('\n', '')

    def parsing(self):
        for table in self.tables:
            header = self.get_header(table)
            for key, value in self.headers.items():
                if header.startswith(value['name']):
                    self.data[key] = self.convert_tab(table, value['column'], rule=key)

    def transactions(self):
        transactions = self.data['transactions'][2:]
        result = []
        for item in transactions:
            result.append(Transactions(id_deal=int(item[13]), name_paper=item[3],
                date_deal=datetime.strptime(item[0], '%d.%m.%Y'), type_deal=item[6], count_paper=int(item[7]), price_paper=float(item[8]),
                coupon_add_paper=float(item[10]), broker_comission=float(item[11]), market_comission=float(item[12])))
        return result

    def cash_flow_period(self, papers: list):
        enrollments = self.data['cash_flow_period'][2:]
        result = []
        name_paper = None
        for item in enrollments:
            for paper in papers:
                if paper in item[2]:
                    name_paper = paper
                    break
            if item[4] != "0.00":
                result.append(Enrollments(name_paper=name_paper, date_operation=datetime.strptime(item[0], '%d.%m.%Y'),
                        sum_enroll=float(item[4])))
            else:
                result.append(WriteDowns(name_paper=name_paper, date_operation=datetime.strptime(item[0], '%d.%m.%Y'),
                        sum_enroll=float(item[4])))
        return result

    def dictionary_paper(self):
        dictionary = self.data['securities_directory'][2:]
        result = []
        for item in dictionary:
            result.append(SecurityDirectory(name_paper=item[0], code_paper=item[1], isin_paper=item[2],
                        emitent=item[3], type_paper=item[4], series_paper=item[5]))
        return result


    # with open('stack_data/data.json', 'w', encoding='utf-8') as data_set:
    #     json.dump(data, data_set, ensure_ascii=False, indent=4)

parse = ParseTable(file_path=PATH)
parse.parsing()

for item in parse.dictionary_paper():#cash_flow_period(['Магнит4P03', 'ФЭСАгро1Р1']):
    print(item.__dict__)