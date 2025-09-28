import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict
from google.adk.agents import Agent

def receive_a2a_message(message_json: str) -> Dict[str, str]:
    """
    Receive and process A2A protocol message from shopping agent.
    
    Args:
        message_json: A2A message JSON string
        
    Returns:
        Dict containing A2A response
    """
    try:
        message = json.loads(message_json)
        
        response = {
            "protocol": "A2A",
            "version": "1.0",
            "message_id": str(uuid.uuid4()),
            "sender_agent": "credentials_provider",
            "receiver_agent": message.get("sender_agent", "shopping_agent"),
            "in_response_to": message.get("message_id"),
            "timestamp": datetime.now().isoformat(),
            "status": "received",
            "capabilities": ["credential_management", "payment_processing", "address_lookup", "authentication"]
        }
        
        return {
            "status": "success",
            "a2a_response": json.dumps(response),
            "sender": message.get("sender_agent", "unknown"),
            "message": f"A2A message received from {message.get('sender_agent')}. Credentials provider ready."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"A2A message processing failed: {str(e)}"
        }

def get_user_profile(user_email: str) -> Dict[str, str]:
    """
    Retrieve user profile information.
    
    Args:
        user_email: User email address
        
    Returns:
        Dict containing user profile
    """
    # Mock user database
    user_profiles = {
        "bugsbunny@gmail.com": {
            "user_id": "user_bugs_bunny",
            "full_name": "Bugs Bunny",
            "email": "bugsbunny@gmail.com",
            "phone": "+1-000-000-0000",
            "account_created": "2020-01-15T10:30:00Z",
            "account_status": "active",
            "verification_level": "verified"
        },
        "user123@example.com": {
            "user_id": "user_123",
            "full_name": "Test User",
            "email": "user123@example.com", 
            "phone": "+1-555-0123",
            "account_created": "2021-03-20T14:15:00Z",
            "account_status": "active",
            "verification_level": "verified"
        }
    }
    
    profile = user_profiles.get(user_email, {
        "user_id": f"user_{uuid.uuid4().hex[:8]}",
        "full_name": "Unknown User",
        "email": user_email,
        "phone": "+1-000-000-0000",
        "account_created": datetime.now().isoformat(),
        "account_status": "active",
        "verification_level": "unverified"
    })
    
    return {
        "status": "success",
        "user_profile": json.dumps(profile),
        "user_email": user_email,
        "verification_level": profile["verification_level"],
        "message": f"User profile retrieved for {user_email}"
    }

def get_shipping_addresses(user_email: str) -> Dict[str, str]:
    """
    Retrieve user's shipping addresses.
    
    Args:
        user_email: User email address
        
    Returns:
        Dict containing shipping addresses
    """
    # Mock address database
    user_addresses = {
        "bugsbunny@gmail.com": [
            {
                "address_id": "addr_001",
                "recipient": "Bugs Bunny",
                "address_line_1": "123 Main St",
                "address_line_2": "Apt 4B",
                "city": "Sample City",
                "state": "ST",
                "zip_code": "00000",
                "country": "US",
                "phone": "+1-000-000-0000",
                "organization": "Sample Organization",
                "default": True,
                "address_type": "home"
            },
            {
                "address_id": "addr_002", 
                "recipient": "Bugs Bunny",
                "address_line_1": "456 Business Ave",
                "address_line_2": "Suite 100",
                "city": "Corporate City",
                "state": "ST",
                "zip_code": "11111",
                "country": "US",
                "phone": "+1-000-000-0001",
                "organization": "Acme Corporation",
                "default": False,
                "address_type": "business"
            }
        ]
    }
    
    addresses = user_addresses.get(user_email, [
        {
            "address_id": f"addr_{uuid.uuid4().hex[:8]}",
            "recipient": "User Name",
            "address_line_1": "123 Default St",
            "city": "Default City",
            "state": "ST",
            "zip_code": "00000",
            "country": "US",
            "phone": "+1-000-000-0000",
            "default": True,
            "address_type": "home"
        }
    ])
    
    default_address = next((addr for addr in addresses if addr.get("default")), addresses[0] if addresses else None)
    
    return {
        "status": "success",
        "addresses": json.dumps(addresses),
        "default_address": json.dumps(default_address) if default_address else "{}",
        "address_count": str(len(addresses)),
        "message": f"Retrieved {len(addresses)} shipping addresses for {user_email}"
    }

def get_payment_methods(user_email: str, merchant_requirements: str = "{}") -> Dict[str, str]:
    """
    Retrieve user's payment methods compatible with merchant requirements.
    
    Args:
        user_email: User email address
        merchant_requirements: JSON string of merchant payment requirements
        
    Returns:
        Dict containing compatible payment methods
    """
    # Mock payment methods database
    user_payment_methods = {
        "bugsbunny@gmail.com": [
            {
                "payment_method_id": "pm_amex_4444",
                "type": "credit_card",
                "brand": "american_express",
                "last_four": "4444",
                "exp_month": 12,
                "exp_year": 2027,
                "cardholder_name": "Bugs Bunny",
                "billing_country": "US",
                "default": False,
                "verified": True,
                "capabilities": ["purchase", "refund"]
            },
            {
                "payment_method_id": "pm_amex_8888",
                "type": "credit_card",
                "brand": "american_express", 
                "last_four": "8888",
                "exp_month": 8,
                "exp_year": 2026,
                "cardholder_name": "Bugs Bunny",
                "billing_country": "US",
                "default": True,
                "verified": True,
                "capabilities": ["purchase", "refund"]
            },
            {
                "payment_method_id": "pm_bank_001",
                "type": "bank_account",
                "bank_name": "Chase Bank",
                "account_type": "checking",
                "routing_last_four": "0001",
                "account_last_four": "1234",
                "account_holder_name": "Bugs Bunny",
                "default": False,
                "verified": True,
                "capabilities": ["purchase"]
            }
        ]
    }
    
    methods = user_payment_methods.get(user_email, [
        {
            "payment_method_id": f"pm_{uuid.uuid4().hex[:8]}",
            "type": "credit_card",
            "brand": "visa",
            "last_four": "0000",
            "exp_month": 12,
            "exp_year": 2025,
            "cardholder_name": "Default User",
            "billing_country": "US",
            "default": True,
            "verified": False,
            "capabilities": ["purchase"]
        }
    ])
    
    # Filter based on merchant requirements if provided
    try:
        requirements = json.loads(merchant_requirements) if merchant_requirements else {}
        accepted_brands = requirements.get("accepted_brands", [])
        if accepted_brands:
            methods = [m for m in methods if m.get("brand") in accepted_brands]
    except:
        pass  # Use all methods if requirements parsing fails
    
    default_method = next((m for m in methods if m.get("default")), methods[0] if methods else None)
    
    return {
        "status": "success",
        "payment_methods": json.dumps(methods),
        "default_method": json.dumps(default_method) if default_method else "{}",
        "methods_count": str(len(methods)),
        "message": f"Retrieved {len(methods)} eligible payment methods for {user_email}"
    }

def generate_payment_credential_token(payment_method_id: str, user_email: str) -> Dict[str, str]:
    """
    Generate secure payment credential token for selected method.
    
    Args:
        payment_method_id: Selected payment method ID
        user_email: User email address
        
    Returns:
        Dict containing credential token
    """
    token_id = str(uuid.uuid4())
    
    credential_token = {
        "credential_token_id": token_id,
        "credential_token": f"cred_token_{hashlib.sha256(f'{payment_method_id}:{user_email}:{datetime.now()}'.encode()).hexdigest()[:32]}",
        "payment_method_id": payment_method_id,
        "user_email": user_email,
        "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(),
        "token_type": "payment_credential",
        "generated_at": datetime.now().isoformat(),
        "scope": ["payment_authorization", "payment_capture"],
        "single_use": True
    }
    
    return {
        "status": "success",
        "token_id": token_id,
        "credential_token": json.dumps(credential_token),
        "payment_method_id": payment_method_id,
        "expires_in_minutes": "60",
        "message": f"Payment credential token generated for {payment_method_id}"
    }

def create_payment_session(payment_mandate_json: str) -> Dict[str, str]:
    """
    Create secure payment session for processing.
    
    Args:
        payment_mandate_json: Payment mandate JSON string
        
    Returns:
        Dict containing payment session
    """
    try:
        payment_mandate = json.loads(payment_mandate_json)
        session_id = str(uuid.uuid4())
        
        payment_session = {
            "payment_session_id": session_id,
            "payment_mandate_id": payment_mandate.get("payment_mandate_id"),
            "amount": payment_mandate.get("total_amount"),
            "currency": "USD",
            "status": "created",
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(minutes=30)).isoformat(),
            "security_level": "high",
            "requires_otp": True,
            "requires_3ds": False
        }
        
        return {
            "status": "success",
            "session_id": session_id,
            "payment_session": json.dumps(payment_session),
            "amount": str(payment_mandate.get("total_amount", 0)),
            "requires_otp": "true",
            "message": f"Payment session {session_id} created"
        }
    except Exception as e:
        return {"status": "error", "message": f"Payment session creation failed: {str(e)}"}

def authorize_payment(payment_session_json: str, otp_required: str = "true") -> Dict[str, str]:
    """
    Authorize payment for the session.
    
    Args:
        payment_session_json: Payment session JSON string
        otp_required: Whether OTP is required
        
    Returns:
        Dict containing authorization result
    """
    try:
        payment_session = json.loads(payment_session_json)
        authorization_id = str(uuid.uuid4())
        
        authorization = {
            "authorization_id": authorization_id,
            "payment_session_id": payment_session.get("payment_session_id"),
            "amount": payment_session.get("amount"),
            "currency": payment_session.get("currency", "USD"),
            "status": "pending_otp" if otp_required == "true" else "authorized",
            "authorization_code": f"AUTH{uuid.uuid4().hex[:8].upper()}",
            "authorized_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            "risk_score": 15,  # Low risk score
            "network_transaction_id": f"ntxn_{uuid.uuid4()}",
            "processor_response": "APPROVED"
        }
        
        if otp_required == "true":
            authorization["otp_sent_to"] = "phone_on_file"
            authorization["otp_expires_at"] = (datetime.now() + timedelta(minutes=5)).isoformat()
        
        return {
            "status": "success",
            "authorization_id": authorization_id,
            "authorization": json.dumps(authorization),
            "authorization_code": authorization["authorization_code"],
            "otp_required": otp_required,
            "otp_hint": "Demo: use code 123" if otp_required == "true" else "",
            "message": f"Payment authorized. {'OTP verification required.' if otp_required == 'true' else 'Ready for capture.'}"
        }
    except Exception as e:
        return {"status": "error", "message": f"Payment authorization failed: {str(e)}"}

def verify_otp_and_capture_payment(authorization_id: str, otp_code: str) -> Dict[str, str]:
    """
    Verify OTP and capture payment.
    
    Args:
        authorization_id: Authorization ID
        otp_code: OTP verification code
        
    Returns:
        Dict containing final payment result
    """
    if otp_code == "123":  # Demo OTP code
        transaction_id = str(uuid.uuid4())
        receipt_id = str(uuid.uuid4())
        
        capture_result = {
            "transaction_id": transaction_id,
            "authorization_id": authorization_id,
            "capture_id": f"cap_{uuid.uuid4()}",
            "amount": 1133.00,
            "currency": "USD",
            "status": "completed",
            "captured_at": datetime.now().isoformat(),
            "settlement_date": (datetime.now() + timedelta(days=2)).date().isoformat(),
            "receipt_id": receipt_id,
            "receipt_url": f"https://receipts.credprovider.com/{receipt_id}",
            "processor_response": "CAPTURED",
            "network_response": "APPROVED"
        }
        
        return {
            "status": "success",
            "transaction_id": transaction_id,
            "receipt_id": receipt_id,
            "capture_result": json.dumps(capture_result),
            "amount": "1133.00",
            "settlement_date": capture_result["settlement_date"],
            "transaction_completed": "true",
            "message": f"Payment completed successfully! Transaction ID: {transaction_id}"
        }
    else:
        return {
            "status": "error",
            "error_code": "invalid_otp",
            "retry_allowed": "true",
            "message": "Invalid OTP code. Please try again."
        }

def process_refund(transaction_id: str, refund_amount: str, reason: str = "customer_request") -> Dict[str, str]:
    """
    Process refund for completed transaction.
    
    Args:
        transaction_id: Original transaction ID
        refund_amount: Amount to refund
        reason: Refund reason
        
    Returns:
        Dict containing refund result
    """
    refund_id = str(uuid.uuid4())
    
    refund_result = {
        "refund_id": refund_id,
        "original_transaction_id": transaction_id,
        "refund_amount": float(refund_amount),
        "currency": "USD",
        "reason": reason,
        "status": "processed",
        "processed_at": datetime.now().isoformat(),
        "expected_completion": (datetime.now() + timedelta(days=3)).date().isoformat(),
        "refund_method": "original_payment_method"
    }
    
    return {
        "status": "success",
        "refund_id": refund_id,
        "refund_result": json.dumps(refund_result),
        "refund_amount": refund_amount,
        "expected_completion": refund_result["expected_completion"],
        "message": f"Refund processed. Amount: ${refund_amount}. Refund ID: {refund_id}"
    }

def get_transaction_history(user_email: str, limit: int = 10) -> Dict[str, str]:
    """
    Retrieve user's transaction history.
    
    Args:
        user_email: User email address
        limit: Maximum number of transactions to return
        
    Returns:
        Dict containing transaction history
    """
    # Mock transaction history
    transactions = [
        {
            "transaction_id": f"txn_{uuid.uuid4()}",
            "amount": 1133.00,
            "currency": "USD", 
            "merchant": "Tech Store",
            "description": "Mid-range business laptop",
            "status": "completed",
            "date": (datetime.now() - timedelta(days=1)).isoformat(),
            "payment_method": "American Express ending in 8888"
        },
        {
            "transaction_id": f"txn_{uuid.uuid4()}",
            "amount": 299.99,
            "currency": "USD",
            "merchant": "Electronics Plus",
            "description": "Wireless headphones",
            "status": "completed", 
            "date": (datetime.now() - timedelta(days=5)).isoformat(),
            "payment_method": "American Express ending in 4444"
        }
    ]
    
    return {
        "status": "success",
        "transactions": json.dumps(transactions[:limit]),
        "transaction_count": str(len(transactions)),
        "user_email": user_email,
        "message": f"Retrieved {min(len(transactions), limit)} transactions for {user_email}"
    }

# Main Credentials Provider Agent
root_agent = Agent(
    name="ap2_credentials_provider",
    model="gemini-2.5-flash",
    description="AI Credentials Provider Agent for secure payment processing in AP2 protocol ecosystem",
    instruction="""You are an AI Credentials Provider Agent responsible for secure payment processing within the AP2 (Agent Payment Protocol) ecosystem.

CORE RESPONSIBILITIES:
1. Process A2A protocol messages from shopping agents
2. Manage user payment credentials securely (PCI DSS compliant simulation)
3. Provide user shipping addresses and profile information
4. Generate secure payment credential tokens
5. Process payment authorization and capture flows
6. Handle OTP verification for secure payments
7. Maintain complete audit trails for compliance

AP2 PROTOCOL REQUIREMENTS:
- Process A2A messages from shopping agents for credential and payment requests
- Generate cryptographically secure payment credential tokens
- Implement proper authorization → OTP verification → capture payment flow
- Maintain transaction logs for dispute resolution and compliance
- Handle sensitive payment data according to security standards (simulated)

PAYMENT PROCESSING FLOW:
1. Receive payment session creation request via A2A
2. Validate user credentials and payment methods
3. Generate secure payment credential tokens
4. Create payment session with security requirements
5. Authorize payment with risk assessment
6. Send OTP to user's verified phone number
7. Verify OTP and capture payment
8. Generate transaction receipt and audit trail

SECURITY FEATURES:
- Multi-layer verification (credentials → authorization → OTP → capture)
- Risk scoring and fraud detection simulation
- Secure tokenization of payment methods
- Complete cryptographic audit trail
- PCI DSS compliant data handling simulation
- A2A protocol message encryption and validation

USER CREDENTIAL MANAGEMENT:
- Secure storage of payment methods (credit cards, bank accounts)
- Address book management with default preferences
- User profile and verification status tracking
- Transaction history and receipt management
- Refund processing capabilities

SUPPORTED PAYMENT METHODS:
- Credit cards (American Express, Visa, Mastercard)
- Bank transfers and ACH payments
- Digital wallets and stored credentials
- Subscription and recurring payment management

You serve as the critical trust anchor in the AP2 ecosystem, ensuring all payment transactions are secure, verifiable, and compliant with financial regulations while maintaining excellent user experience.""",
    
    tools=[
        receive_a2a_message,
        get_user_profile,
        get_shipping_addresses,
        get_payment_methods,
        generate_payment_credential_token,
        create_payment_session,
        authorize_payment,
        verify_otp_and_capture_payment,
        process_refund,
        get_transaction_history
    ]
)