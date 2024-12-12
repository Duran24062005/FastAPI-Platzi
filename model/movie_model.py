from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    password = Column(String)

class User2(Base):
    __tablename__ = 'users2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    password = Column(String)
