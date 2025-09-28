# A2A/AP2 Multi-Agent Shopping System

A sophisticated multi-agent shopping system implementing Agent-to-Agent (A2A) and Agent Payment Protocol (AP2) with Google ADK-powered LLM capabilities.

## Features

### Core Capabilities
- **A2A Protocol Implementation**: Structured agent-to-agent messaging with session tracking
- **AP2 Protocol Integration**: Agent payment protocol with session management
- **Google ADK Integration**: Advanced LLM capabilities for intelligent decision making
- **Multi-Agent Architecture**: Shopping agents, merchant agents, and payment processors
- **Real-time Processing**: Asynchronous message handling and transaction processing

### Interactive Modes
1. **Interactive Chat Interface** (`chat_interface.py`) - Real-time conversation with the shopping assistant
2. **Demo Mode** (`main.py`) - Automated demonstration scenarios
3. **Test Mode** (`test_demo.py`) - Simplified testing and validation

## Quick Start

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
```

### Interactive Chat Mode (Recommended)
```bash
python chat_interface.py
```

**Features:**
- Real-time chat with AI shopping assistant
- Natural language product search
- Multi-merchant comparison
- Interactive commands (`/help`, `/status`, `/inventory`, `/quit`)
- Session-based shopping experience

**Example Usage:**
```
🧑 You: I need a laptop for programming under $1000
🤖 Assistant: 🤔 Processing your request...
🤖 Assistant: I found several great options for programming laptops under $1000...

🧑 You: /inventory
🤖 Assistant: 🏪 **Available Products**
...

🧑 You: /quit
🤖 Assistant: 👋 Thank you for using our shopping service! Goodbye!
```

### Demo Mode
```bash
python main.py
```
Runs automated scenarios demonstrating the complete A2A/AP2 workflow.

### Test Mode
```bash
python test_demo.py
```
Simplified testing of core functionality.

## System Architecture

### Agents
- **Shopping Agent**: Handles user requests, coordinates with merchants, manages transactions
- **Merchant Agents**: Provide product information, pricing, and availability
- **Payment Processor**: Handles payment processing and transaction completion

### Protocols
- **A2A (Agent-to-Agent)**: Message types include IntentMandate, CartMandate, ContactAddress, PaymentMandate, PaymentResult
- **AP2 (Agent Payment Protocol)**: Session management, message history, participant tracking

### LLM Integration
- **Google ADK**: Powers intelligent product search, merchant selection, and natural language responses
- **Fallback Responses**: System continues to function without API keys using predefined responses

## Available Merchants

1. **TechMart Electronics** (⭐ 4.5/5, 🚚 2-3 days)
   - Gaming laptops, smartphones, tablets, headphones, monitors

2. **Budget Electronics Co** (⭐ 4.0/5, 🚚 5-7 days)
   - Affordable electronics and budget-friendly options

3. **Premium Gadgets** (⭐ 4.8/5, 🚚 1-2 days)
   - High-end devices including MacBooks, iPhones, iPads

## Chat Commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands and usage examples |
| `/status` | Display system status and statistics |
| `/inventory` | View available products from all merchants |
| `/quit` | Exit the chat interface |

## Message Flow

```
1. User Request → Shopping Agent (IntentMandate via A2A)
2. Shopping Agent → Merchant Agents (CartMandate via A2A)
3. Merchant Agents → Shopping Agent (ContactAddress via A2A)
4. Shopping Agent → Best Merchant (cart update)
5. Shopping Agent → Payment Processor (PaymentMandate via A2A)
6. Payment Processor → Shopping Agent (PaymentResult via A2A)
7. Shopping Agent → User (completion notification)
```

## Configuration

### Environment Variables
```bash
# Required for LLM functionality
GOOGLE_API_KEY=your_google_api_key_here
```

### Dependencies
- **google-adk**: Google Agent Development Kit for LLM capabilities
- **ap2**: Official Google AP2 library
- **python-dotenv**: Environment variable management
- **asyncio**: Asynchronous programming support

## Development

### File Structure
```
├── chat_interface.py      # Interactive chat interface
├── main.py               # Demo scenarios
├── test_demo.py          # Simple testing
├── shopping_agent.py     # Shopping agent implementation
├── merchant_agent.py     # Merchant agent implementation
├── payment_processor.py  # Payment processing agent
├── protocols.py          # A2A/AP2 protocol implementations
├── ap2_components.py     # Custom AP2 components
├── requirements.txt      # Python dependencies
└── .env                 # Environment variables
```

### Key Features Implemented
- ✅ Clean code without unnecessary debug output
- ✅ Official Google AP2 library integration
- ✅ Google ADK for LLM capabilities
- ✅ Interactive chat interface
- ✅ Multi-agent communication
- ✅ Session-based transaction tracking
- ✅ Asynchronous processing
- ✅ Error handling and fallback responses

## Usage Examples

### Shopping Queries
- "I need a laptop for gaming under $1500"
- "Show me the cheapest smartphones available"
- "I want wireless headphones with noise canceling"
- "Looking for a professional tablet for design work"
- "What monitors do you have for programming?"

### System Commands
- "/status" - Check system health
- "/inventory" - Browse all available products
- "/help" - Get assistance and command list

## Technical Details

### A2A Protocol Features
- Unique message IDs and timestamps
- Session-based conversation tracking
- Reliable delivery and acknowledgment
- Structured message types for different transaction phases

### AP2 Protocol Features
- Payment processing and transaction management
- Message history and audit trail
- Participant tracking and session lifecycle
- Integration with official Google AP2 library

### LLM Capabilities
- Natural language intent parsing
- Intelligent product matching
- Merchant selection optimization
- Conversational response generation

## Troubleshooting

### Common Issues
1. **Missing Google API Key**: System will use fallback responses
2. **Network Issues**: Check internet connection for LLM features
3. **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`

### Getting Help
- Use `/help` command in chat mode
- Check system status with `/status`
- Review error messages for specific issues

---

🛒 **Happy Shopping with A2A/AP2 Multi-Agent System!** 🤖
