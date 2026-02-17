#!/usr/bin/env python3
"""
Demo script showcasing KYC audit logging functionality.
This script demonstrates the complete lifecycle of customer data with audit logging.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def pretty_print(data):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=2))

def main():
    print("KYC Audit Logging Demo")
    print("="*60)
    print("This demo showcases comprehensive audit logging for customer data mutations")
    
    # 1. Create a customer
    print_section("1. Creating a Customer")
    customer_data = {
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "phone": "+1234567890",
        "address": "456 Oak Avenue",
        "date_of_birth": "1985-05-15",
        "national_id": "XYZ789012"
    }
    
    response = requests.post(
        f"{BASE_URL}/customers",
        json=customer_data,
        headers={"X-User-Id": "admin@example.com"}
    )
    
    if response.status_code == 201:
        result = response.json()
        customer_id = result['customer']['customer_id']
        print(f"✓ Customer created successfully!")
        print(f"  Customer ID: {customer_id}")
        print(f"  Name: {result['customer']['name']}")
        print(f"  Email: {result['customer']['email']}")
    else:
        print(f"✗ Failed to create customer: {response.text}")
        return
    
    time.sleep(1)
    
    # 2. Update the customer
    print_section("2. Updating the Customer")
    update_data = {
        "phone": "+9876543210",
        "address": "789 Pine Street, Apt 4B"
    }
    
    response = requests.put(
        f"{BASE_URL}/customers/{customer_id}",
        json=update_data,
        headers={"X-User-Id": "manager@example.com"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Customer updated successfully!")
        print(f"  New Phone: {result['customer']['phone']}")
        print(f"  New Address: {result['customer']['address']}")
    else:
        print(f"✗ Failed to update customer: {response.text}")
    
    time.sleep(1)
    
    # 3. View audit logs for this customer
    print_section("3. Viewing Audit Logs for This Customer")
    response = requests.get(f"{BASE_URL}/audit-logs?entity_id={customer_id}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Found {result['count']} audit log entries:")
        for i, log in enumerate(result['logs'], 1):
            print(f"\n  Entry {i}:")
            print(f"    Action: {log['action']}")
            print(f"    User: {log['user']}")
            print(f"    Timestamp: {log['timestamp']}")
            if log['data_before'] and log['data_after']:
                print(f"    Changes:")
                if log['data_before']['phone'] != log['data_after']['phone']:
                    print(f"      Phone: {log['data_before']['phone']} → {log['data_after']['phone']}")
                if log['data_before']['address'] != log['data_after']['address']:
                    print(f"      Address: {log['data_before']['address']} → {log['data_after']['address']}")
    
    time.sleep(1)
    
    # 4. Delete the customer
    print_section("4. Deleting the Customer")
    response = requests.delete(
        f"{BASE_URL}/customers/{customer_id}",
        headers={"X-User-Id": "compliance@example.com"}
    )
    
    if response.status_code == 200:
        print(f"✓ Customer deleted successfully!")
    else:
        print(f"✗ Failed to delete customer: {response.text}")
    
    time.sleep(1)
    
    # 5. View complete audit trail
    print_section("5. Complete Audit Trail (All Operations)")
    response = requests.get(f"{BASE_URL}/audit-logs?entity_id={customer_id}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Complete audit trail with {result['count']} entries:")
        for log in result['logs']:
            print(f"\n  [{log['timestamp']}] {log['action']} by {log['user']}")
            if log['action'] == 'DELETE':
                print(f"    Deleted customer: {log['data_before']['name']}")
    
    # 6. Summary
    print_section("Demo Summary")
    print("✓ All customer data mutations have been logged")
    print("✓ Audit trail includes:")
    print("  - CREATE operation with complete customer data")
    print("  - UPDATE operation with before/after states")
    print("  - DELETE operation with final customer data")
    print("\n✓ Each log entry contains:")
    print("  - ISO 8601 timestamp")
    print("  - User who performed the action")
    print("  - Action type (CREATE/UPDATE/DELETE)")
    print("  - Complete data states (before/after)")
    print("  - Metadata (IP address, user agent)")
    
    print("\n" + "="*60)
    print("Demo completed successfully!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to the API server.")
        print("  Please start the server first with: python app.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")
