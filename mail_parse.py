from os import listdir
from os.path import isfile, join
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database import DBManager, Base, Transactions, SecurityDirectory, Enrollments, MyCash, WriteDowns
from typing import List
# from models.table_parse import ParseTable


class MainPage:
    def __init__(self):
        engine = create_engine('sqlite:///my-database.db')
        self.Session: sessionmaker = sessionmaker(engine)

    def enrollments(self, types='купон'):
        query = select(Enrollments).where(Enrollments.type_operation == types)
        data: Enrollments = self.Session().scalars(query).all()
        result = []
        for item in data:
            item.date_operation = item.date_operation.strftime("%d.%m.%Y")
            result.append(item.__dict__)
        return result

def add_data(Session: sessionmaker):
    mypath = 'stack_data'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f != 'data.json']
    for file in onlyfiles:
        db = DBManager(Session, file_path=f'{mypath}/{file}')
        db.add_dictionary()
        db.add_transactions()
        db.add_nominal()
        db.add_cash_flow()
        # ParseTable(f'{mypath}/{file}')

def query(Session: sessionmaker):
    query = select(Enrollments).where(Enrollments.type_operation != 'купон')
    data: Enrollments = Session().scalars(query).all()
    result = 0
    for item in data:
        # result += item.price_paper * item.count_paper * 10
        print(item.__dict__)
    print(result)



def transactions(Session: sessionmaker, type_deal = 'Покупка'):
    query = select(Transactions.name_paper, Transactions.price_paper,
                   Transactions.count_paper).where(Transactions.type_deal == type_deal)
    data: Transactions = Session().execute(query)
    papers = select(SecurityDirectory.name_paper).where(SecurityDirectory.type_paper == 'Облигация')
    papers_query = Session().scalars(papers).all()
    result = {}
    cash = 0
    for item in data:
        if item[0] in papers_query:
            result[item[0]] = result.get(item[0], 0) + 10*item[1] * item[2]

    for key, value in result.items():
        # print(f'{key}: {value}')
        cash += value
    return cash

def my_cash(Session: sessionmaker):
    query = select(MyCash)
    data: List[MyCash] = Session().scalars(query).all()
    result = 0
    for item in data:
        result += item.sum_enroll
        # print(item.__dict__)
    return result

def my_write_down(Session: sessionmaker):
    query = select(WriteDowns)
    data: List[WriteDowns] = Session().scalars(query).all()
    result = 0
    for item in data:
        if item.operation == 'Списание д/с':
            result += item.sum_enroll
            # print(item.__dict__)
    return result

def enrollment(Session: sessionmaker, oper = 'купон'):
    query = select(Enrollments.name_paper, Enrollments.sum_enroll).where(Enrollments.type_operation == oper)
    papers_query = Session().execute(query)
    result = {}
    cash = 0
    for item in papers_query:
        result[item[0]] = result.get(item[0], 0) + item[1]

    for key, value in result.items():
        # print(f'{key}: {value}')
        cash += value
    return cash

def main():
    engine = create_engine('sqlite:///my-database.db')
    Session = sessionmaker(engine)
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    # add_data(Session)
    # query(Session)
    # cash = my_cash(Session) + enrollment(Session) - \
    #     my_write_down(Session) + enrollment(Session, oper='погашение') - \
    #     transactions(Session) + transactions(Session, 'Продажа') + enrollment(Session, oper='амортизация')
    # print(cash)
    print(MainPage().enrollments()[0])


if __name__ == '__main__':
    main()