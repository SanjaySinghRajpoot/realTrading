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
    - For `matching-service`: `uvicorn main:app --reload --host 0.0.0.0 --port 8001`
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



**Microservices Architecture for Trading Platform**


**Main Service:**

The Main Service is responsible for managing basic CRUD (Create, Read, Update, Delete) operations related to orders within the trading platform. It serves as the primary interface for users to interact with the system. Key functionalities of the Main Service include:

- **Order Management:** Allows users to perform CRUD operations on orders, providing essential functionalities such as placing, modifying, and canceling orders.
- **WebSocket Integration:** Opens a WebSocket connection to provide real-time updates of order history to clients. The service sends order updates at regular intervals (e.g., every 1 second) to ensure users receive timely information about the market.


**Matching Service:**

The Matching Service is dedicated to handling the complex logic of matching trades between buyers and sellers within the trading platform. Unlike the Main Service, it focuses solely on trade matching and does not perform CRUD operations on orders. Key functionalities of the Matching Service include:

- **Trade Matching:** Implements algorithms and rules for matching buy and sell orders based on predefined criteria such as price, quantity, and time priority.
- **WebSocket Integration:** Opens a WebSocket connection to notify clients whenever a trade is completed. This ensures that users receive immediate notifications about executed trades, enabling them to stay informed about market activity.


**Design Rationale:**

The decision to separate the Main Service and the Matching Service into distinct microservices is based on several considerations:

- **Scalability:** By decoupling order management (Main Service) from trade matching (Matching Service), we can scale each component independently based on its specific resource demands. This allows us to allocate resources more efficiently and handle varying levels of traffic effectively.
- **Performance Optimization:** The Main Service is optimized for handling CRUD operations, which are typically less computationally intensive compared to trade matching algorithms. Separating these concerns ensures that each service can be fine-tuned for optimal performance without impacting the overall system's responsiveness.
- **Modularity and Maintainability:** The microservices architecture promotes modularity and encapsulation of functionalities, making it easier to maintain and evolve the system over time. Changes to one service are less likely to impact others, facilitating agile development and deployment practices.

