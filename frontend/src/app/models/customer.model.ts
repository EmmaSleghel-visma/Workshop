export interface Customer {
  id: string;
  fullName: string;
  email: string;
  phoneNumber?: string;
  companyName: string;
  businessNumber?: string;
  country: string;
  address?: string;
  createdAt: string;
  kycStatus: KycStatus;
  riskLevel: RiskLevel;
  complianceChecks: ComplianceCheck[];
}

export interface CreateCustomerRequest {
  fullName: string;
  email: string;
  phoneNumber?: string;
  companyName: string;
  businessNumber?: string;
  country: string;
  address?: string;
}

export interface ComplianceCheck {
  id: string;
  customerId: string;
  checkType: string;
  status: CheckStatus;
  notes?: string;
  checkedAt: string;
}

export enum KycStatus {
  Pending = 0,
  InProgress = 1,
  Completed = 2,
  Rejected = 3
}

export enum RiskLevel {
  Low = 0,
  Medium = 1,
  High = 2
}

export enum CheckStatus {
  Pending = 0,
  Passed = 1,
  Failed = 2,
  RequiresReview = 3
}

export const KycStatusLabels = {
  [KycStatus.Pending]: 'Pending',
  [KycStatus.InProgress]: 'In Progress',
  [KycStatus.Completed]: 'Completed',
  [KycStatus.Rejected]: 'Rejected'
};

export const RiskLevelLabels = {
  [RiskLevel.Low]: 'Low',
  [RiskLevel.Medium]: 'Medium',
  [RiskLevel.High]: 'High'
};

export const CheckStatusLabels = {
  [CheckStatus.Pending]: 'Pending',
  [CheckStatus.Passed]: 'Passed',
  [CheckStatus.Failed]: 'Failed',
  [CheckStatus.RequiresReview]: 'Requires Review'
};
