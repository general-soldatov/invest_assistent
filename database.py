import logging
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.exc import NoResultFound, IntegrityError
import sqlite3

from models.report import Base, Transactions, SecurityDirectory, Enrollments, WriteDowns
from models.table_parse import ParseTable
from typing import List
from dotenv import load_dotenv
from os import getenv

logger = logging.getLogger(__name__)


class DBManager:
    def __init__(self, Session: sessionmaker, file_path: str):
        self.Session: sessionmaker = Session
        self.parse = ParseTable(file_path)
        self.parse.parsing()

    def add_dictionary(self):
        with self.Session() as session:
            for item in self.parse.dictionary_paper():
                try:
                    condition = SecurityDirectory.name_paper == item.name_paper
                    query = select(SecurityDirectory).where(condition)
                    data: SecurityDirectory = session.scalars(query).one()
                    logger.error(f'{data.name_paper} is present with dictionary')
                except NoResultFound:
                    session.add(item)
                    continue
            session.commit()

    def add_transactions(self):
        with self.Session() as session:
            for item in self.parse.transactions():
                try:
                    condition = Transactions.id_deal == item.id_deal
                    query = select(Transactions).where(condition)
                    data: Transactions = session.scalars(query).one()
                    logger.error(f'{data.id_deal} is present with transactions')
                except NoResultFound:
                    session.add(item)
                    continue
            session.commit()

    def add_cash_flow(self):
        with self.Session() as session:
            query = select(SecurityDirectory.name_paper)
            papers = session.scalars(query).all()
            for item in self.parse.cash_flow_period(papers):
                try:
                    if isinstance(item, WriteDowns):
                        table = WriteDowns
                    elif isinstance(item, Enrollments):
                        table = Enrollments
                    condition = table.name_paper == item.name_paper
                    query = select(table).where(condition)
                    data: WriteDowns = session.scalars(query).one()
                    logger.error(f'{data.name_paper} is present with cash-flow data.')
                except NoResultFound:
                    session.add(item)
                    continue
            session.commit()


    def get_data(self, obj: Base, condition: bool = True):
        query = select(obj).where(condition)
        return self.Session().scalars(query)


# def create_user(Session: sessionmaker, id_, name, email):
#     user = User(id_=id_, name=name, e_mail=email)

#     with Session() as session:
#         session.add(user)
#         session.commit()

# def get_by_name(name: str, Session) -> list[User]:
#     query = select(User).where(User.name == name)
#     db_object = Session().scalars(query).one()
#     return db_object

# def update(name: str, name_old: str, Session) -> None:
#     data: User = get_by_name(name_old, Session)
#     with Session() as session:
#         data.name = name
#         session.merge(data)
#         session.commit()


# def delete(name: str, session) -> User:
#     query = select(User).where(User.name == name)
#     db_object = session.scalars(query).one()
#     session.delete(db_object)
#     return db_object
