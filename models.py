from sqlalchemy import create_engine, Integer, Column, String, Date, Float, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, declarative_base



engine = create_engine("sqlite:///games.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()



class Game(Base):
    __tablename__ = 'Games'
    id = Column(Integer, primary_key=True, index=True)
    game_name = Column(String, index=True)
    price = Column(String, index=True)
    link = Column(String, index=True)
