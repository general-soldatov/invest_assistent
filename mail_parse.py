from os import listdir
from os.path import isfile, join
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database import DBManager, Base, Transactions

def add_data(Session: sessionmaker):
    mypath = 'stack_data'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f != 'data.json']
    for file in onlyfiles:
        db = DBManager(Session, file_path=f'{mypath}/{file}')
        db.add_dictionary()
        db.add_transactions()
        db.add_nominal()
        db.add_cash_flow()

def query(Session: sessionmaker):
    query = select(Transactions)
    data: Transactions = Session().scalars(query).all()
    result = 0
    for item in data:
        result += item.price_paper * item.count_paper * 10
        print(item.__dict__)
    print(result)

def main():
    engine = create_engine('sqlite:///my-database.db')
    Session = sessionmaker(engine)
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    # add_data(Session)
    query(Session)


if __name__ == '__main__':
    main()