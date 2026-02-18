# Workshop - Customer Management API

A Flask-based customer management system with bulk CSV import functionality and KYC (Know Your Customer) tracking.

## Features

- **Customer CRUD Operations**: Create, read, update, and delete customer records
- **Bulk CSV Import**: Import multiple customers from CSV files with validation
- **Email Validation**: Automatic email format validation
- **Country Code Validation**: ISO 3166-1 alpha-2 country code validation
- **Audit Logging**: All customer data mutations are logged with timestamps
- **KYC Status Tracking**: Automatic KYC status initialization to "Pending"
- **File Size Limits**: Maximum 5MB file uploads
- **Batch Size Limits**: Maximum 500 rows per CSV import

## Requirements

- Python 3.8+
- Flask 3.0.0
- SQLAlchemy
- See `requirements.txt` for full list

## Installation

1. Clone the repository:
```bash
git clone https://github.com/EmmaSleghel-visma/Workshop.git
cd Workshop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`.

## API Endpoints

### Create Single Customer
**POST** `/api/customers`

Create a new customer.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "country": "US"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "country": "US",
  "kyc_status": "Pending",
  "created_at": "2026-02-18T09:00:00+00:00",
  "updated_at": "2026-02-18T09:00:00+00:00"
}
```

### List Customers
**GET** `/api/customers`

Get all customers.

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "country": "US",
    "kyc_status": "Pending",
    "created_at": "2026-02-18T09:00:00+00:00",
    "updated_at": "2026-02-18T09:00:00+00:00"
  }
]
```

### Get Single Customer
**GET** `/api/customers/<id>`

Get a specific customer by ID.

**Response:** `200 OK`

### Update Customer
**PUT** `/api/customers/<id>`

Update customer information.

**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "country": "GB",
  "kyc_status": "Approved"
}
```

**Response:** `200 OK`

### Delete Customer
**DELETE** `/api/customers/<id>`

Delete a customer.

**Response:** `204 No Content`

### Bulk Import Customers
**POST** `/api/customers/bulk-import`

Import multiple customers from a CSV file.

**Request:**
- Content-Type: `multipart/form-data`
- Field name: `file`
- File type: CSV

**CSV Format:**
```csv
name,email,country
John Doe,john.doe@example.com,US
Jane Smith,jane.smith@example.com,GB
Bob Johnson,bob.johnson@example.com,CA
```

**Response:** `200 OK`
```json
{
  "total_rows": 3,
  "successful_imports": 3,
  "failed_rows": []
}
```

**Failed Row Example:**
```json
{
  "total_rows": 5,
  "successful_imports": 2,
  "failed_rows": [
    {
      "line": 3,
      "data": {"name": "", "email": "test@example.com", "country": "US"},
      "reason": "Missing required field: name"
    },
    {
      "line": 4,
      "data": {"name": "Test", "email": "invalid-email", "country": "US"},
      "reason": "Invalid email format"
    },
    {
      "line": 5,
      "data": {"name": "Test", "email": "test2@example.com", "country": "XX"},
      "reason": "Invalid country code (must be ISO 3166-1 alpha-2)"
    }
  ]
}
```

## Validation Rules

### Required Fields
- `name`: Customer's full name (cannot be empty)
- `email`: Valid email address
- `country`: ISO 3166-1 alpha-2 country code (e.g., US, GB, DE, FR, CA)

### Email Validation
- Must be a valid email format
- Must be unique across all customers

### Country Code Validation
- Must be a valid ISO 3166-1 alpha-2 code
- Examples: US, GB, DE, FR, CA, JP, AU, etc.

### File Constraints
- **Maximum file size**: 5MB
- **Maximum rows**: 500 per batch
- **File format**: CSV with UTF-8 encoding
- **Required columns**: name, email, country

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run specific test classes:
```bash
pytest tests/test_customer_api.py::TestBulkImport -v
```

## Demo

A demo script is provided to test the API:
```bash
# Start the server in one terminal
python app.py

# In another terminal, run the demo
python demo.py
```

## Security Features

- **Debug mode disabled in production**: Controlled via `FLASK_DEBUG` environment variable
- **Audit logging**: All customer mutations (CREATE, UPDATE, DELETE) are logged
- **Input validation**: All inputs are validated before processing
- **SQL injection prevention**: Using SQLAlchemy ORM with parameterized queries
- **File size limits**: Prevents denial-of-service via large file uploads

## Architecture

```
Workshop/
├── app.py                    # Main Flask application
├── customer.py               # Customer model and database schema
├── audit_logger.py           # Audit logging functionality
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── tests/
│   ├── fixtures/            # Test CSV files
│   │   ├── valid_customers.csv
│   │   ├── invalid_customers.csv
│   │   └── duplicate_email.csv
│   └── test_customer_api.py # Integration tests
└── demo.py                  # Demo script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.