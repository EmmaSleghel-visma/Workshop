from flask import Flask, request, jsonify
from customer import Customer, CustomerStore
from audit_logger import AuditLogger

app = Flask(__name__)

# Initialize storage and audit logger
customer_store = CustomerStore()
audit_logger = AuditLogger()


def get_current_user() -> str:
    """
    Get the current user from request headers.
    In a real application, this would extract user from authentication token.
    """
    return request.headers.get('X-User-Id', 'anonymous')


@app.route('/customers', methods=['GET'])
def list_customers():
    """List all customers (no audit logging needed for read operations)."""
    customers = customer_store.list_all()
    return jsonify({
        "customers": customers,
        "count": len(customers)
    }), 200


@app.route('/customers', methods=['POST'])
def create_customer():
    """
    Create a new customer with KYC audit logging.
    All customer data mutations are logged for compliance.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Validate required fields
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Create customer
    customer = Customer(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        date_of_birth=data.get('date_of_birth', ''),
        national_id=data.get('national_id', '')
    )
    
    customer_store.create(customer)
    
    # Log the customer creation for KYC audit
    user = get_current_user()
    audit_logger.log_mutation(
        action="CREATE",
        entity_type="customer",
        entity_id=customer.customer_id,
        user=user,
        data_before=None,
        data_after=customer.to_dict(),
        metadata={
            "ip_address": request.remote_addr,
            "user_agent": request.headers.get('User-Agent', 'unknown')
        }
    )
    
    return jsonify({
        "message": "Customer created successfully",
        "customer": customer.to_dict()
    }), 201


@app.route('/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a customer by ID (no audit logging needed for read operations)."""
    customer = customer_store.get(customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    return jsonify({"customer": customer.to_dict()}), 200


@app.route('/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """
    Update a customer with KYC audit logging.
    Logs both the before and after state for compliance.
    """
    customer = customer_store.get(customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Capture state before update
    data_before = customer.to_dict()
    
    # Update customer
    update_fields = {}
    allowed_fields = ['name', 'email', 'phone', 'address', 'date_of_birth', 'national_id']
    for field in allowed_fields:
        if field in data:
            update_fields[field] = data[field]
    
    customer_store.update(customer_id, **update_fields)
    
    # Capture state after update
    data_after = customer.to_dict()
    
    # Log the customer update for KYC audit
    user = get_current_user()
    audit_logger.log_mutation(
        action="UPDATE",
        entity_type="customer",
        entity_id=customer_id,
        user=user,
        data_before=data_before,
        data_after=data_after,
        metadata={
            "ip_address": request.remote_addr,
            "user_agent": request.headers.get('User-Agent', 'unknown'),
            "fields_updated": list(update_fields.keys())
        }
    )
    
    return jsonify({
        "message": "Customer updated successfully",
        "customer": customer.to_dict()
    }), 200


@app.route('/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """
    Delete a customer with KYC audit logging.
    Logs the deleted customer data for compliance.
    """
    customer = customer_store.get(customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    # Capture state before deletion
    data_before = customer.to_dict()
    
    # Delete customer
    customer_store.delete(customer_id)
    
    # Log the customer deletion for KYC audit
    user = get_current_user()
    audit_logger.log_mutation(
        action="DELETE",
        entity_type="customer",
        entity_id=customer_id,
        user=user,
        data_before=data_before,
        data_after=None,
        metadata={
            "ip_address": request.remote_addr,
            "user_agent": request.headers.get('User-Agent', 'unknown')
        }
    )
    
    return jsonify({
        "message": "Customer deleted successfully"
    }), 200


@app.route('/audit-logs', methods=['GET'])
def get_audit_logs():
    """
    Retrieve KYC audit logs with optional filtering.
    Supports filtering by entity_type, entity_id, action, and user.
    """
    entity_type = request.args.get('entity_type')
    entity_id = request.args.get('entity_id')
    action = request.args.get('action')
    user = request.args.get('user')
    
    logs = audit_logger.get_logs(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        user=user
    )
    
    return jsonify({
        "logs": logs,
        "count": len(logs)
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
