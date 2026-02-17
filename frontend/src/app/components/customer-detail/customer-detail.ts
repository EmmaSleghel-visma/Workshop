import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CustomerService } from '../../services/customer.service';
import { Customer, KycStatus, RiskLevel, CheckStatus, KycStatusLabels, RiskLevelLabels, CheckStatusLabels } from '../../models/customer.model';

@Component({
  selector: 'app-customer-detail',
  imports: [CommonModule, RouterModule],
  templateUrl: './customer-detail.html',
  styleUrl: './customer-detail.css',
})
export class CustomerDetail implements OnInit {
  customer: Customer | null = null;
  loading = true;
  error: string | null = null;
  
  kycStatusLabels = KycStatusLabels;
  riskLevelLabels = RiskLevelLabels;
  checkStatusLabels = CheckStatusLabels;
  
  kycStatuses = Object.keys(KycStatus).filter(k => !isNaN(Number(k))).map(k => ({
    value: Number(k),
    label: KycStatusLabels[Number(k) as KycStatus]
  }));
  
  riskLevels = Object.keys(RiskLevel).filter(k => !isNaN(Number(k))).map(k => ({
    value: Number(k),
    label: RiskLevelLabels[Number(k) as RiskLevel]
  }));

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private customerService: CustomerService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadCustomer(id);
    }
  }

  loadCustomer(id: string): void {
    this.loading = true;
    this.error = null;
    this.customerService.getCustomer(id).subscribe({
      next: (customer) => {
        this.customer = customer;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'Failed to load customer details.';
        this.loading = false;
        this.cdr.detectChanges();
        console.error('Error loading customer:', err);
      }
    });
  }

  updateKycStatus(status: number): void {
    if (!this.customer) return;
    
    this.customerService.updateKycStatus(this.customer.id, status as KycStatus).subscribe({
      next: (updated) => {
        this.customer = updated;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error updating KYC status:', err);
        alert('Failed to update KYC status');
      }
    });
  }

  updateRiskLevel(riskLevel: number): void {
    if (!this.customer) return;
    
    this.customerService.updateRiskLevel(this.customer.id, riskLevel as RiskLevel).subscribe({
      next: (updated) => {
        this.customer = updated;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error updating risk level:', err);
        alert('Failed to update risk level');
      }
    });
  }

  addComplianceCheck(checkType: string): void {
    if (!this.customer) return;
    
    const check = {
      checkType: checkType,
      status: CheckStatus.Pending,
      notes: 'Check initiated'
    };
    
    this.customerService.addComplianceCheck(this.customer.id, check).subscribe({
      next: (updated) => {
        this.customer = updated;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error adding compliance check:', err);
        alert('Failed to add compliance check');
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/']);
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

  getCheckStatusClass(status: number): string {
    switch (status) {
      case 0: return 'check-pending';
      case 1: return 'check-passed';
      case 2: return 'check-failed';
      case 3: return 'check-review';
      default: return '';
    }
  }
}
