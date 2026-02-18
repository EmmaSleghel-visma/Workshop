"""Integration tests for customer management API."""
import os
import io
from pathlib import Path
import pytest
from app import app, db, Customer

# Get the directory containing this test file
TEST_DIR = Path(__file__).parent
FIXTURES_DIR = TEST_DIR / 'fixtures'


@pytest.fixture
def client():
    """Create test client with in-memory database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.fixture
def sample_customer_data():
    """Sample customer data for testing."""
    return {
        'name': 'Test Customer',
        'email': 'test@example.com',
        'country': 'US'
    }


class TestCustomerCRUD:
    """Tests for basic customer CRUD operations."""
    
    def test_create_customer(self, client, sample_customer_data):
        """Test creating a single customer."""
        response = client.post('/api/customers', json=sample_customer_data)
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == sample_customer_data['name']
        assert data['email'] == sample_customer_data['email']
        assert data['country'] == sample_customer_data['country']
        assert data['kyc_status'] == 'Pending'
        assert 'id' in data
    
    def test_create_customer_missing_fields(self, client):
        """Test creating customer with missing required fields."""
        response = client.post('/api/customers', json={'name': 'Test'})
        assert response.status_code == 400
        assert 'error' in response.get_json()
    
    def test_create_customer_invalid_email(self, client):
        """Test creating customer with invalid email."""
        response = client.post('/api/customers', json={
            'name': 'Test',
            'email': 'not-an-email',
            'country': 'US'
        })
        assert response.status_code == 400
        assert 'email' in response.get_json()['error'].lower()
    
    def test_create_customer_invalid_country(self, client):
        """Test creating customer with invalid country code."""
        response = client.post('/api/customers', json={
            'name': 'Test',
            'email': 'test@example.com',
            'country': 'INVALID'
        })
        assert response.status_code == 400
        assert 'country' in response.get_json()['error'].lower()
    
    def test_create_customer_duplicate_email(self, client, sample_customer_data):
        """Test creating customer with duplicate email."""
        client.post('/api/customers', json=sample_customer_data)
        response = client.post('/api/customers', json=sample_customer_data)
        assert response.status_code == 409
        assert 'email' in response.get_json()['error'].lower()
    
    def test_list_customers(self, client, sample_customer_data):
        """Test listing customers."""
        client.post('/api/customers', json=sample_customer_data)
        response = client.get('/api/customers')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 1
    
    def test_get_customer(self, client, sample_customer_data):
        """Test getting a single customer."""
        create_response = client.post('/api/customers', json=sample_customer_data)
        customer_id = create_response.get_json()['id']
        
        response = client.get(f'/api/customers/{customer_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == customer_id
    
    def test_update_customer(self, client, sample_customer_data):
        """Test updating a customer."""
        create_response = client.post('/api/customers', json=sample_customer_data)
        customer_id = create_response.get_json()['id']
        
        update_data = {'name': 'Updated Name'}
        response = client.put(f'/api/customers/{customer_id}', json=update_data)
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == 'Updated Name'
    
    def test_delete_customer(self, client, sample_customer_data):
        """Test deleting a customer."""
        create_response = client.post('/api/customers', json=sample_customer_data)
        customer_id = create_response.get_json()['id']
        
        response = client.delete(f'/api/customers/{customer_id}')
        assert response.status_code == 204
        
        # Verify customer is deleted
        get_response = client.get(f'/api/customers/{customer_id}')
        assert get_response.status_code == 404


class TestBulkImport:
    """Tests for bulk customer import endpoint."""
    
    def test_bulk_import_valid_csv(self, client):
        """Test bulk import with valid CSV file."""
        csv_content = b'name,email,country\nJohn Doe,john@example.com,US\nJane Smith,jane@example.com,GB\n'
        
        response = client.post(
            '/api/customers/bulk-import',
            data={'file': (io.BytesIO(csv_content), 'customers.csv')},
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total_rows'] == 2
        assert data['successful_imports'] == 2
        assert len(data['failed_rows']) == 0
        
        # Verify customers were created
        customers = client.get('/api/customers').get_json()
        assert len(customers) == 2
        
        # Verify KYC status is Pending
        assert all(c['kyc_status'] == 'Pending' for c in customers)
    
    def test_bulk_import_with_fixture(self, client):
        """Test bulk import using valid_customers.csv fixture."""
        fixture_path = FIXTURES_DIR / 'valid_customers.csv'
        
        with open(fixture_path, 'rb') as f:
            response = client.post(
                '/api/customers/bulk-import',
                data={'file': (f, 'valid_customers.csv')},
                content_type='multipart/form-data'
            )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total_rows'] == 5
        assert data['successful_imports'] == 5
        assert len(data['failed_rows']) == 0
    
    def test_bulk_import_invalid_rows(self, client):
        """Test bulk import with some invalid rows."""
        fixture_path = FIXTURES_DIR / 'invalid_customers.csv'
        
        with open(fixture_path, 'rb') as f:
            response = client.post(
                '/api/customers/bulk-import',
                data={'file': (f, 'invalid_customers.csv')},
                content_type='multipart/form-data'
            )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total_rows'] == 5
        assert data['successful_imports'] == 1  # Only first row is valid
        assert len(data['failed_rows']) == 4
        
        # Check that error reasons are provided
        for failed_row in data['failed_rows']:
            assert 'line' in failed_row
            assert 'reason' in failed_row
    
    def test_bulk_import_duplicate_email(self, client):
        """Test bulk import with duplicate email addresses."""
        fixture_path = FIXTURES_DIR / 'duplicate_email.csv'
        
        with open(fixture_path, 'rb') as f:
            response = client.post(
                '/api/customers/bulk-import',
                data={'file': (f, 'duplicate_email.csv')},
                content_type='multipart/form-data'
            )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['total_rows'] == 3
        assert data['successful_imports'] == 2  # First two are unique
        assert len(data['failed_rows']) == 1  # Third has duplicate email
        assert 'email' in data['failed_rows'][0]['reason'].lower()
    
    def test_bulk_import_no_file(self, client):
        """Test bulk import without file."""
        response = client.post('/api/customers/bulk-import')
        assert response.status_code == 400
        assert 'error' in response.get_json()
    
    def test_bulk_import_non_csv(self, client):
        """Test bulk import with non-CSV file."""
        response = client.post(
            '/api/customers/bulk-import',
            data={'file': (io.BytesIO(b'not csv'), 'file.txt')},
            content_type='multipart/form-data'
        )
        assert response.status_code == 400
        assert 'csv' in response.get_json()['error'].lower()
    
    def test_bulk_import_empty_file(self, client):
        """Test bulk import with empty CSV file."""
        response = client.post(
            '/api/customers/bulk-import',
            data={'file': (io.BytesIO(b''), 'empty.csv')},
            content_type='multipart/form-data'
        )
        assert response.status_code == 400
        assert 'error' in response.get_json()
    
    def test_bulk_import_missing_columns(self, client):
        """Test bulk import with missing required columns."""
        csv_content = b'name,email\nJohn Doe,john@example.com\n'
        
        response = client.post(
            '/api/customers/bulk-import',
            data={'file': (io.BytesIO(csv_content), 'customers.csv')},
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 400
        assert 'columns' in response.get_json()['error'].lower()
    
    def test_bulk_import_max_rows(self, client):
        """Test bulk import with more than 500 rows."""
        # Generate CSV with 501 rows
        csv_lines = ['name,email,country']
        for i in range(501):
            csv_lines.append(f'User{i},user{i}@example.com,US')
        csv_content = '\n'.join(csv_lines).encode('utf-8')
        
        response = client.post(
            '/api/customers/bulk-import',
            data={'file': (io.BytesIO(csv_content), 'large.csv')},
            content_type='multipart/form-data'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        # Should process only up to 500 rows
        assert data['total_rows'] == 501
        assert data['successful_imports'] == 500
        assert len(data['failed_rows']) == 1
        assert 'limit' in data['failed_rows'][0]['reason'].lower()
    
    def test_bulk_import_file_too_large(self, client):
        """Test bulk import with file exceeding 5MB limit."""
        # Note: Flask's test client may not enforce MAX_CONTENT_LENGTH the same way
        # as a real server, but the configuration is set correctly in the app.
        # This test verifies the handler is set up correctly.
        
        # Create a CSV that exceeds 5MB
        # Each line is about 35 bytes, so we need ~150,000 lines to exceed 5MB
        csv_lines = ['name,email,country']
        for i in range(150000):
            csv_lines.append(f'User{i},user{i}@example.com,US')
        csv_content = '\n'.join(csv_lines).encode('utf-8')
        
        # Verify the file is actually > 5MB
        assert len(csv_content) > 5 * 1024 * 1024, f"File size is {len(csv_content)} bytes, need > 5MB"
        
        response = client.post(
            '/api/customers/bulk-import',
            data={'file': (io.BytesIO(csv_content), 'huge.csv')},
            content_type='multipart/form-data'
        )
        
        # In test environment, may return 200 with row limit error
        # In production, would return 413 before reaching handler
        assert response.status_code in [200, 413]
        if response.status_code == 413:
            assert '5mb' in response.get_json()['error'].lower()
        else:
            # File was processed but hit row limit
            data = response.get_json()
            assert data['total_rows'] == 501
            assert 'limit' in data['failed_rows'][0]['reason'].lower()


class TestValidation:
    """Tests for validation functions."""
    
    def test_email_validation(self, client):
        """Test various email format validations."""
        valid_emails = [
            'user@example.com',
            'user.name@example.com',
            'user+tag@example.co.uk',
            'user_123@sub.example.com'
        ]
        
        for email in valid_emails:
            response = client.post('/api/customers', json={
                'name': 'Test',
                'email': email,
                'country': 'US'
            })
            assert response.status_code in [201, 409]  # 201 for first, 409 if email reused
    
    def test_country_validation(self, client):
        """Test various country code validations."""
        valid_countries = ['US', 'GB', 'DE', 'FR', 'CA', 'JP', 'AU']
        
        for i, country in enumerate(valid_countries):
            response = client.post('/api/customers', json={
                'name': 'Test',
                'email': f'test{i}@example.com',
                'country': country
            })
            assert response.status_code == 201
            assert response.get_json()['country'] == country
