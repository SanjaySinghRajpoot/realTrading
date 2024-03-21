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
