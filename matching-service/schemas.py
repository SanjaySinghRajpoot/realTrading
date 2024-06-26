from pydantic import BaseModel

class OrderBase(BaseModel):
    order_id: int
    quantity: int
    price: int
    side: int
