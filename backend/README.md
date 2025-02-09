# Insurance Bidding System Backend

Django-based backend system for the real-time insurance bidding platform.

## Technology Stack

- Django with Django-Ninja for REST API
- SQLite database
- WebSocket server for real-time updates
- Async worker for bid processing
- JWT authentication

## Core Components

### API Endpoints

- Quote management
- Bid submission and processing
- Winner confirmation
- Session management

### WebSocket Server

- Real-time bid broadcasting
- Session status updates
- Timer notifications
- Connection management

### Database Models

- Quotes
- Bids
- Carriers
- Consumers
- Transactions

### Background Tasks

- Bid session timers
- Confirmation deadlines
- Rate limiting
- Data cleanup

## Data Flow

- Quote creation and validation
- Bid processing and broadcasting
- Winner selection and confirmation
- Transaction finalization