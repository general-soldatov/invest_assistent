# from models.table_parse import ParseTable, SecurityDirectory
# from dotenv import load_dotenv
# from os import getenv
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine, select

# load_dotenv()
# PATH = getenv('PATH')

# parse = ParseTable(PATH)
# parse.parsing()

# engine = create_engine('sqlite:///my-database.db')
# Session = sessionmaker(engine)
# with Session() as session:
#     query = select(SecurityDirectory.name_paper)
#     papers = session.scalars(query).all()

# print('Dictionary')
# for item in parse.dictionary_paper():
#     print(item.__dict__)
# print('Cash Flow')
# for item in parse.cash_flow_period(papers):
#     print(item.__dict__)
# print('Transactions')
# for item in parse.transactions():
#     print(item.__dict__)
# print('Nominal')
# for item in parse.nominal_paper():
#     print(item.__dict__)
