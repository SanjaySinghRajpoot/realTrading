from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    execution_timestamp = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    bid_order_id = Column(Integer,  nullable=False)
    ask_order_id = Column(Integer,  nullable=False)
