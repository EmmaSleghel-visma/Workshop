# Creditro Demo - KYC & AML Compliance Management

A demo web application inspired by Creditro, built for workshop demonstrations. This application showcases a KYC (Know Your Customer) and AML (Anti-Money Laundering) compliance management system.

## Overview

Creditro Demo helps businesses manage customer onboarding and compliance workflows with features including:
- **Customer Onboarding**: Collect and manage KYC information
- **Risk Assessment**: Evaluate and track customer risk levels
- **Compliance Checks**: Manage various compliance verification steps
- **Status Tracking**: Monitor KYC status throughout the customer lifecycle

## Technology Stack

### Backend
- **.NET 10.0** - ASP.NET Core Web API
- **In-memory data store** - For demonstration purposes (pre-seeded with sample customers)
- **RESTful API** - Clean API endpoints for all operations

### Frontend
- **Angular 19+** - Modern Angular with standalone components
- **TypeScript** - Type-safe development
- **CSS** - Custom styling for a professional look
- **Angular Router** - Client-side routing
- **RxJS** - Reactive programming with Observables

## Features

### 1. Customer List View
- View all customers in a clean, organized table
- See KYC status with color-coded badges (Pending, In Progress, Completed, Rejected)
- View risk levels (Low, Medium, High)
- Quick access to customer details

### 2. Customer Detail View
- Complete customer information display
- Update KYC status with dropdown selector
- Modify risk assessment levels
- View and manage compliance checks
- Add new compliance checks on the fly

### 3. Customer Onboarding Form
- Comprehensive form for new customer registration
- Personal information collection (Name, Email, Phone)
- Company information (Company Name, Business Number, Country, Address)
- Form validation with required fields
- Clean, intuitive user interface

## Screenshots

### Customer List
![Customer List](https://github.com/user-attachments/assets/05bd491c-eb69-4d0d-adc4-8b10e40525e7)

### Customer Detail
![Customer Detail](https://github.com/user-attachments/assets/7e7c74bd-b3af-45ee-ad6d-a314e4ad720e)

### Add Customer Form
![Customer Form](https://github.com/user-attachments/assets/2e058ade-88ca-4a4f-960e-24d30abd5c88)

## Getting Started

### Prerequisites
- [.NET 10.0 SDK](https://dotnet.microsoft.com/download)
- [Node.js 18+](https://nodejs.org/) and npm

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/EmmaSleghel-visma/Workshop.git
   cd Workshop
   ```

2. **Start the Backend API**
   ```bash
   cd backend/CreditroDemo.API
   dotnet restore
   dotnet run --urls "http://localhost:5000"
   ```
   
   The API will be available at http://localhost:5000

3. **Start the Frontend (in a new terminal)**
   ```bash
   cd frontend
   npm install
   npm start
   ```
   
   The Angular app will be available at http://localhost:4200

4. **Access the Application**
   
   Open your browser and navigate to http://localhost:4200

## API Endpoints

The backend API provides the following endpoints:

- `GET /api/customers` - Get all customers
- `GET /api/customers/{id}` - Get a specific customer
- `POST /api/customers` - Create a new customer
- `PATCH /api/customers/{id}/kyc-status` - Update KYC status
- `PATCH /api/customers/{id}/risk-level` - Update risk level
- `POST /api/customers/{id}/compliance-checks` - Add a compliance check

## Sample Data

The application comes pre-seeded with three sample customers:

1. **John Anderson** - TechCorp Solutions (United States) - Completed, Low Risk
2. **Maria Garcia** - Finance Group Ltd (Spain) - In Progress, Medium Risk
3. **Lars Nielsen** - Nordic Bank A/S (Denmark) - Pending, Low Risk

## Development

### Backend Development
```bash
cd backend/CreditroDemo.API
dotnet build
dotnet watch run --urls "http://localhost:5000"
```

### Frontend Development
```bash
cd frontend
npm start
```

The Angular development server supports hot reload for quick development.

## Project Structure

```
Workshop/
├── backend/
│   └── CreditroDemo.API/
│       ├── Controllers/       # API Controllers
│       ├── Models/           # Data models
│       ├── Services/         # Business logic
│       └── Program.cs        # Application entry point
│
├── frontend/
│   └── src/
│       └── app/
│           ├── components/   # Angular components
│           ├── models/       # TypeScript interfaces
│           ├── services/     # HTTP services
│           └── app.ts        # Root component
│
└── README.md
```

## Future Enhancements

For production use, consider adding:
- Persistent database (SQL Server, PostgreSQL)
- Authentication and authorization
- Document upload and management
- Audit logging
- Real-time notifications
- Advanced reporting and analytics
- Integration with external compliance services

## Workshop Use

This demo application is designed for workshop presentations to:
- Demonstrate modern .NET and Angular development
- Show RESTful API design patterns
- Illustrate responsive UI design
- Showcase business application workflows

## License

This is a demonstration project created for workshop purposes.

## Author

Created for Visma Creditro workshop demonstrations.
