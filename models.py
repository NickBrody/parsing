from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///games.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Game(Base):
    """Класс Game, для работы с базой данных.
    id - поле типа Integer, являющееся первичным ключом (primary_key=True).
    game_name - поле типа String.
    platform - поле типа String.
    price - поле типа String.
    link - поле типа String."""

    __tablename__ = "Games"
    id = Column(Integer, primary_key=True, index=True)
    game_name = Column(String, index=True)
    platform = Column(String, index=True)
    price = Column(String, index=True)
    link = Column(String, index=True)
