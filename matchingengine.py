class Order:
    def __init__(self, order_id, quantity, price, side):
        self.order_id = order_id
        self.quantity = quantity
        self.price = price
        self.side = side

class MatchingEngine:
    def __init__(self):
        self.orders = {}  # Dictionary to store orders based on their side and price

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
            print("Invalid order side")

    def match_bid(self, order):
        for price in sorted(self.orders.keys(), reverse=True):
            if price >= order.price:
                for ask in self.orders[price]:
                    if ask.quantity >= order.quantity:
                        self.execute_trade(order, ask)
                        self.orders[price].remove(ask)
                        if not self.orders[price]:  # Remove the price key if no more orders at that price
                            del self.orders[price]
                        return
                    else:
                        self.execute_trade(order, ask)
                        order.quantity -= ask.quantity
                        self.orders[price].remove(ask)
                        if not self.orders[price]:  # Remove the price key if no more orders at that price
                            del self.orders[price]
        print("No matching ask orders")

    def match_ask(self, order):
        for price in sorted(self.orders.keys()):
            if price <= order.price:
                for bid in self.orders[price]:
                    if bid.quantity >= order.quantity:
                        self.execute_trade(bid, order)
                        self.orders[price].remove(bid)
                        if not self.orders[price]:  # Remove the price key if no more orders at that price
                            del self.orders[price]
                        return
                    else:
                        self.execute_trade(bid, order)
                        order.quantity -= bid.quantity
                        self.orders[price].remove(bid)
                        if not self.orders[price]:  # Remove the price key if no more orders at that price
                            del self.orders[price]
        print("No matching bid orders")

    def execute_trade(self, bid, ask):
        traded_quantity = min(bid.quantity, ask.quantity)
        if traded_quantity > 0:
            print(f"Trade: Bid {bid.order_id} matched with Ask {ask.order_id} - Price: {ask.price}, Quantity: {traded_quantity}")
            bid.quantity -= traded_quantity
            ask.quantity -= traded_quantity

# Example usage
            
# (self, order_id, quantity, price, side)
engine = MatchingEngine()
order1 = Order(1, 5, 120, 1) #buy  
order2 = Order(2, 10, 120, -1)  #sell
order3 = Order(3, 5, 120, 1)  

order4 = Order(4, 5, 120, -1)  
order5 = Order(5, 5, 120, 1)  


engine.place_order(order1)
engine.place_order(order2)
engine.place_order(order3)
engine.place_order(order4)
engine.place_order(order5)
