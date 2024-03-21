from fastapi import FastAPI, Depends, Request, Form, status
from starlette.responses import RedirectResponse
from database import SessionLocal, engine
from schemas import Order
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

    def place_order(self, order):
        if order.side == 1:  # Buy order
            self.match_ask(order)
            if order.price in self.orders:
                self.orders[order.price].append(order)
            else:
                self.orders[order.price] = [order]
        elif order.side == -1:  # Sell order
            self.match_bid(order)
            if order.price in self.orders:
                self.orders[order.price].append(order)
            else:
                self.orders[order.price] = [order]
        else:
            raise HTTPException(status_code=400, detail="Invalid order side")

    def match_bid(self, order):
        for price in sorted(self.orders.keys(), reverse=True):
            if price >= order.price:
                for ask in self.orders[price]:
                    if ask.quantity >= order.quantity:
                        self.execute_trade(order, ask)
                        self.orders[price].remove(ask)
                        if not self.orders[price]:
                            del self.orders[price]
                        return
                    else:
                        self.execute_trade(order, ask)
                        order.quantity -= ask.quantity
                        self.orders[price].remove(ask)
                        if not self.orders[price]:
                            del self.orders[price]
        print("No matching ask orders")

    def match_ask(self, order):
        for price in sorted(self.orders.keys()):
            if price <= order.price:
                for bid in self.orders[price]:
                    if bid.quantity >= order.quantity:
                        self.execute_trade(bid, order)
                        self.orders[price].remove(bid)
                        if not self.orders[price]:
                            del self.orders[price]
                        return
                    else:
                        self.execute_trade(bid, order)
                        order.quantity -= bid.quantity
                        self.orders[price].remove(bid)
                        if not self.orders[price]:
                            del self.orders[price]
        print("No matching bid orders")

    def execute_trade(self, bid, ask):
        traded_quantity = min(bid.quantity, ask.quantity)
        if traded_quantity > 0:
            print(f"Trade: Bid {bid.order_id} matched with Ask {ask.order_id} - Price: {ask.price}, Quantity: {traded_quantity}")
            bid.quantity -= traded_quantity
            ask.quantity -= traded_quantity
            #save this in the database


engine = MatchingEngine()

@app.post("/place-order")
async def place_order(order: Order):
    engine.place_order(order)
    return {"message": "Order placed successfully"}

@app.get("/")
async def home():
    return {"message":"hello world from matching server"}


if __name__ == "__main__":
 uvicorn.run("main:app", host="0.0.0.0", port=8081,reload=True)  