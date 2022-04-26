from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class ClientOrder(SqlAlchemyBase):
    __tablename__ = 'client_order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_client = Column(ForeignKey('client.id'), nullable=False)
    id_order = Column(ForeignKey('order.id'), nullable=False)

    client = relationship('Client')
    Order = relationship('Order')