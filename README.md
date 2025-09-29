# A2A and AP2 Based Multi-Agent System

A sophisticated multi-agent system implementing the Agent Payment Protocol (AP2) with Google ADK-powered AI agents for autonomous shopping, payment processing, and merchant services.

## Overview

This project demonstrates a complete AP2 protocol implementation using three AI agents that communicate via the Agent-to-Agent (A2A) protocol to handle the entire e-commerce flow from product search to payment completion.

## Architecture

### Core Agents

1. **Shopping Agent** (`shopping_agent/agent.py`)
   - Handles user requests and orchestrates the entire shopping flow
   - Implements AP2 Intent Mandates and Cart Mandates
   - Manages A2A communication with merchant and credentials provider
   - Processes the complete 13-step AP2 payment flow

2. **Merchant Agent** (`merchant_agent/agent.py`)
   - Manages product catalog and inventory
   - Validates cart items and pricing
   - Signs cart mandates with cryptographic guarantees
   - Handles order fulfillment and tracking

3. **Credentials Provider Agent** (`credentials_provider/agent.py`)
   - Manages user payment credentials securely
   - Handles payment authorization and OTP verification
   - Processes payment capture and settlement
   - Maintains transaction history and audit trails

### Protocol Implementation

#### A2A Protocol Features
- Structured message format with protocol versioning
- Agent discovery and capability exchange
- Session establishment with cryptographic signatures
- Secure message routing between agents

#### AP2 Protocol Features
- Intent Mandates for human-not-present purchases
- Cart Mandates with merchant fulfillment guarantees
- Payment Mandates with secure credential tokenization
- Complete audit trail and transaction logging

## Dependencies

```bash
google-adk>=0.2.0      # Google Agent Development Kit
a2a-sdk>=0.3.7         # Official A2A Python SDK
requests>=2.31.0       # HTTP client library
fastapi>=0.104.0       # Web framework (for future API endpoints)
uvicorn>=0.24.0        # ASGI server
pydantic>=2.5.0        # Data validation
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/meetrais/A2A_AP2.git
   cd A2A_AP2
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # Create .env file with your Google API key
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```

## Usage

### Running Individual Agents

Each agent can be run independently using the Google ADK:

```python
from shopping_agent.agent import root_agent as shopping_agent
from merchant_agent.agent import root_agent as merchant_agent
from credentials_provider.agent import root_agent as credentials_provider

# Start shopping agent conversation
response = shopping_agent.chat("I want to buy a laptop")
```

### Complete AP2 Flow

The shopping agent implements the full 13-step AP2 protocol:

1. `transfer_to_agent` - Establish A2A connection with merchant
2. `create_intent_mandate` - Create purchase authorization
3. `find_products` - Search merchant catalog via A2A
4. `update_chosen_cart_mandate` - Select specific product
5. `transfer_to_agent` - Connect to credentials provider
6. `get_shipping_address` - Retrieve user address via A2A
7. `update_cart` - Calculate totals and shipping
8. `get_payment_methods` - Get user payment options
9. `get_payment_credential_token` - Generate secure token
10. `create_payment_mandate` - Create payment authorization
11. `sign_mandates_on_user_device` - Cryptographic signing
12. `send_signed_payment_mandate_to_credentials_provider` - A2A transmission
13. `initiate_payment_with_otp` - Complete with OTP verification

## Features

### Shopping Agent Capabilities
- Natural language product search
- Multi-merchant comparison and selection
- Complete AP2 payment flow automation
- A2A protocol communication
- Cryptographic mandate signing
- OTP verification handling

### Merchant Agent Capabilities
- Product catalog management (laptops, phones, tablets)
- Real-time inventory validation
- Cart mandate signing with fulfillment guarantees
- Inventory reservation during checkout
- Order fulfillment and tracking

### Credentials Provider Capabilities
- Secure payment method management
- User profile and address management
- Payment authorization with risk scoring
- OTP generation and verification
- Transaction capture and settlement
- Complete audit trail maintenance

## Sample Product Catalog

The merchant agent provides these product categories:

**Laptops:**
- High-performance laptop ($1,599.99)
- Mid-range business laptop ($1,129.50)
- Entry-level student laptop ($789.00)

**Mobile Devices:**
- Flagship smartphone ($999.99)
- Professional tablet ($649.99)

## Payment Methods Supported

**Credit Cards:**
- American Express
- Visa
- Mastercard

**Bank Transfers:**
- ACH payments
- Direct bank transfers

## Security Features

### Cryptographic Security
- SHA-256 signatures for all mandates
- Secure credential tokenization
- A2A message encryption
- User device signing

### Payment Security
- Multi-factor authentication (OTP)
- Risk scoring and fraud detection
- PCI DSS compliant simulation
- Complete transaction audit trails

### A2A Protocol Security
- Message authentication and integrity
- Session-based communication
- Agent capability verification
- Secure routing and delivery

## A2A SDK Integration

This project uses the official [A2A Python SDK](https://github.com/a2aproject/a2a-python) to simplify A2A protocol implementation:

### SDK Features Used
- **Message Types**: `Message`, `TextPart`, `Role` from `a2a.types`
- **Client**: `Client` from `a2a.client` for A2A communication
- **JSON Serialization**: `model_dump_json()` and `model_validate_json()` for message handling

### Implementation Examples

**Creating A2A Messages:**
```python
from a2a.types import Message, TextPart, Role

# Create A2A message using SDK types
a2a_message = Message(
    role=Role.user,
    parts=[TextPart(text="Product search request")],
    message_id=str(uuid.uuid4()),
    metadata={
        "sender_agent": "shopping_agent",
        "receiver_agent": "merchant_agent",
        "capabilities_required": ["product_search"]
    }
)
```

**Processing A2A Messages:**
```python
# Parse incoming A2A message using SDK
incoming_message = Message.model_validate_json(message_json)

# Create response using A2A SDK types
response_message = Message(
    role=Role.agent,
    parts=[TextPart(text="Request processed")],
    message_id=str(uuid.uuid4()),
    metadata={
        "sender_agent": "merchant_agent",
        "in_response_to": incoming_message.message_id
    }
)
```

### Benefits of SDK Usage
- **Standardized Types**: Ensures compliance with A2A protocol specifications
- **Type Safety**: Pydantic-based models provide validation and type checking
- **JSON Serialization**: Built-in methods for converting to/from JSON
- **Error Handling**: Graceful fallback when SDK operations fail
- **Future Compatibility**: Automatic updates with protocol evolution

## Development

### Project Structure
```
├── shopping_agent/
│   ├── __init__.py
│   └── agent.py           # Main shopping agent with AP2 flow
├── merchant_agent/
│   ├── __init__.py
│   └── agent.py           # Product catalog and fulfillment
├── credentials_provider/
│   ├── __init__.py
│   └── agent.py           # Payment processing and credentials
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
└── .env                  # Environment variables
```

### Key Implementation Details

**A2A Message Format:**
```json
{
  "protocol": "A2A",
  "version": "1.0",
  "message_id": "uuid",
  "sender_agent": "shopping_agent",
  "receiver_agent": "merchant_agent",
  "timestamp": "ISO-8601",
  "payload": {...},
  "security": {"signature": "..."}
}
```

**AP2 Mandate Structure:**
```json
{
  "ap2_protocol": "intent_mandate",
  "mandate_id": "uuid",
  "user_id": "user_identifier",
  "item_description": "product description",
  "expires": "ISO-8601",
  "user_signature": "cryptographic_hash"
}
```

## Testing

The system includes mock data and simulation for:
- Product inventory and pricing
- User payment methods and addresses
- Transaction processing and settlement
- OTP verification (demo code: "123")

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

This is a demonstration project showcasing AP2 protocol implementation with Google ADK. Contributions for educational and research purposes are welcome.
