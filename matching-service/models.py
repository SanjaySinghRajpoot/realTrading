from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    side = Column(Integer, nullable=False)  # 1 for buy, -1 for sell
    alive = Column(Boolean, default=True)

class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    execution_timestamp = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    bid_order_id = Column(Integer,  nullable=False)
    ask_order_id = Column(Integer,  nullable=False)
