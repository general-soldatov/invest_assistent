from os import listdir
from os.path import isfile, join
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import DBManager


def main():
    engine = create_engine('sqlite:///my-database.db')
    Session = sessionmaker(engine)
    # Base.metadata.create_all(engine)
    # Base.metadata.drop_all(engine)
    mypath = 'stack_data'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f != 'data.json']
    for file in onlyfiles:
        db = DBManager(Session, file_path=f'{mypath}/{file}')
        db.add_dictionary()
        db.add_transactions()
        db.add_cash_flow()


if __name__ == '__main__':
    main()