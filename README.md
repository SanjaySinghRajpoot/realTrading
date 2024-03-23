# Real Trading System

This project is a simulation of an order API that allows users to place, modify, cancel, and fetch orders for buying and selling instruments/stocks. It includes functionalities to provide a CRUD interface, a WebSocket for trade updates, and another WebSocket for order book snapshots. The system is divided into two microservices: `main-service` and `matching-service`, connected to a central PostgreSQL database called `realtrading-db`.

## Features

### 1. CRUD Interface

- **Place Order [POST]:** Allows users to place a bid or ask order with quantity, price, and side.
- **Modify Order [PUT]:** Enables users to update the quantity and price of an existing order.
- **Cancel Order [DELETE]:** Allows users to cancel an order if it has not yet been traded.
- **Fetch Order [GET]:** Retrieves information about a specific order, including price, quantity, average traded price, traded quantity, and order status.
- **Get All Orders [GET]:** Returns all orders placed.
- **Get All Trades [GET]:** Returns all trades that have taken place.

### 2. WebSockets

- **Trade Update WebSocket:** Sends updates whenever a trade is executed, providing information such as execution timestamp, price, quantity, bid order ID, and ask order ID.
- **Order Book Snapshot WebSocket:** Sends a snapshot of the order book with 5 levels of both bid and ask depth every second, including price and quantity.

## Setup Procedure

1. Clone the repository: `git clone https://github.com/yourusername/real-trading-system.git`
2. Navigate to the project directory: `cd real-trading-system`
3. Ensure you have Docker and Docker Compose installed on your system.
4. Run the PostgreSQL server using Docker Compose: `docker-compose up -d`
5. Start the `main-service` and `matching-service` using uvicorn:
    - For `main-service`: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
    - For `matching-service`: `uvicorn matching:app --reload --host 0.0.0.0 --port 8001`
6. Access the application through the provided endpoints:
    - `main-service` REST API: http://localhost:8000/
    - `matching-service` WebSocket for trade updates: ws://localhost:8001/trade_updates
    - `main-service` WebSocket for order book snapshots: ws://localhost:8000/order_book_snapshot

## Docker Compose

The project includes a Docker Compose YAML file (`docker-compose.yml`) to facilitate easy setup of the PostgreSQL database. To use Docker Compose:

1. Make sure you have Docker and Docker Compose installed.
2. Navigate to the project directory.
3. Run `docker-compose up -d` to start the PostgreSQL database container.
4. Follow the setup procedure mentioned above to start the microservices.
