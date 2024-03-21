from fastapi import FastAPI, HTTPException, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import update
from schemas import OrderCreate, OrderUpdate, OrderBase
from database import SessionLocal, engine

from models import Order, Base
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
        print("this is working")
    finally:
        db.close()

@app.get("/")
async def home(db: Session = Depends(get_db)):
    return {"message":"hello world"}


# Place order
@app.post("/orders", response_model=int)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    if order.quantity <= 0 or order.price <= 0:
        raise HTTPException(status_code=400, detail="Invalid quantity or price")
    if order.side not in [-1, 1]:
        raise HTTPException(status_code=400, detail="Invalid side, must be -1 or 1")
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order.id

# Modify order
@app.put("/orders/{order_id}/", response_model=bool)
def modify_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.alive == False:
        raise HTTPException(status_code=400, detail="Order is already cancelled")
    db.execute(update(Order).where(Order.id == order_id).values(quantity=order_update.updated_quantity, price=order_update.updated_price))
    db.commit()
    return True

# Cancel order
@app.delete("/orders/{order_id}", response_model=bool)
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.alive == False:
        raise HTTPException(status_code=400, detail="Order is already cancelled")
    order.alive = False
    db.commit()
    return True

# All orders
@app.get("/orders", response_model=list[OrderBase])
def fetch_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


if __name__ == "__main__":
 uvicorn.run("main:app", host="0.0.0.0", port=8080,reload=True)  