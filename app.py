"""Flask application for customer management with KYC."""
import os
import csv
import io
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from werkzeug.exceptions import RequestEntityTooLarge
from email_validator import validate_email, EmailNotValidError
import pycountry

from customer import db, Customer
from audit_logger import audit_logger

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///customers.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


def validate_country_code(country_code: str) -> bool:
    """Validate ISO 3166-1 alpha-2 country code."""
    try:
        return pycountry.countries.get(alpha_2=country_code.upper()) is not None
    except (AttributeError, KeyError):
        return False


def validate_email_format(email: str) -> bool:
    """Validate email format."""
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Create a single customer."""
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name')
    email = data.get('email')
    country = data.get('country')
    
    if not all([name, email, country]):
        return jsonify({'error': 'Missing required fields: name, email, country'}), 400
    
    # Validate email format
    if not validate_email_format(email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate country code
    if not validate_country_code(country):
        return jsonify({'error': 'Invalid country code (must be ISO 3166-1 alpha-2)'}), 400
    
    # Check if email already exists
    existing_customer = Customer.query.filter_by(email=email).first()
    if existing_customer:
        return jsonify({'error': 'Customer with this email already exists'}), 409
    
    # Create customer
    customer = Customer(
        name=name,
        email=email,
        country=country.upper(),
        kyc_status='Pending'
    )
    
    db.session.add(customer)
    db.session.commit()
    
    # Log the creation
    audit_logger.log_event(
        action='CREATE',
        user='system',
        customer_id=customer.id,
        before_state=None,
        after_state=customer.to_dict(),
        metadata={'source': 'api'}
    )
    
    return jsonify(customer.to_dict()), 201


@app.route('/api/customers', methods=['GET'])
def list_customers():
    """List all customers."""
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200


@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a single customer by ID."""
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_dict()), 200


@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update a customer."""
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Store before state for audit
    before_state = customer.to_dict()
    
    # Update fields if provided
    if 'name' in data:
        customer.name = data['name']
    
    if 'email' in data:
        if not validate_email_format(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if email already exists for another customer
        existing = Customer.query.filter_by(email=data['email']).first()
        if existing and existing.id != customer_id:
            return jsonify({'error': 'Email already in use by another customer'}), 409
        
        customer.email = data['email']
    
    if 'country' in data:
        if not validate_country_code(data['country']):
            return jsonify({'error': 'Invalid country code (must be ISO 3166-1 alpha-2)'}), 400
        customer.country = data['country'].upper()
    
    if 'kyc_status' in data:
        customer.kyc_status = data['kyc_status']
    
    customer.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    
    # Log the update
    audit_logger.log_event(
        action='UPDATE',
        user='system',
        customer_id=customer.id,
        before_state=before_state,
        after_state=customer.to_dict(),
        metadata={'source': 'api'}
    )
    
    return jsonify(customer.to_dict()), 200


@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Delete a customer."""
    customer = Customer.query.get_or_404(customer_id)
    
    # Store before state for audit
    before_state = customer.to_dict()
    
    db.session.delete(customer)
    db.session.commit()
    
    # Log the deletion
    audit_logger.log_event(
        action='DELETE',
        user='system',
        customer_id=customer_id,
        before_state=before_state,
        after_state=None,
        metadata={'source': 'api'}
    )
    
    return '', 204


@app.route('/api/customers/bulk-import', methods=['POST'])
def bulk_import_customers():
    """
    Bulk import customers from CSV file.
    
    Expected CSV format:
    name,email,country
    John Doe,john@example.com,US
    Jane Smith,jane@example.com,GB
    
    Returns:
    {
        "total_rows": 2,
        "successful_imports": 2,
        "failed_rows": []
    }
    """
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'}), 400
    
    try:
        # Read CSV content
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        # Validate headers
        if not csv_reader.fieldnames:
            return jsonify({'error': 'CSV file is empty'}), 400
        
        required_fields = {'name', 'email', 'country'}
        if not required_fields.issubset(set(csv_reader.fieldnames)):
            return jsonify({
                'error': f'CSV must contain columns: {", ".join(required_fields)}'
            }), 400
        
        # Process rows
        total_rows = 0
        successful_imports = 0
        failed_rows = []
        
        for line_num, row in enumerate(csv_reader, start=2):  # Start at 2 (1 for header + 1)
            total_rows += 1
            
            # Check batch size limit
            if total_rows > 500:
                failed_rows.append({
                    'line': line_num,
                    'reason': 'Batch size limit exceeded (max 500 rows)'
                })
                break
            
            # Validate required fields
            name = row.get('name', '').strip()
            email = row.get('email', '').strip()
            country = row.get('country', '').strip()
            
            if not name:
                failed_rows.append({
                    'line': line_num,
                    'reason': 'Missing required field: name'
                })
                continue
            
            if not email:
                failed_rows.append({
                    'line': line_num,
                    'reason': 'Missing required field: email'
                })
                continue
            
            if not country:
                failed_rows.append({
                    'line': line_num,
                    'reason': 'Missing required field: country'
                })
                continue
            
            # Validate email format
            if not validate_email_format(email):
                failed_rows.append({
                    'line': line_num,
                    'reason': 'Invalid email format'
                })
                continue
            
            # Validate country code
            if not validate_country_code(country):
                failed_rows.append({
                    'line': line_num,
                    'reason': 'Invalid country code (must be ISO 3166-1 alpha-2)'
                })
                continue
            
            # Check if email already exists
            existing_customer = Customer.query.filter_by(email=email).first()
            if existing_customer:
                failed_rows.append({
                    'line': line_num,
                    'reason': 'Customer with this email already exists'
                })
                continue
            
            # Create customer
            try:
                # Use a nested transaction (savepoint) for each row
                # This allows us to rollback individual rows without affecting others
                with db.session.begin_nested():
                    customer = Customer(
                        name=name,
                        email=email,
                        country=country.upper(),
                        kyc_status='Pending'
                    )
                    
                    db.session.add(customer)
                    db.session.flush()  # Get the ID and detect any DB errors
                    
                    # Log the creation
                    audit_logger.log_event(
                        action='CREATE',
                        user='system',
                        customer_id=customer.id,
                        before_state=None,
                        after_state=customer.to_dict(),
                        metadata={'source': 'bulk_import', 'line_number': line_num}
                    )
                    
                    successful_imports += 1
            except Exception as e:
                # Nested transaction automatically rolled back on exception
                # Other successful imports remain intact
                failed_rows.append({
                    'line': line_num,
                    'reason': f'Database error: {str(e)}'
                })
        
        # Commit all successful imports
        db.session.commit()
        
        return jsonify({
            'total_rows': total_rows,
            'successful_imports': successful_imports,
            'failed_rows': failed_rows
        }), 200
        
    except UnicodeDecodeError:
        return jsonify({'error': 'File encoding error. Please use UTF-8 encoding'}), 400
    except csv.Error as e:
        return jsonify({'error': f'CSV parsing error: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """Handle file size too large errors."""
    return jsonify({'error': 'File size exceeds 5MB limit'}), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


if __name__ == '__main__':
    # Flask debug mode must be disabled in production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
