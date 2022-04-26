from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Employee(SqlAlchemyBase, UserMixin):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String, unique=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)