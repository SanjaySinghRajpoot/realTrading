from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    quantity: int
    price: int
    side: int
