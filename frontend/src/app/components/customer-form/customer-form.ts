import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CustomerService } from '../../services/customer.service';
import { CreateCustomerRequest } from '../../models/customer.model';

@Component({
  selector: 'app-customer-form',
  imports: [CommonModule, FormsModule],
  templateUrl: './customer-form.html',
  styleUrl: './customer-form.css',
})
export class CustomerForm {
  customer: CreateCustomerRequest = {
    fullName: '',
    email: '',
    phoneNumber: '',
    companyName: '',
    businessNumber: '',
    country: '',
    address: ''
  };

  submitting = false;
  error: string | null = null;

  constructor(
    private customerService: CustomerService,
    private router: Router
  ) {}

  onSubmit(): void {
    if (!this.isValid()) {
      return;
    }

    this.submitting = true;
    this.error = null;

    this.customerService.createCustomer(this.customer).subscribe({
      next: (result) => {
        console.log('Customer created:', result);
        this.router.navigate(['/customer', result.id]);
      },
      error: (err) => {
        this.error = 'Failed to create customer. Please try again.';
        this.submitting = false;
        console.error('Error creating customer:', err);
      }
    });
  }

  isValid(): boolean {
    return !!(this.customer.fullName && this.customer.email && 
              this.customer.companyName && this.customer.country);
  }

  cancel(): void {
    this.router.navigate(['/']);
  }
}
