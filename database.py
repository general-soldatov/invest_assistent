import logging
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.exc import NoResultFound, IntegrityError
import sqlite3

from models.report import Base, Transactions, SecurityDirectory, Enrollments, WriteDowns, MyCash, NominalPaper, BondInfo
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
                    # logger.error(f'{data.name_paper} is present with dictionary')
                except NoResultFound:
                    session.add(item)
                    continue
            session.commit()

    def add_transactions(self):
        with self.Session() as session:
            try:
                transactions = self.parse.transactions()
            except KeyError:
                logger.error('Transactions is not implemented.')
                return
            for item in transactions:
                try:
                    condition = Transactions.id_deal == item.id_deal
                    query = select(Transactions).where(condition)
                    data: Transactions = session.scalars(query).one()
                    # logger.error(f'{data.id_deal} is present with transactions')
                except NoResultFound:
                    session.add(item)
                    continue
            session.commit()

    def add_nominal(self):
        with self.Session() as session:
            for item in self.parse.nominal_paper():
                try:
                    condition = NominalPaper.name_paper == item.name_paper
                    query = select(NominalPaper).where(condition)
                    data: NominalPaper = session.scalars(query).one()
                    session.merge(data)
                except NoResultFound:
                    session.add(item)
                    continue
            session.commit()

    def add_cash_flow(self):
        with self.Session() as session:
            try:
                query = select(SecurityDirectory.name_paper)
                papers = session.scalars(query).all()
                data = self.parse.cash_flow_period(papers)
            except KeyError:
                logger.error('cash_flow_period is not with data')
                return
            for item in data:
                session.merge(item)
                continue
            session.commit()

    def add_bond_info(self, data: List[dict]):
        with self.Session() as session:
            for item in data:
                session.merge(BondInfo(**item))

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
