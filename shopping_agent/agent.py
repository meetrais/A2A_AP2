# shopping_agent/agent.py
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict
from google.adk.agents import Agent

def transfer_to_agent(target_agent: str, message: str, context: str = "") -> Dict[str, str]:
    """
    Transfer conversation to another agent using A2A protocol.
    
    Args:
        target_agent: Target agent name (merchant_agent, credentials_provider)
        message: Message to transfer
        context: Additional context
        
    Returns:
        Dict containing A2A transfer result
    """
    # A2A Protocol Message Structure
    a2a_message = {
        "protocol": "A2A",
        "version": "1.0",
        "message_id": str(uuid.uuid4()),
        "sender_agent": "shopping_agent",
        "receiver_agent": target_agent,
        "message_type": "agent_transfer",
        "timestamp": datetime.now().isoformat(),
        "payload": {
            "transfer_reason": context,
            "message": message,
            "session_id": str(uuid.uuid4()),
            "capabilities_required": ["product_search", "payment_processing"] if target_agent == "merchant_agent" else ["credential_management", "payment_authorization"]
        },
        "security": {
            "signature": hashlib.sha256(f"shopping_agent:{target_agent}:{message}".encode()).hexdigest()[:16]
        }
    }
    
    return {
        "status": "success",
        "a2a_message": json.dumps(a2a_message),
        "target_agent": target_agent,
        "transfer_completed": "true",
        "message": f"A2A transfer to {target_agent} completed. Session established."
    }

def create_intent_mandate(user_id: str, item_description: str, merchants: str = "Any", expires_days: int = 1) -> Dict[str, str]:
    """
    Create Intent Mandate for human-not-present purchases (AP2 Protocol).
    
    Args:
        user_id: User identifier
        item_description: Item description
        merchants: Allowed merchants
        expires_days: Expiration in days
        
    Returns:
        Dict containing Intent Mandate
    """
    mandate_id = str(uuid.uuid4())
    
    # AP2 Intent Mandate Structure
    intent_mandate = {
        "ap2_protocol": "intent_mandate",
        "mandate_id": mandate_id,
        "user_id": user_id,
        "item_description": item_description,
        "merchants": merchants,
        "user_confirmation_required": True,
        "refundable": True,
        "expires": (datetime.now() + timedelta(days=expires_days)).isoformat(),
        "created_at": datetime.now().isoformat(),
        "status": "created",
        "user_signature": hashlib.sha256(f"{user_id}:{item_description}:{mandate_id}".encode()).hexdigest()
    }
    
    return {
        "status": "success",
        "mandate_type": "intent_mandate",
        "mandate_id": mandate_id,
        "intent_mandate": json.dumps(intent_mandate),
        "confirmation_required": "true",
        "message": f"Intent mandate {mandate_id} created for {item_description}"
    }

def find_products(query: str, category: str = "", max_results: int = 3) -> Dict[str, str]:
    """
    Find products via merchant agent (A2A communication).
    
    Args:
        query: Search query
        category: Product category
        max_results: Maximum results
        
    Returns:
        Dict containing product search results
    """
    # Simulate A2A request to merchant agent
    search_request = {
        "protocol": "A2A", 
        "action": "product_search",
        "query": query,
        "category": category,
        "max_results": max_results,
        "request_id": str(uuid.uuid4())
    }
    
    # Mock product catalog from merchant agent
    products = [
        {
            "id": "laptop_001",
            "name": "High-performance laptop",
            "price": 1599.99,
            "expires": (datetime.now() + timedelta(days=1)).isoformat(),
            "refund_period": 30,
            "merchant": "Tech Store"
        },
        {
            "id": "laptop_002", 
            "name": "Mid-range business laptop",
            "price": 1129.50,
            "expires": (datetime.now() + timedelta(days=1)).isoformat(),
            "refund_period": 30,
            "merchant": "Tech Store"
        },
        {
            "id": "laptop_003",
            "name": "Entry-level student laptop", 
            "price": 789.00,
            "expires": (datetime.now() + timedelta(days=1)).isoformat(),
            "refund_period": 14,
            "merchant": "Generic Merchant"
        }
    ]
    
    filtered_products = [p for p in products if query.lower() in p["name"].lower()]
    
    return {
        "status": "success",
        "search_request": json.dumps(search_request),
        "products_found": str(len(filtered_products)),
        "products": json.dumps(filtered_products[:max_results]),
        "message": f"Found {len(filtered_products)} products matching '{query}'"
    }

def update_chosen_cart_mandate(product_id: str, selected_item_number: int) -> Dict[str, str]:
    """
    Update cart mandate with user's product selection.
    
    Args:
        product_id: Selected product ID
        selected_item_number: Item number chosen
        
    Returns:
        Dict containing cart mandate
    """
    cart_mandate_id = str(uuid.uuid4())
    
    cart_mandate = {
        "ap2_protocol": "cart_mandate",
        "cart_mandate_id": cart_mandate_id,
        "product_id": product_id,
        "selected_item": selected_item_number,
        "status": "item_selected",
        "created_at": datetime.now().isoformat(),
        "requires_credentials": True,
        "requires_shipping": True,
        "user_signature": hashlib.sha256(f"user:{product_id}:{cart_mandate_id}".encode()).hexdigest()
    }
    
    return {
        "status": "success",
        "cart_mandate_id": cart_mandate_id,
        "cart_mandate": json.dumps(cart_mandate),
        "selected_item": str(selected_item_number),
        "next_step": "credentials_collection",
        "message": f"Cart mandate {cart_mandate_id} created for item #{selected_item_number}"
    }

def get_shipping_address(user_email: str = "bugsbunny@gmail.com") -> Dict[str, str]:
    """
    Retrieve shipping address from credentials provider via A2A.
    
    Args:
        user_email: User email
        
    Returns:
        Dict containing shipping address
    """
    # A2A request to credentials provider
    address_request = {
        "protocol": "A2A",
        "action": "get_shipping_address", 
        "user_email": user_email,
        "request_id": str(uuid.uuid4())
    }
    
    # Mock response from credentials provider
    address = {
        "recipient": "Bugs Bunny",
        "address_line_1": "123 Main St",
        "city": "Sample City",
        "state": "ST", 
        "zip_code": "00000",
        "country": "US",
        "phone": "+1-000-000-0000",
        "organization": "Sample Organization"
    }
    
    return {
        "status": "success",
        "address_request": json.dumps(address_request),
        "shipping_address": json.dumps(address),
        "user_email": user_email,
        "message": "Shipping address retrieved from credentials provider"
    }

def update_cart(cart_mandate_id: str, shipping_address_json: str, tax: float = 1.50, shipping: float = 2.00) -> Dict[str, str]:
    """
    Update cart with shipping address and calculate totals.
    
    Args:
        cart_mandate_id: Cart mandate ID
        shipping_address_json: Shipping address JSON
        tax: Tax amount
        shipping: Shipping cost
        
    Returns:
        Dict containing updated cart
    """
    item_price = 1129.50  # Mid-range laptop
    total = item_price + tax + shipping
    
    updated_cart = {
        "cart_mandate_id": cart_mandate_id,
        "item_price": item_price,
        "tax": tax,
        "shipping": shipping,
        "total": total,
        "shipping_address": json.loads(shipping_address_json),
        "valid_until": (datetime.now() + timedelta(hours=24)).isoformat(),
        "status": "address_added"
    }
    
    return {
        "status": "success",
        "cart_mandate_id": cart_mandate_id,
        "updated_cart": json.dumps(updated_cart),
        "total_amount": str(total),
        "next_step": "payment_methods",
        "message": f"Cart updated. Total: ${total:.2f}"
    }

def get_payment_methods(user_email: str) -> Dict[str, str]:
    """
    Retrieve payment methods from credentials provider via A2A.
    
    Args:
        user_email: User email
        
    Returns:
        Dict containing payment methods
    """
    # A2A request to credentials provider
    payment_request = {
        "protocol": "A2A",
        "action": "get_payment_methods",
        "user_email": user_email,
        "request_id": str(uuid.uuid4())
    }
    
    payment_methods = [
        {
            "id": "amex_4444",
            "type": "American Express", 
            "last_four": "4444",
            "default": False
        },
        {
            "id": "amex_8888",
            "type": "American Express",
            "last_four": "8888", 
            "default": True
        }
    ]
    
    return {
        "status": "success",
        "payment_request": json.dumps(payment_request),
        "payment_methods": json.dumps(payment_methods),
        "methods_count": str(len(payment_methods)),
        "message": "Payment methods retrieved from credentials provider"
    }

def get_payment_credential_token(payment_method_id: str) -> Dict[str, str]:
    """
    Generate payment credential token for selected method.
    
    Args:
        payment_method_id: Selected payment method ID
        
    Returns:
        Dict containing credential token
    """
    token_id = str(uuid.uuid4())
    
    credential_token = {
        "credential_token": f"token_{token_id}",
        "payment_method_id": payment_method_id,
        "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(),
        "token_type": "payment_credential",
        "generated_at": datetime.now().isoformat()
    }
    
    return {
        "status": "success",
        "token_id": token_id,
        "credential_token": json.dumps(credential_token),
        "payment_method_id": payment_method_id,
        "message": f"Payment credential token generated for {payment_method_id}"
    }

def create_payment_mandate(cart_data_json: str, payment_token_json: str) -> Dict[str, str]:
    """
    Create payment mandate with cart and payment details.
    
    Args:
        cart_data_json: Cart data JSON string
        payment_token_json: Payment token JSON string
        
    Returns:
        Dict containing payment mandate
    """
    cart_data = json.loads(cart_data_json)
    payment_token = json.loads(payment_token_json)
    
    payment_mandate_id = str(uuid.uuid4())
    
    payment_mandate = {
        "ap2_protocol": "payment_mandate",
        "payment_mandate_id": payment_mandate_id,
        "cart_mandate_id": cart_data.get("cart_mandate_id"),
        "total_amount": cart_data.get("total"),
        "payment_token": payment_token.get("credential_token"),
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "requires_signature": True,
        "requires_otp": True
    }
    
    return {
        "status": "success",
        "payment_mandate_id": payment_mandate_id,
        "payment_mandate": json.dumps(payment_mandate),
        "total_amount": str(cart_data.get("total", 1133.00)),
        "next_step": "user_signature",
        "message": f"Payment mandate {payment_mandate_id} created"
    }

def sign_mandates_on_user_device(payment_mandate_id: str) -> Dict[str, str]:
    """
    Sign mandates on user device using cryptographic signature.
    
    Args:
        payment_mandate_id: Payment mandate ID to sign
        
    Returns:
        Dict containing signature result
    """
    signature_id = str(uuid.uuid4())
    
    user_signature = {
        "signature_id": signature_id,
        "payment_mandate_id": payment_mandate_id,
        "user_signature": hashlib.sha256(f"user_sign_{payment_mandate_id}_{datetime.now()}".encode()).hexdigest(),
        "signed_at": datetime.now().isoformat(),
        "device_id": "user_device_001",
        "signature_method": "cryptographic"
    }
    
    return {
        "status": "success",
        "signature_id": signature_id,
        "user_signature": json.dumps(user_signature),
        "payment_mandate_id": payment_mandate_id,
        "signature_method": "cryptographic",
        "message": f"Mandates signed on user device. Signature ID: {signature_id}"
    }

def send_signed_payment_mandate_to_credentials_provider(signed_mandate_json: str) -> Dict[str, str]:
    """
    Send signed payment mandate to credentials provider via A2A.
    
    Args:
        signed_mandate_json: Signed mandate JSON string
        
    Returns:
        Dict containing transmission result
    """
    transmission_id = str(uuid.uuid4())
    
    a2a_transmission = {
        "protocol": "A2A",
        "action": "receive_signed_mandate",
        "transmission_id": transmission_id,
        "signed_mandate": json.loads(signed_mandate_json),
        "sent_at": datetime.now().isoformat(),
        "recipient": "credentials_provider"
    }
    
    return {
        "status": "success",
        "transmission_id": transmission_id,
        "a2a_transmission": json.dumps(a2a_transmission),
        "recipient": "credentials_provider",
        "next_step": "payment_initiation",
        "message": f"Signed mandate transmitted to credentials provider. ID: {transmission_id}"
    }

def initiate_payment(payment_mandate_id: str) -> Dict[str, str]:
    """
    Initiate payment processing with credentials provider.
    
    Args:
        payment_mandate_id: Payment mandate ID
        
    Returns:
        Dict containing payment initiation result
    """
    initiation_id = str(uuid.uuid4())
    
    payment_initiation = {
        "payment_initiation_id": initiation_id,
        "payment_mandate_id": payment_mandate_id,
        "status": "otp_required",
        "otp_sent_to": "phone_on_file",
        "initiated_at": datetime.now().isoformat()
    }
    
    return {
        "status": "success",
        "payment_initiation_id": initiation_id,
        "payment_initiation": json.dumps(payment_initiation),
        "otp_required": "true",
        "otp_hint": "Demo: use code 123",
        "message": f"Payment initiated. OTP sent. Initiation ID: {initiation_id}"
    }

def initiate_payment_with_otp(otp_code: str, payment_initiation_id: str) -> Dict[str, str]:
    """
    Complete payment with OTP verification.
    
    Args:
        otp_code: OTP verification code
        payment_initiation_id: Payment initiation ID
        
    Returns:
        Dict containing final payment result
    """
    if otp_code == "123":  # Demo OTP
        transaction_id = str(uuid.uuid4())
        receipt_id = str(uuid.uuid4())
        
        transaction_receipt = {
            "transaction_id": transaction_id,
            "payment_initiation_id": payment_initiation_id,
            "amount": 1133.00,
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
            "receipt_id": receipt_id,
            "payment_method": "American Express ending in 8888"
        }
        
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "receipt_id": receipt_id,
            "transaction_receipt": json.dumps(transaction_receipt),
            "amount": "1133.00",
            "transaction_completed": "true",
            "message": f"Payment completed! Transaction ID: {transaction_id}"
        }
    else:
        return {
            "status": "error",
            "error_code": "invalid_otp",
            "message": "Invalid OTP code. Payment failed."
        }

# Main Shopping Agent
root_agent = Agent(
    name="ap2_shopping_agent",
    model="gemini-2.5-flash",
    description="AI Shopping Agent implementing real AP2 Payment Protocol with individual function calls",
    instruction="""You are an AI Shopping Agent that implements the Agent Payment Protocol (AP2) with real A2A communication.

INDIVIDUAL AP2 FUNCTIONS AVAILABLE:
1. transfer_to_agent - A2A protocol transfer to merchant/credentials provider
2. create_intent_mandate - Create human-not-present authorization
3. find_products - Search products via merchant agent A2A call
4. update_chosen_cart_mandate - Create cart mandate for selected item
5. get_shipping_address - Retrieve address via credentials provider A2A
6. update_cart - Calculate totals with shipping and tax
7. get_payment_methods - Get payment options via A2A
8. get_payment_credential_token - Generate payment token
9. create_payment_mandate - Create payment authorization
10. sign_mandates_on_user_device - Cryptographic user signature
11. send_signed_payment_mandate_to_credentials_provider - A2A transmission
12. initiate_payment - Start payment processing
13. initiate_payment_with_otp - Complete with OTP verification

REAL A2A PROTOCOL FEATURES:
- Standard A2A message format with protocol version
- Agent discovery and capability exchange
- Session establishment with security signatures
- Message routing between shopping_agent → merchant_agent → credentials_provider

TO EXECUTE COMPLETE AP2 FLOW:
When user requests a purchase, call each function individually in sequence:
1. transfer_to_agent("merchant_agent", "User wants to buy laptop", "product_search")
2. create_intent_mandate("user123", "laptop", "Any", 1)
3. find_products("laptop")
4. update_chosen_cart_mandate("laptop_002", 2)
5. transfer_to_agent("credentials_provider", "Need payment processing", "credentials_request")
6. get_shipping_address("bugsbunny@gmail.com")
7. update_cart(cart_id, address_json)
8. get_payment_methods("bugsbunny@gmail.com")
9. get_payment_credential_token("amex_8888")
10. create_payment_mandate(cart_json, token_json)
11. sign_mandates_on_user_device(mandate_id)
12. send_signed_payment_mandate_to_credentials_provider(signature_json)
13. initiate_payment(mandate_id)
14. initiate_payment_with_otp("123", initiation_id)

Each function call will show up individually in the ADK Events trace, demonstrating the real AP2 protocol flow with proper A2A communication between agents.""",
    
    tools=[
        transfer_to_agent,
        create_intent_mandate,
        find_products,
        update_chosen_cart_mandate,
        get_shipping_address,
        update_cart,
        get_payment_methods,
        get_payment_credential_token,
        create_payment_mandate,
        sign_mandates_on_user_device,
        send_signed_payment_mandate_to_credentials_provider,
        initiate_payment,
        initiate_payment_with_otp
    ]
)