from fastapi import FastAPI, HTTPException, WebSocket, BackgroundTasks, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import update
from models import Order, Base, Trade
from schemas import OrderCreate, OrderUpdate, OrderBase, TradeBase
from database import SessionLocal, engine
from typing import List
import requests

import uvicorn
import asyncio

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


# Place order
@app.post("/orders", response_model=int)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    if order.quantity <= 0 or order.price <= 0:
        raise HTTPException(status_code=400, detail="Invalid quantity or price")
    if order.side not in [-1, 1]:
        raise HTTPException(status_code=400, detail="Invalid side, must be -1 or 1")
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    payload = {
    "order_id": db_order.id,
    "quantity": order.quantity,
    "price": order.price,
    "side": order.side
    }

    url = "http://matching-service:8001/place-order"  

    response = requests.post(url, json=payload)
    print(response)

    #send a http request to matching service

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
@app.get("/orders", response_model=List[OrderBase])
def fetch_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).limit(100).all()

# get all trades from the trades table
@app.get("/trades", response_model=List[TradeBase])
def fetch_all_orders(db: Session = Depends(get_db)):
    return db.query(Trade).limit(100).all()

# Background task to send order book snapshot to WebSocket clients
async def send_order_book_snapshot(websocket: WebSocket, db: Session):
    while True:
        # Query orders from database
        bid_orders = db.query(Order).filter(Order.side == 1).order_by(Order.price.desc()).limit(5).all()
        ask_orders = db.query(Order).filter(Order.side == -1).order_by(Order.price.asc()).limit(5).all()

        # Prepare order book snapshot
        order_book_snapshot = {
            "bids": [{"price": order.price, "quantity": order.quantity} for order in bid_orders],
            "asks": [{"price": order.price, "quantity": order.quantity} for order in ask_orders]
        }

        # Send order book snapshot to all WebSocket clients
        await websocket.send_json(order_book_snapshot)

        # Wait for 1 second before sending the next snapshot
        await asyncio.sleep(1)

@app.websocket("/ws_order_book")
async def websocket_endpoint(websocket: WebSocket, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        # Add WebSocket connection to the background task
        print("WebSocket connection established.")
        asyncio.create_task(send_order_book_snapshot(websocket, db))
        # Keep the WebSocket connection open
        while True:
            await websocket.receive_text()
    except Exception as e:
        print("Error:", e)



html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws_order_book");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


