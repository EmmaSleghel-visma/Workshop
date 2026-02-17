import { Routes } from '@angular/router';
import { CustomerList } from './components/customer-list/customer-list';
import { CustomerDetail } from './components/customer-detail/customer-detail';
import { CustomerForm } from './components/customer-form/customer-form';

export const routes: Routes = [
  { path: '', component: CustomerList },
  { path: 'customer/:id', component: CustomerDetail },
  { path: 'new-customer', component: CustomerForm }
];
