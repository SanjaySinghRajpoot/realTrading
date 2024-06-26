from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    quantity: float
    price: float
    side: int

class OrderUpdate(BaseModel):
    updated_quantity: float
    updated_price: float

class OrderBase(BaseModel):
    quantity: float
    price: float
    side: int
    alive: bool

# Response models
class GetOrderBase(BaseModel):
    order_price: float
    order_quantity: float
    average_traded_price: float
    traded_quantity: float
    order_alive: bool


class TradeBase(BaseModel):
    execution_timestamp: datetime
    price: float
    quantity: float
    bid_order_id: int
    ask_order_id: int
