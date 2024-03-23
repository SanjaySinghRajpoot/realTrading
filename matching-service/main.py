from fastapi import FastAPI, HTTPException, WebSocket, Depends, WebSocketDisconnect
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from schemas import Order
from models import Trade
from datetime import datetime
import uvicorn


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
        print("this is working")
    finally:
        db.close()


class MatchingEngine:
    def __init__(self):
        self.orders = {}
        self.connection = None  # Set to store WebSocket connections

    async def place_order(self, order, db):
        if order.side == 1:  # Buy order
            await self.match_ask(order, db)
            if order.price in self.orders:
                self.orders[order.price].append(order)
            else:
                self.orders[order.price] = [order]
        elif order.side == -1:  # Sell order
            await self.match_bid(order, db)
            if order.price in self.orders:
                self.orders[order.price].append(order)
            else:
                self.orders[order.price] = [order]
        else:
            raise HTTPException(status_code=400, detail="Invalid order side")

    async def match_bid(self, order, db):
        for price in sorted(self.orders.keys(), reverse=True):
            if price >= order.price:
                for ask in self.orders[price]:
                    if ask.quantity >= order.quantity:
                        await self.execute_trade(order, ask, db)
                        self.orders[price].remove(ask)
                        if not self.orders[price]:
                            del self.orders[price]
                        return
                    else:
                        await self.execute_trade(order, ask, db)
                        order.quantity -= ask.quantity
                        self.orders[price].remove(ask)
                        if not self.orders[price]:
                            del self.orders[price]
        print("No matching ask orders")

    async def match_ask(self, order, db):
        for price in sorted(self.orders.keys()):
            if price <= order.price:
                for bid in self.orders[price]:
                    if bid.quantity >= order.quantity:
                        await self.execute_trade(bid, order, db)
                        self.orders[price].remove(bid)
                        if not self.orders[price]:
                            del self.orders[price]
                        return
                    else:
                        await self.execute_trade(bid, order, db)
                        order.quantity -= bid.quantity
                        self.orders[price].remove(bid)
                        if not self.orders[price]:
                            del self.orders[price]
        print("No matching bid orders")

    async def execute_trade(self, bid, ask, db):
        traded_quantity = min(bid.quantity, ask.quantity)
        if traded_quantity > 0:
            print(f"Trade: Bid {bid.order_id} matched with Ask {ask.order_id} - Price: {ask.price}, Quantity: {traded_quantity}")
            bid.quantity -= traded_quantity
            ask.quantity -= traded_quantity

            trade = Trade(execution_timestamp=datetime.now(),
                      price=ask.price,
                      quantity=traded_quantity,
                      bid_order_id=bid.order_id,
                      ask_order_id=ask.order_id)
            db.add(trade)
            db.commit()

            if self.connection is not None:
                    trade_data = {
                        "bid_order_id": bid.order_id,
                        "ask_order_id": ask.order_id,
                        "price": ask.price,
                        "quantity": min(bid.quantity, ask.quantity),
                        "execution_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    await self.connection.send_json(trade_data)
            else:
                print("WebSocket connection not established")
                return {"error": "WebSocket connection not established"}


engine = MatchingEngine()

@app.post("/place-order")
async def place_order(order: Order, db: Session = Depends(get_db)):
    await engine.place_order(order, db)
    return {"message": "Order placed successfully"}

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
            var ws = new WebSocket("ws://localhost:8001/ws");
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    engine.connection = websocket  # Add WebSocket connection to the set
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        engine.connection = None # Remove WebSocket connection from the set



if __name__ == "__main__":
 uvicorn.run("main:app", host="0.0.0.0", port=8081,reload=True)  