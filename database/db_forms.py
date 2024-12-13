import json
from bs4 import BeautifulSoup
from sqlalchemy import select

from models.table_parse import ParseTable
from database.database import DBManager
from database.report import DBManageCreator, SecurityDirectory

class FormParseReport(ParseTable):
    def __init__(self, text: str):
        self.data = {}
        with open('models/headers.json', 'r', encoding='utf-8') as head:
            self.headers: dict = json.load(head)

        soup = BeautifulSoup(text, "html.parser")
        self.tables = soup.findAll('table')
        self.parsing()


class DBForm(DBManager):
    def __init__(self, text):
        DBManageCreator.__init__(self)
        self.parse = FormParseReport(text)

    def __call__(self):
        with self.Session() as session:
            query = select(SecurityDirectory.name_paper)
            papers = session.scalars(query).all()

        data = (
            self.parse.cash_flow_period(papers),
            self.parse.transactions(),
            self.parse.dictionary_paper()
        )
        return [[elem.__dict__ for elem in item] for item in data]
