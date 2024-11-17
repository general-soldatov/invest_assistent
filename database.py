from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id_: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    e_mail: Mapped[str] = mapped_column()


def create_user(Session: sessionmaker, id_, name, email):
    user = User(id_=id_, name=name, e_mail=email)

    with Session() as session:
        session.add(user)
        session.commit()

def get_by_name(name: str, Session) -> list[User]:
    query = select(User).where(User.name == name)
    db_object = Session().scalars(query).one()
    return db_object

def update(name: str, name_old: str, Session) -> None:
    data: User = get_by_name(name_old, Session)
    with Session() as session:
        data.name = name
        session.merge(data)
        session.commit()


def delete(name: str, session) -> User:
    query = select(User).where(User.name == name)
    db_object = session.scalars(query).one()
    session.delete(db_object)
    return db_object

def main():
    engine = create_engine('sqlite:///my-database.db')
    Session = sessionmaker(engine)
    # Base.metadata.create_all(engine)
    # Base.metadata.drop_all(engine)

    # update('yura', 'User_Daa', Session)
    # create_user(Session, 22, 'User_Daa', 'example@example.com')
    # print(get_by_name('yura', Session).__dict__)




if __name__ == '__main__':
    main()
