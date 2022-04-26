from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase


class Client(SqlAlchemyBase):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    phone = Column(String)
    email = Column(String, unique=True)