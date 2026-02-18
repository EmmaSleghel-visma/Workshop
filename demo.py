"""Demo script to test the bulk import functionality."""
import requests
import json

# Base URL for the API
BASE_URL = 'http://localhost:5000/api'


def test_single_customer_creation():
    """Test creating a single customer."""
    print("Testing single customer creation...")
    response = requests.post(
        f'{BASE_URL}/customers',
        json={
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'country': 'US'
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_bulk_import():
    """Test bulk importing customers from CSV."""
    print("Testing bulk import...")
    
    # Read the test CSV file
    with open('tests/fixtures/valid_customers.csv', 'rb') as f:
        files = {'file': ('customers.csv', f, 'text/csv')}
        response = requests.post(
            f'{BASE_URL}/customers/bulk-import',
            files=files
        )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_list_customers():
    """Test listing all customers."""
    print("Listing all customers...")
    response = requests.get(f'{BASE_URL}/customers')
    print(f"Status: {response.status_code}")
    customers = response.json()
    print(f"Total customers: {len(customers)}")
    for customer in customers:
        print(f"  - {customer['name']} ({customer['email']}) - KYC Status: {customer['kyc_status']}")
    print()


if __name__ == '__main__':
    print("=" * 60)
    print("Customer Management API Demo")
    print("=" * 60)
    print()
    
    try:
        test_single_customer_creation()
        test_bulk_import()
        test_list_customers()
        print("All tests completed successfully!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Please start the server first with: python app.py")
    except Exception as e:
        print(f"Error: {e}")
