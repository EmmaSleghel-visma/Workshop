import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Customer, CreateCustomerRequest, ComplianceCheck, KycStatus, RiskLevel } from '../models/customer.model';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  private apiUrl = 'http://localhost:5000/api/customers';

  constructor(private http: HttpClient) { }

  getAllCustomers(): Observable<Customer[]> {
    return this.http.get<Customer[]>(this.apiUrl);
  }

  getCustomer(id: string): Observable<Customer> {
    return this.http.get<Customer>(`${this.apiUrl}/${id}`);
  }

  createCustomer(request: CreateCustomerRequest): Observable<Customer> {
    return this.http.post<Customer>(this.apiUrl, request);
  }

  updateKycStatus(id: string, status: KycStatus): Observable<Customer> {
    return this.http.patch<Customer>(`${this.apiUrl}/${id}/kyc-status`, status, {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  updateRiskLevel(id: string, riskLevel: RiskLevel): Observable<Customer> {
    return this.http.patch<Customer>(`${this.apiUrl}/${id}/risk-level`, riskLevel, {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  addComplianceCheck(id: string, check: Partial<ComplianceCheck>): Observable<Customer> {
    return this.http.post<Customer>(`${this.apiUrl}/${id}/compliance-checks`, check);
  }
}
