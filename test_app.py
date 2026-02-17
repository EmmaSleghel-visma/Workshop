import unittest
import json
import os
from app import app, customer_store, audit_logger
from customer import Customer


class TestKYCAuditLogging(unittest.TestCase):
    """Test KYC audit logging for all customer data mutations."""
    
    def setUp(self):
        """Set up test client and clean state."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Clear customer store
        customer_store.customers.clear()
        
        # Clear audit logs
        if os.path.exists('audit_logs.json'):
            os.remove('audit_logs.json')
        audit_logger._ensure_log_file_exists()
    
    def tearDown(self):
        """Clean up after tests."""
        customer_store.customers.clear()
        if os.path.exists('audit_logs.json'):
            os.remove('audit_logs.json')
    
    def test_create_customer_with_audit_log(self):
        """Test that customer creation is logged in audit logs."""
        # Create a customer
        customer_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "address": "123 Main St",
            "date_of_birth": "1990-01-01",
            "national_id": "ABC123456"
        }
        
        response = self.client.post(
            '/customers',
            data=json.dumps(customer_data),
            content_type='application/json',
            headers={'X-User-Id': 'test_user'}
        )
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        customer_id = response_data['customer']['customer_id']
        
        # Verify audit log was created
        logs_response = self.client.get('/audit-logs')
        logs_data = json.loads(logs_response.data)
        
        self.assertEqual(len(logs_data['logs']), 1)
        log = logs_data['logs'][0]
        
        self.assertEqual(log['action'], 'CREATE')
        self.assertEqual(log['entity_type'], 'customer')
        self.assertEqual(log['entity_id'], customer_id)
        self.assertEqual(log['user'], 'test_user')
        self.assertIsNone(log['data_before'])
        self.assertIsNotNone(log['data_after'])
        self.assertEqual(log['data_after']['name'], 'John Doe')
        self.assertEqual(log['data_after']['email'], 'john.doe@example.com')
    
    def test_update_customer_with_audit_log(self):
        """Test that customer updates are logged with before/after states."""
        # First create a customer
        customer_data = {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "+1987654321"
        }
        
        create_response = self.client.post(
            '/customers',
            data=json.dumps(customer_data),
            content_type='application/json',
            headers={'X-User-Id': 'test_user'}
        )
        
        customer_id = json.loads(create_response.data)['customer']['customer_id']
        
        # Update the customer
        update_data = {
            "name": "Jane Doe",
            "phone": "+1111111111"
        }
        
        update_response = self.client.put(
            f'/customers/{customer_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'X-User-Id': 'admin_user'}
        )
        
        self.assertEqual(update_response.status_code, 200)
        
        # Verify audit logs (should have 2: CREATE and UPDATE)
        logs_response = self.client.get('/audit-logs')
        logs_data = json.loads(logs_response.data)
        
        self.assertEqual(len(logs_data['logs']), 2)
        
        # Check UPDATE log
        update_log = logs_data['logs'][1]
        self.assertEqual(update_log['action'], 'UPDATE')
        self.assertEqual(update_log['entity_type'], 'customer')
        self.assertEqual(update_log['entity_id'], customer_id)
        self.assertEqual(update_log['user'], 'admin_user')
        
        # Verify before state
        self.assertEqual(update_log['data_before']['name'], 'Jane Smith')
        self.assertEqual(update_log['data_before']['phone'], '+1987654321')
        
        # Verify after state
        self.assertEqual(update_log['data_after']['name'], 'Jane Doe')
        self.assertEqual(update_log['data_after']['phone'], '+1111111111')
        
        # Verify fields_updated metadata
        self.assertIn('fields_updated', update_log['metadata'])
        self.assertIn('name', update_log['metadata']['fields_updated'])
        self.assertIn('phone', update_log['metadata']['fields_updated'])
    
    def test_delete_customer_with_audit_log(self):
        """Test that customer deletion is logged."""
        # First create a customer
        customer_data = {
            "name": "Bob Johnson",
            "email": "bob.johnson@example.com"
        }
        
        create_response = self.client.post(
            '/customers',
            data=json.dumps(customer_data),
            content_type='application/json',
            headers={'X-User-Id': 'test_user'}
        )
        
        customer_id = json.loads(create_response.data)['customer']['customer_id']
        
        # Delete the customer
        delete_response = self.client.delete(
            f'/customers/{customer_id}',
            headers={'X-User-Id': 'admin_user'}
        )
        
        self.assertEqual(delete_response.status_code, 200)
        
        # Verify customer is deleted
        get_response = self.client.get(f'/customers/{customer_id}')
        self.assertEqual(get_response.status_code, 404)
        
        # Verify audit logs (should have 2: CREATE and DELETE)
        logs_response = self.client.get('/audit-logs')
        logs_data = json.loads(logs_response.data)
        
        self.assertEqual(len(logs_data['logs']), 2)
        
        # Check DELETE log
        delete_log = logs_data['logs'][1]
        self.assertEqual(delete_log['action'], 'DELETE')
        self.assertEqual(delete_log['entity_type'], 'customer')
        self.assertEqual(delete_log['entity_id'], customer_id)
        self.assertEqual(delete_log['user'], 'admin_user')
        
        # Verify before state is captured
        self.assertIsNotNone(delete_log['data_before'])
        self.assertEqual(delete_log['data_before']['name'], 'Bob Johnson')
        
        # Verify after state is None
        self.assertIsNone(delete_log['data_after'])
    
    def test_audit_log_filtering(self):
        """Test that audit logs can be filtered."""
        # Create multiple customers with different users
        customer1_data = {"name": "User1 Customer", "email": "user1@example.com"}
        customer2_data = {"name": "User2 Customer", "email": "user2@example.com"}
        
        response1 = self.client.post(
            '/customers',
            data=json.dumps(customer1_data),
            content_type='application/json',
            headers={'X-User-Id': 'user1'}
        )
        
        response2 = self.client.post(
            '/customers',
            data=json.dumps(customer2_data),
            content_type='application/json',
            headers={'X-User-Id': 'user2'}
        )
        
        customer1_id = json.loads(response1.data)['customer']['customer_id']
        
        # Filter by user
        logs_response = self.client.get('/audit-logs?user=user1')
        logs_data = json.loads(logs_response.data)
        
        self.assertEqual(len(logs_data['logs']), 1)
        self.assertEqual(logs_data['logs'][0]['user'], 'user1')
        
        # Filter by entity_id
        logs_response = self.client.get(f'/audit-logs?entity_id={customer1_id}')
        logs_data = json.loads(logs_response.data)
        
        self.assertEqual(len(logs_data['logs']), 1)
        self.assertEqual(logs_data['logs'][0]['entity_id'], customer1_id)
        
        # Filter by action
        logs_response = self.client.get('/audit-logs?action=CREATE')
        logs_data = json.loads(logs_response.data)
        
        self.assertEqual(len(logs_data['logs']), 2)
        for log in logs_data['logs']:
            self.assertEqual(log['action'], 'CREATE')
    
    def test_read_operations_not_logged(self):
        """Test that read operations (GET) are not logged."""
        # Create a customer
        customer_data = {"name": "Test User", "email": "test@example.com"}
        
        create_response = self.client.post(
            '/customers',
            data=json.dumps(customer_data),
            content_type='application/json',
            headers={'X-User-Id': 'test_user'}
        )
        
        customer_id = json.loads(create_response.data)['customer']['customer_id']
        
        # Perform read operations
        self.client.get('/customers')
        self.client.get(f'/customers/{customer_id}')
        self.client.get('/audit-logs')
        
        # Verify only 1 log entry (CREATE)
        logs_response = self.client.get('/audit-logs')
        logs_data = json.loads(logs_response.data)
        
        self.assertEqual(len(logs_data['logs']), 1)
        self.assertEqual(logs_data['logs'][0]['action'], 'CREATE')
    
    def test_audit_log_includes_metadata(self):
        """Test that audit logs include metadata like IP and user agent."""
        customer_data = {"name": "Metadata Test", "email": "metadata@example.com"}
        
        response = self.client.post(
            '/customers',
            data=json.dumps(customer_data),
            content_type='application/json',
            headers={
                'X-User-Id': 'test_user',
                'User-Agent': 'TestClient/1.0'
            }
        )
        
        # Get audit logs
        logs_response = self.client.get('/audit-logs')
        logs_data = json.loads(logs_response.data)
        
        log = logs_data['logs'][0]
        self.assertIn('metadata', log)
        self.assertIn('ip_address', log['metadata'])
        self.assertIn('user_agent', log['metadata'])
        self.assertEqual(log['metadata']['user_agent'], 'TestClient/1.0')


if __name__ == '__main__':
    unittest.main()
