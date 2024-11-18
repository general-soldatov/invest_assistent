# from pydantic import BaseModel
from datetime import date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Transactions(Base):
    __tablename__ = 'transactions'

    id_deal: Mapped[int] = mapped_column(primary_key=True) #Номер сделки
    name_paper: Mapped[str] = mapped_column() # Наименование ЦБ
    date_deal: Mapped[date] = mapped_column() #Дата заключения
    type_deal: Mapped[str] = mapped_column() #Вид
    count_paper: Mapped[int] = mapped_column() #Количество, шт.
    price_paper: Mapped[float] = mapped_column() #Цена
    coupon_add_paper: Mapped[float] = mapped_column() #НКД
    broker_comission: Mapped[float] = mapped_column() #Комиссия Брокера
    market_comission: Mapped[float] = mapped_column() #Комиссия Биржи


class Enrollments(Base):
    __tablename__ = 'enrollments'

    id_: Mapped[int] = mapped_column(primary_key=True, autoincrement = "auto")
    name_paper: Mapped[str] = mapped_column()
    date_operation: Mapped[date] = mapped_column()
    sum_enroll: Mapped[float] = mapped_column()

class WriteDowns(Base):
    __tablename__ = 'write-downs'

    id_: Mapped[int] = mapped_column(primary_key=True, autoincrement = "auto")
    name_paper: Mapped[str] = mapped_column()
    date_operation: Mapped[date] = mapped_column()
    sum_down: Mapped[float] = mapped_column()

class SecurityDirectory(Base):
    __tablename__ = 'security-directory'

    name_paper: Mapped[str] = mapped_column(primary_key=True)
    code_paper: Mapped[str] = mapped_column()
    isin_paper: Mapped[str] = mapped_column()
    emitent: Mapped[str] = mapped_column()
    type_paper: Mapped[str] = mapped_column()
    series_paper: Mapped[str] = mapped_column()
