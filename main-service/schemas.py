from pydantic import BaseModel


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