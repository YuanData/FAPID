from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from order.database import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    order_type = Column(String)
    symbol = Column(String)
    price = Column(Float)
    volume = Column(Integer)

    orderowner = relationship("Account", back_populates="orders")


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String)
    email = Column(String)
    password = Column(String)

    orders = relationship('Order', back_populates="orderowner")
