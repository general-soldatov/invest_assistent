from bs4 import BeautifulSoup
import json
from models.report import Transactions, Enrollments, WriteDowns, SecurityDirectory, MyCash, NominalPaper
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

class ParseTable:
    def __init__(self, file_path: str):
        self.data = {}
        with open('models/headers.json', 'r', encoding='utf-8') as head:
            self.headers: dict = json.load(head)

        with open(file_path, 'r', encoding='utf-8') as page:
            try:
                soup = BeautifulSoup(page.read(), "html.parser")
                self.tables = soup.findAll('table')
            except UnicodeDecodeError:
                logger.error(file_path)


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

    @staticmethod
    def hash_key(*args, table_size=10**13, prime=7):
        hash_str = ''.join(map(str, args))
        hash_value = 0
        for i, char in enumerate(hash_str, 1):
            hash_value += ord(char) * (prime ** i)
        return hash_value % table_size

    def parsing(self):
        for table in self.tables:
            header = self.get_header(table)
            for key, value in self.headers.items():
                if header.startswith(value['name']):
                    self.data[key] = self.convert_tab(table, value['column'], rule=key)

    def transactions(self) -> List[Transactions]:
        transactions = self.data['transactions'][2:]
        result = []
        for item in transactions:
            result.append(Transactions(id_deal=int(item[13]), name_paper=item[3],
                date_deal=datetime.strptime(item[0], '%d.%m.%Y'), type_deal=item[6], count_paper=int(item[7].replace(' ', '')), price_paper=float(item[8].replace(' ', '')),
                coupon_add_paper=float(item[10].replace(' ', '')), broker_comission=float(item[11].replace(' ', '')), market_comission=float(item[12].replace(' ', ''))))
        return result

    def cash_flow_period(self, papers: list) -> List[Enrollments | WriteDowns]:
        enrollments = self.data['cash_flow_period'][2:]
        result = []
        for item in enrollments:
            name_paper = None
            for paper in papers:
                if paper in item[2]:
                    name_paper = paper
                    break
            try:
                hash_str = self.hash_key(item[4], item[5], item[0], item[2])
                if not name_paper and "Зачисление" in item[2]:
                    result.append(MyCash(id_hash=hash_str, operation=item[2], date_operation=datetime.strptime(item[0], '%d.%m.%Y'),
                            sum_enroll=float(item[4].replace(' ', ''))))
                    continue
                type_oper = None
                for oper in ['купон', 'амортизация', 'погашение', 'дивиденды']:
                    if oper in item[2].lower():
                        type_oper = oper
                        break
                if not type_oper:
                    type_oper = item[2]

                if item[4] != "0.00" and name_paper:
                    result.append(Enrollments(id_hash=hash_str, name_paper=name_paper, type_operation = type_oper, date_operation=datetime.strptime(item[0], '%d.%m.%Y'),
                            sum_enroll=float(item[4].replace(' ', ''))))
                elif item[5] != "0.00":
                    result.append(WriteDowns(id_hash=hash_str, operation=item[2], date_operation=datetime.strptime(item[0], '%d.%m.%Y'),
                            sum_enroll=float(item[5].replace(' ', ''))))
            except ValueError:
                logger.error('Value Error')
                continue

        return result

    def dictionary_paper(self) -> List[SecurityDirectory]:
        dictionary = self.data['securities_directory'][2:]
        result = []
        for item in dictionary:
            result.append(SecurityDirectory(name_paper=item[0], code_paper=item[1], isin_paper=item[2],
                        emitent=item[3], type_paper=item[4], series_paper=item[5]))
        return result

    def nominal_paper(self) -> List[NominalPaper]:
        nominal = self.data['briefcase'][2:-1]
        result = []
        for item in nominal:
            result.append(NominalPaper(name_paper=item[0], nominal=float(item[4].replace(' ', '')),
                paper_count=int(item[8].replace(" ", ""))))
        return result
