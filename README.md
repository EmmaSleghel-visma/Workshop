# Workshop - KYC Audit Logging System

A demonstration application that implements comprehensive KYC (Know Your Customer) audit logging for all customer data mutations. This system ensures compliance by tracking all changes to customer data with complete audit trails.

## Features

- **Complete Audit Trail**: All customer data mutations (CREATE, UPDATE, DELETE) are automatically logged
- **Detailed Logging**: Captures before/after states, user information, timestamps, and metadata
- **Compliance Ready**: Structured audit logs suitable for regulatory compliance and forensic analysis
- **Filtering Support**: Query audit logs by entity type, entity ID, action type, or user
- **RESTful API**: Clean REST API for customer management and audit log retrieval

## Installation

1. Clone the repository:
```bash
git clone https://github.com/EmmaSleghel-visma/Workshop.git
cd Workshop
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

**Security Note**: By default, the application runs with debug mode disabled for security. To enable debug mode in development only, set the environment variable:
```bash
export FLASK_DEBUG=true
python app.py
```

Never enable debug mode in production environments.

## API Endpoints

### Customer Management

#### Create Customer
```bash
POST /customers
Content-Type: application/json
X-User-Id: user@example.com

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "address": "123 Main St",
  "date_of_birth": "1990-01-01",
  "national_id": "ABC123456"
}
```

#### Get Customer
```bash
GET /customers/{customer_id}
```

#### Update Customer
```bash
PUT /customers/{customer_id}
Content-Type: application/json
X-User-Id: user@example.com

{
  "name": "Jane Doe",
  "phone": "+9876543210"
}
```

#### Delete Customer
```bash
DELETE /customers/{customer_id}
X-User-Id: user@example.com
```

#### List All Customers
```bash
GET /customers
```

### Audit Logs

#### Get All Audit Logs
```bash
GET /audit-logs
```

#### Get Filtered Audit Logs
```bash
# Filter by user
GET /audit-logs?user=user@example.com

# Filter by entity ID
GET /audit-logs?entity_id=123e4567-e89b-12d3-a456-426614174000

# Filter by action type
GET /audit-logs?action=CREATE

# Filter by entity type
GET /audit-logs?entity_type=customer

# Combine filters
GET /audit-logs?action=UPDATE&user=admin@example.com
```

## Audit Log Format

Each audit log entry contains:

```json
{
  "timestamp": "2026-02-17T23:01:00.000Z",
  "action": "UPDATE",
  "entity_type": "customer",
  "entity_id": "123e4567-e89b-12d3-a456-426614174000",
  "user": "user@example.com",
  "data_before": {
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890"
  },
  "data_after": {
    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Jane Doe",
    "email": "john.doe@example.com",
    "phone": "+9876543210"
  },
  "metadata": {
    "ip_address": "127.0.0.1",
    "user_agent": "curl/7.68.0",
    "fields_updated": ["name", "phone"]
  }
}
```

### Audit Log Fields

- **timestamp**: ISO 8601 UTC timestamp of the mutation
- **action**: Type of mutation (CREATE, UPDATE, DELETE)
- **entity_type**: Type of entity being mutated (e.g., "customer")
- **entity_id**: Unique identifier of the entity
- **user**: User who performed the action (from X-User-Id header)
- **data_before**: State of the data before mutation (null for CREATE)
- **data_after**: State of the data after mutation (null for DELETE)
- **metadata**: Additional context including IP address, user agent, and fields updated

## Testing

Run the test suite:
```bash
python -m unittest test_app.py
```

The test suite includes:
- Customer creation with audit logging
- Customer updates with before/after state logging
- Customer deletion with audit logging
- Audit log filtering functionality
- Verification that read operations are not logged
- Metadata inclusion in audit logs

## Example Usage

### Complete Customer Lifecycle with Audit Logging

```bash
# 1. Create a customer
curl -X POST http://localhost:5000/customers \
  -H "Content-Type: application/json" \
  -H "X-User-Id: admin@example.com" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "+1234567890",
    "address": "456 Oak Ave",
    "date_of_birth": "1985-05-15",
    "national_id": "XYZ789012"
  }'

# Response includes customer_id: "abc-123-def-456"

# 2. Update the customer
curl -X PUT http://localhost:5000/customers/abc-123-def-456 \
  -H "Content-Type: application/json" \
  -H "X-User-Id: admin@example.com" \
  -d '{
    "phone": "+9876543210",
    "address": "789 Pine St"
  }'

# 3. View audit logs for this customer
curl http://localhost:5000/audit-logs?entity_id=abc-123-def-456

# 4. Delete the customer
curl -X DELETE http://localhost:5000/customers/abc-123-def-456 \
  -H "X-User-Id: admin@example.com"

# 5. View all audit logs for admin user
curl http://localhost:5000/audit-logs?user=admin@example.com
```

## Architecture

### Components

1. **app.py**: Flask application with REST API endpoints
2. **customer.py**: Customer data model and in-memory storage
3. **audit_logger.py**: KYC audit logging implementation
4. **test_app.py**: Comprehensive test suite

### Audit Logging Flow

```
API Request → Endpoint Handler → Business Logic
                                      ↓
                                Capture Data Before (UPDATE/DELETE)
                                      ↓
                                Perform Mutation
                                      ↓
                                Capture Data After (CREATE/UPDATE)
                                      ↓
                                AuditLogger.log_mutation()
                                      ↓
                                Write to audit_logs.json
                                      ↓
                                Return Response
```

## Security Considerations

- **User Identification**: Users are identified via the `X-User-Id` header. In production, integrate with your authentication system.
- **Audit Log Immutability**: In production, audit logs should be write-only and stored in a tamper-proof system.
- **Data Retention**: Implement appropriate data retention policies for compliance.
- **Access Control**: Restrict access to audit logs to authorized personnel only.

## Compliance

This implementation provides:
- Complete audit trail for all customer data mutations
- Timestamp precision for forensic analysis
- Before/after state tracking for data integrity verification
- User attribution for accountability
- Metadata capture for context and traceability

## Future Enhancements

- Database persistence (PostgreSQL, MongoDB)
- Audit log encryption
- Automated compliance reporting
- Real-time audit log streaming
- Integration with SIEM systems
- Role-based access control
- Audit log retention policies

## License

This is a workshop/demonstration project.