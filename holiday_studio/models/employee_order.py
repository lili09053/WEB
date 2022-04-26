from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class EmployeeOrder(SqlAlchemyBase):
    __tablename__ = 'employee_order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_employee = Column(ForeignKey('employee.id'), nullable=False)
    id_order = Column(ForeignKey('order.id'), nullable=False)

    employee = relationship('Employee')
    order = relationship('Order')