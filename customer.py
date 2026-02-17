from typing import Dict, Optional
from datetime import datetime, timezone
import uuid


class Customer:
    """Customer data model for KYC purposes."""
    
    def __init__(
        self,
        customer_id: Optional[str] = None,
        name: str = "",
        email: str = "",
        phone: str = "",
        address: str = "",
        date_of_birth: str = "",
        national_id: str = "",
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.customer_id = customer_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.date_of_birth = date_of_birth
        self.national_id = national_id
        self.created_at = created_at or datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        self.updated_at = updated_at or datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    def to_dict(self) -> Dict:
        """Convert customer to dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Customer':
        """Create customer from dictionary."""
        return cls(**data)
    
    def update(self, **kwargs) -> None:
        """Update customer fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


class CustomerStore:
    """In-memory customer storage."""
    
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
    
    def create(self, customer: Customer) -> Customer:
        """Create a new customer."""
        self.customers[customer.customer_id] = customer
        return customer
    
    def get(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID."""
        return self.customers.get(customer_id)
    
    def update(self, customer_id: str, **kwargs) -> Optional[Customer]:
        """Update a customer."""
        customer = self.customers.get(customer_id)
        if customer:
            customer.update(**kwargs)
        return customer
    
    def delete(self, customer_id: str) -> Optional[Customer]:
        """Delete a customer."""
        return self.customers.pop(customer_id, None)
    
    def list_all(self) -> list:
        """List all customers."""
        return [customer.to_dict() for customer in self.customers.values()]
