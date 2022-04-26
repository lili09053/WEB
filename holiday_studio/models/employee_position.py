from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class EmployeePosition(SqlAlchemyBase):
    __tablename__ = 'employee_position'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_employee = Column(ForeignKey('employee.id'), nullable=False)
    id_position = Column(ForeignKey('position.id'), nullable=False)

    employee = relationship('Employee')
    position = relationship('Position')