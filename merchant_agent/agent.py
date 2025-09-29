# merchant_agent/agent.py
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict
from google.adk.agents import Agent

def receive_a2a_message(message_json: str) -> Dict[str, str]:
    """
    Receive and process A2A protocol message from shopping agent using A2A SDK.
    
    Args:
        message_json: A2A message JSON string
        
    Returns:
        Dict containing A2A response
    """
    try:
        from a2a.types import Message, TextPart, Role
        
        # Parse incoming A2A message using SDK
        incoming_message = Message.model_validate_json(message_json)
        
        # Create response using A2A SDK types
        response_message = Message(
            role=Role.agent,
            parts=[TextPart(text="Merchant agent ready to process your request")],
            message_id=str(uuid.uuid4()),
            metadata={
                "sender_agent": "merchant_agent",
                "receiver_agent": incoming_message.metadata.get("sender_agent", "shopping_agent"),
                "in_response_to": incoming_message.message_id,
                "capabilities": ["product_search", "inventory_management", "cart_signing"],
                "status": "received"
            }
        )
        
        return {
            "status": "success",
            "a2a_response": response_message.model_dump_json(),
            "sender": incoming_message.metadata.get("sender_agent", "unknown"),
            "message": f"A2A message received using SDK from {incoming_message.metadata.get('sender_agent')}. Merchant agent ready."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"A2A message processing failed: {str(e)}",
            "fallback": "Using local processing"
        }

def get_product_catalog(category: str = "", query: str = "", max_results: int = 10) -> Dict[str, str]:
    """
    Get product catalog with optional filtering.
    
    Args:
        category: Product category filter
        query: Search query
        max_results: Maximum results to return
        
    Returns:
        Dict containing product catalog
    """
    catalog = [
        {
            "id": "laptop_001",
            "name": "High-performance laptop",
            "price": 1599.99,
            "category": "electronics",
            "description": "Latest generation processor, 32GB RAM, 1TB SSD",
            "stock": 15,
            "merchant": "Tech Store",
            "expires": (datetime.now() + timedelta(days=1)).isoformat(),
            "refund_period": 30
        },
        {
            "id": "laptop_002", 
            "name": "Mid-range business laptop",
            "price": 1129.50,
            "category": "electronics",
            "description": "Perfect for business and productivity tasks",
            "stock": 25,
            "merchant": "Tech Store",
            "expires": (datetime.now() + timedelta(days=1)).isoformat(),
            "refund_period": 30
        },
        {
            "id": "laptop_003",
            "name": "Entry-level student laptop", 
            "price": 789.00,
            "category": "electronics",
            "description": "Affordable option for students and basic tasks",
            "stock": 40,
            "merchant": "Generic Merchant",
            "expires": (datetime.now() + timedelta(days=1)).isoformat(),
            "refund_period": 14
        },
        {
            "id": "phone_001",
            "name": "Flagship smartphone",
            "price": 999.99,
            "category": "electronics", 
            "description": "Latest smartphone with advanced camera",
            "stock": 30,
            "merchant": "Tech Store",
            "expires": (datetime.now() + timedelta(days=1)).isoformat(),
            "refund_period": 30
        },
        {
            "id": "tablet_001",
            "name": "Professional tablet",
            "price": 649.99,
            "category": "electronics",
            "description": "High-resolution display, stylus included",
            "stock": 20,
            "merchant": "Tech Store", 
            "expires": (datetime.now() + timedelta(days=1)).isoformat(),
            "refund_period": 30
        }
    ]
    
    filtered_catalog = catalog
    
    # Filter by category
    if category and category.strip():
        filtered_catalog = [p for p in filtered_catalog if p["category"].lower() == category.lower()]
    
    # Filter by query
    if query and query.strip():
        query_lower = query.lower()
        filtered_catalog = [p for p in filtered_catalog 
                          if query_lower in p["name"].lower() or query_lower in p["description"].lower()]
    
    return {
        "status": "success",
        "total_products": str(len(catalog)),
        "filtered_count": str(len(filtered_catalog)),
        "products": json.dumps(filtered_catalog[:max_results]),
        "message": f"Product catalog retrieved. {len(filtered_catalog)} products match criteria."
    }

def validate_cart_items(cart_items_json: str) -> Dict[str, str]:
    """
    Validate cart items against inventory and pricing.
    
    Args:
        cart_items_json: JSON string of cart items
        
    Returns:
        Dict containing validation results
    """
    try:
        cart_items = json.loads(cart_items_json)
        catalog_result = get_product_catalog()
        catalog = {p["id"]: p for p in json.loads(catalog_result["products"])}
        
        validation_results = []
        total_amount = 0
        all_valid = True
        
        for item in cart_items:
            item_id = item.get("id")
            quantity = item.get("quantity", 1)
            
            if item_id not in catalog:
                validation_results.append({
                    "item_id": item_id,
                    "status": "error",
                    "message": "Product not found in catalog"
                })
                all_valid = False
                continue
            
            product = catalog[item_id]
            
            if quantity > product["stock"]:
                validation_results.append({
                    "item_id": item_id,
                    "status": "error", 
                    "message": f"Insufficient stock. Available: {product['stock']}, Requested: {quantity}"
                })
                all_valid = False
                continue
            
            line_total = product["price"] * quantity
            validation_results.append({
                "item_id": item_id,
                "status": "valid",
                "product_name": product["name"],
                "unit_price": product["price"],
                "quantity": quantity,
                "line_total": line_total
            })
            
            total_amount += line_total
        
        return {
            "status": "success",
            "cart_valid": "true" if all_valid else "false",
            "total_amount": str(total_amount),
            "validation_results": json.dumps(validation_results),
            "message": f"Cart validation {'passed' if all_valid else 'failed'}"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Cart validation failed: {str(e)}"}

def sign_cart_mandate(cart_mandate_json: str, merchant_id: str = "tech_store_merchant") -> Dict[str, str]:
    """
    Sign cart mandate as merchant fulfillment guarantee.
    
    Args:
        cart_mandate_json: Cart mandate JSON string
        merchant_id: Merchant identifier
        
    Returns:
        Dict containing signed cart mandate
    """
    try:
        cart_mandate = json.loads(cart_mandate_json)
        
        # Extract cart items for validation
        cart_items = cart_mandate.get("cart_items", [])
        if cart_items:
            validation = validate_cart_items(json.dumps(cart_items))
            if validation.get("cart_valid") != "true":
                return {
                    "status": "error",
                    "message": "Cannot sign invalid cart mandate",
                    "validation_errors": validation.get("validation_results", "[]")
                }
        
        mandate_id = cart_mandate.get("cart_mandate_id")
        total_amount = cart_mandate.get("total_amount", 0)
        
        # Generate merchant signature
        signature_data = f"{merchant_id}:{total_amount}:{mandate_id}:{datetime.now().date().isoformat()}"
        merchant_signature = hashlib.sha256(signature_data.encode()).hexdigest()
        
        # Add merchant signature to cart mandate
        cart_mandate["merchant_signature"] = merchant_signature
        cart_mandate["merchant_id"] = merchant_id
        cart_mandate["merchant_signed_at"] = datetime.now().isoformat()
        cart_mandate["fulfillment_guarantee"] = True
        cart_mandate["merchant_terms"] = {
            "fulfillment_sla": "2-3 business days",
            "return_policy": "30 days",
            "warranty": "1 year manufacturer warranty"
        }
        
        return {
            "status": "success",
            "signed_cart_mandate": json.dumps(cart_mandate),
            "merchant_signature": merchant_signature,
            "merchant_id": merchant_id,
            "fulfillment_guaranteed": "true",
            "message": f"Cart mandate signed by {merchant_id}. Fulfillment guaranteed."
        }
    except Exception as e:
        return {"status": "error", "message": f"Cart mandate signing failed: {str(e)}"}

def reserve_inventory(cart_mandate_json: str, reservation_hours: int = 24) -> Dict[str, str]:
    """
    Reserve inventory for cart items.
    
    Args:
        cart_mandate_json: Cart mandate JSON string
        reservation_hours: Hours to hold reservation
        
    Returns:
        Dict containing reservation details
    """
    try:
        cart_mandate = json.loads(cart_mandate_json)
        cart_items = cart_mandate.get("cart_items", [])
        
        reservations = []
        reservation_id = str(uuid.uuid4())
        
        for item in cart_items:
            item_reservation = {
                "item_id": item.get("id"),
                "product_name": item.get("name"),
                "quantity_reserved": item.get("quantity", 1),
                "reservation_id": f"res_{uuid.uuid4()}",
                "expires_at": (datetime.now() + timedelta(hours=reservation_hours)).isoformat()
            }
            reservations.append(item_reservation)
        
        return {
            "status": "success",
            "reservation_id": reservation_id,
            "item_reservations": json.dumps(reservations),
            "expires_in_hours": str(reservation_hours),
            "items_reserved": str(len(cart_items)),
            "message": f"Inventory reserved for {len(cart_items)} items. Expires in {reservation_hours} hours."
        }
    except Exception as e:
        return {"status": "error", "message": f"Inventory reservation failed: {str(e)}"}

def process_order_fulfillment(signed_cart_mandate_json: str) -> Dict[str, str]:
    """
    Process order fulfillment after payment completion.
    
    Args:
        signed_cart_mandate_json: Signed cart mandate JSON string
        
    Returns:
        Dict containing fulfillment details
    """
    try:
        cart_mandate = json.loads(signed_cart_mandate_json)
        
        # Verify merchant signature
        if not cart_mandate.get("merchant_signature"):
            return {"status": "error", "message": "Cart mandate not signed by merchant"}
        
        fulfillment_id = str(uuid.uuid4())
        
        fulfillment_order = {
            "fulfillment_id": fulfillment_id,
            "cart_mandate_id": cart_mandate.get("cart_mandate_id"),
            "merchant_id": cart_mandate.get("merchant_id"),
            "status": "processing",
            "created_at": datetime.now().isoformat(),
            "estimated_shipping": (datetime.now() + timedelta(days=2)).isoformat(),
            "tracking_number": f"TRACK{uuid.uuid4().hex[:8].upper()}",
            "shipping_method": "standard_shipping"
        }
        
        return {
            "status": "success",
            "fulfillment_id": fulfillment_id,
            "fulfillment_order": json.dumps(fulfillment_order),
            "tracking_number": fulfillment_order["tracking_number"],
            "estimated_delivery": fulfillment_order["estimated_shipping"],
            "message": f"Order fulfillment initiated. Tracking: {fulfillment_order['tracking_number']}"
        }
    except Exception as e:
        return {"status": "error", "message": f"Order fulfillment failed: {str(e)}"}

# Main Merchant Agent
root_agent = Agent(
    name="ap2_merchant_agent",
    model="gemini-2.5-flash",
    description="AI Merchant Agent for AP2 protocol - handles product catalog, inventory, and cart mandate signing",
    instruction="""You are an AI Merchant Agent that participates in the AP2 (Agent Payment Protocol) ecosystem.

CORE RESPONSIBILITIES:
1. Process A2A protocol messages from shopping agents
2. Provide product catalog with real-time inventory and pricing
3. Validate cart contents against available inventory
4. Sign cart mandates to provide fulfillment guarantees
5. Reserve inventory during purchase process
6. Process order fulfillment after payment completion

AP2 PROTOCOL COMPLIANCE:
- Receive A2A messages from shopping agents requesting product information
- Validate all cart items against current inventory and pricing
- Generate cryptographic signatures for cart mandates as fulfillment guarantees
- Maintain complete audit trail of all signed mandates
- Reserve inventory to prevent overselling during checkout process

PRODUCT CATALOG:
- Electronics: Laptops, smartphones, tablets with competitive pricing
- Real-time inventory tracking with stock levels
- Product descriptions, specifications, and merchant terms
- Dynamic pricing with expiration dates
- Return policies and warranty information

MERCHANT GUARANTEE PROCESS:
1. Validate cart items against inventory
2. Verify pricing and availability
3. Generate cryptographic merchant signature
4. Provide fulfillment guarantee with SLA commitments
5. Reserve inventory for confirmed purchases
6. Process order fulfillment with tracking information

SECURITY FEATURES:
- Cryptographic signatures for all cart mandates
- Inventory validation before signing
- Secure A2A message processing
- Complete transaction audit trail
- Fraud prevention through validation checks

You guarantee fulfillment of all properly signed cart mandates and maintain high standards for inventory accuracy and customer service.""",
    
    tools=[
        receive_a2a_message,
        get_product_catalog,
        validate_cart_items,
        sign_cart_mandate,
        reserve_inventory,
        process_order_fulfillment
    ]
)
