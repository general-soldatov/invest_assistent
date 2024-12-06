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

# from datetime import date

# birthday = date(1992, 10, 6)

# print('Название месяца:', birthday.strftime('%B'))
# print('Название дня недели:', birthday.strftime('%A'))
# print('Год:', birthday.strftime('%Y'))
# print('Месяц:', birthday.strftime('%m'))
# print('День:', birthday.strftime('%d'))

# andrew = date(1992, 8, 24)

# print(andrew.strftime('%Y-%j'))   # выводим дату в формате YYYY-day_number
# from mail_parse import MainPage
# from models.graph_plots import ByteGraph


# def main():
#     data = ByteGraph()
#     data.graph_1(MainPage().get_cash())
#     data.graph_bytes()

# if __name__ == "__main__":
#     main()
