from sqlalchemy import Column, Float, Integer, String
from .db_session import SqlAlchemyBase


class Position(SqlAlchemyBase):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    describtion = Column(String)
    oklad = Column(Float)