from os import listdir
from os.path import isfile, join
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database import DBManager, Base, Transactions, SecurityDirectory, Enrollments, MyCash, WriteDowns, NominalPaper, BondInfo
from typing import List, Dict
from moex_parser import InfoPaper
# from models.table_parse import ParseTable


class MainPage:
    def __init__(self):
        engine = create_engine('sqlite:///my-database.db')
        self.Session: sessionmaker = sessionmaker(engine)

    def enrollments(self, types):
        condition = Enrollments.type_operation == types if types else Enrollments.type_operation != 'купон'
        query = select(Enrollments).where(condition).order_by(Enrollments.date_operation)
        data: Enrollments = self.Session().scalars(query).all()
        result = []
        cash = 0
        for item in data:
            item.date_operation = item.date_operation.strftime("%d.%m.%Y")
            result.append(item.__dict__)
            cash += item.sum_enroll
        return result, round(cash, 2)

    def transactions(self, types='Покупка'):
        data: Transactions = self.Session().query(Transactions, NominalPaper, SecurityDirectory).\
            join(NominalPaper, Transactions.name_paper == NominalPaper.name_paper).\
                join(SecurityDirectory, Transactions.name_paper == SecurityDirectory.name_paper).\
                    where(Transactions.type_deal == types).all()
        result = []
        cash = 0
        for cash_flow, nominal, sec in data:
            cash_flow.date_deal = cash_flow.date_deal.strftime("%d.%m.%Y")
            cash_flow.nominal = nominal.nominal
            cash_flow.type = sec.type_paper
            cash_flow.sum = round(cash_flow.price_paper * cash_flow.count_paper, 2)
            if 'Облигация' in cash_flow.type:
                cash_flow.sum = round(cash_flow.sum * nominal.nominal / 100, 2)
            result.append(cash_flow.__dict__)
            cash += cash_flow.sum
        return result, round(cash, 2)

    def get_bonds(self, types='Облигация'):
        data: SecurityDirectory = self.Session().query(SecurityDirectory.isin_paper).\
            where(SecurityDirectory.type_paper.startswith(types)).all()

        return InfoPaper().get_bonds_lst([item[0] for item in data])

    def get_count_paper(self):
        papers: SecurityDirectory = self.Session().query(SecurityDirectory.name_paper).all()
        data: List[Transactions] = self.Session().query(Transactions)
        nominal: dict = {item.name_paper: item.nominal
                                       for item in self.Session().query(NominalPaper).all()}
        dict_paper = {item[0]: {'credit': 0, 'debet': 0, 'count': 0} for item in papers}
        for item in data:
            if item.name_paper not in dict_paper:
                continue
            if item.name_paper not in nominal:
                nominal[item.name_paper] = 1000
            dict_paper[item.name_paper]['credit'] += (item.broker_comission + item.market_comission) * item.count_paper
            saler = item.price_paper * item.count_paper * nominal[item.name_paper] / 100
            if item.type_deal == 'Покупка':
                dict_paper[item.name_paper]['credit'] += saler
                dict_paper[item.name_paper]['count'] += item.count_paper
            elif item.type_deal == "Продажа":
                dict_paper[item.name_paper]['debet'] += saler
                dict_paper[item.name_paper]['count'] -= item.count_paper

        return dict_paper

    def get_coupons(self):
        dict_paper = self.get_count_paper()
        data: List[Enrollments] = self.Session().query(Enrollments).all()
        for item in data:
            if item.type_operation == 'погашение':
                dict_paper[item.name_paper]['count'] = 0
            dict_paper[item.name_paper]['debet'] += item.sum_enroll

        return dict_paper

    def get_bonds_sql(self):
        data = self.Session().scalars(select(BondInfo)).all()
        return [item.__dict__ for item in data]

    def get_briefcase(self):
        data = self.Session().query(BondInfo.name_paper, BondInfo.security_id).all()
        papers = self.get_count_paper()
        result = []
        for item in data:
            name = item[0]
            if 'ОФЗ ' in name:
                name = name[4:]
            try:
                dct = {**papers[name], 'name_paper': name}
            except KeyError:
                continue
            dct['price'] = InfoPaper().get_price_paper(item[1])
            if dct['count'] < 0:
                dct['count'] = 0
            result.append(dct)
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
    # data = MainPage().get_bonds()
    # data = MainPage().get_bonds_sql()
    # print(InfoPaper().get_price_paper(['RU000A1058K7']))
    data = MainPage().get_briefcase()
    [print(item) for item in data]
    # data = [{'security_id': 'SU26243RMFS4', 'name_paper': 'ОФЗ 26243', 'nominal': 1000, 'coupon_value': 48.87, 'nkd': 46.99, 'next_coupon_date': '2024-12-04', 'maturity_date': '2038-05-19', 'coupon_period': 182, 'coupon_enroll': '9.774 %'}]
    # DBManager(Session, file_path='stack_data/400PJLR_010121_310121_M.html').add_bond_info(data)
    # print(data)


if __name__ == '__main__':
    main()