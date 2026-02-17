import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CustomerService } from '../../services/customer.service';
import { Customer, KycStatusLabels, RiskLevelLabels } from '../../models/customer.model';

@Component({
  selector: 'app-customer-list',
  imports: [CommonModule, RouterModule],
  templateUrl: './customer-list.html',
  styleUrl: './customer-list.css',
})
export class CustomerList implements OnInit {
  customers: Customer[] = [];
  loading = true;
  error: string | null = null;
  kycStatusLabels = KycStatusLabels;
  riskLevelLabels = RiskLevelLabels;

  constructor(private customerService: CustomerService) {}

  ngOnInit(): void {
    this.loadCustomers();
  }

  loadCustomers(): void {
    this.loading = true;
    this.error = null;
    this.customerService.getAllCustomers().subscribe({
      next: (customers) => {
        this.customers = customers;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load customers. Please ensure the API is running.';
        this.loading = false;
        console.error('Error loading customers:', err);
      }
    });
  }

  getStatusClass(status: number): string {
    switch (status) {
      case 0: return 'status-pending';
      case 1: return 'status-progress';
      case 2: return 'status-completed';
      case 3: return 'status-rejected';
      default: return '';
    }
  }

  getRiskClass(riskLevel: number): string {
    switch (riskLevel) {
      case 0: return 'risk-low';
      case 1: return 'risk-medium';
      case 2: return 'risk-high';
      default: return '';
    }
  }
}
