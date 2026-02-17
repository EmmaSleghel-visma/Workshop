# Custom Agents, Instructions & Skills Demo

## Overview
This demo covers the 5-layer customization hierarchy for GitHub Copilot:
1. Base Copilot behavior (default)
2. Workspace/Repository instructions (`.github/copilot-instructions.md`)
3. Folder-level instructions (`.github/instructions/*.instructions.md`)
4. Custom Agents (`.github/agents/*.agent.md`)
5. Agent Skills (`.github/skills/*/skill.md`)

## Part 1: Custom Agents

### What are Custom Agents?
Custom agents (formerly "chat modes") are predefined AI personas with specific behaviors, knowledge, and workflows. They appear as @mentions in Copilot Chat.

### Demo: Using the Reviewer Agent

**Step 1: Verify Agent Exists**
```
In Copilot Chat:
Type "@"

Expected: Auto-complete shows:
- @reviewer
- @subagent-security
- @subagent-performance
- @subagent-improver
- @workspace (built-in)
- @terminal (built-in)
```

**Step 2: Review Bad Code**
```
Open: DEMO-FILES/BadAuthController.cs

In Copilot Chat:
"@reviewer please review BadAuthController.cs"

Expected output:
"Analyzing code... Invoking subagents for specialized review...

@subagent-security found:
🔴 CRITICAL: Hardcoded JWT secret on line 12
🔴 CRITICAL: No password hashing on line 28
🔴 HIGH: No rate limiting on login endpoint
🟡 MEDIUM: Missing [Authorize] attributes

@subagent-performance found:
🔴 HIGH: Synchronous database calls blocking threads
🟠 MEDIUM: No caching for frequently accessed data
🟡 LOW: String concatenation in loops

Consolidated recommendations:
[Detailed fixes with code examples...]"
```

**Step 3: Request Fixes**
```
In Copilot Chat:
"@reviewer please implement the security fixes"

Expected:
"I'll invoke @subagent-improver to implement these fixes...

@subagent-improver implementing:
✓ Moving JWT secret to configuration
✓ Adding password hashing with BCrypt
✓ Implementing rate limiting middleware
✓ Adding [Authorize] attributes

Changes ready for review."
```

### Demo: Creating a Custom Agent

**File**: `.github/agents/api-expert.agent.md`

```markdown
---
name: api-expert
description: REST API design expert for .NET
---

# API Design Expert

You are an expert in RESTful API design for .NET applications.

## Your Expertise

- REST principles and best practices
- HTTP status codes and semantics
- API versioning strategies
- OpenAPI/Swagger documentation
- Authentication and authorization
- Rate limiting and throttling
- API performance optimization

## Your Workflow

1. Analyze API endpoints for REST compliance
2. Check HTTP methods (GET, POST, PUT, DELETE, PATCH)
3. Verify proper status codes (200, 201, 400, 404, 500)
4. Review request/response models
5. Check for proper validation
6. Ensure consistent error handling
7. Verify API documentation

## Guidelines

When reviewing or creating APIs:

### Naming Conventions
- Use plural nouns: `/api/customers`, not `/api/customer`
- Use kebab-case for multi-word resources: `/api/customer-orders`
- Avoid verbs in URLs: use HTTP methods instead

### HTTP Methods
- GET: Retrieve resources (must be idempotent)
- POST: Create new resources
- PUT: Replace entire resource
- PATCH: Partially update resource
- DELETE: Remove resource

### Status Codes
- 200 OK: Successful GET, PUT, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE
- 400 Bad Request: Validation errors
- 401 Unauthorized: Missing/invalid auth
- 403 Forbidden: Authenticated but not authorized
- 404 Not Found: Resource doesn't exist
- 500 Internal Server Error: Server-side errors

### Response Format
```json
{
  "data": { /* resource or array */ },
  "metadata": {
    "timestamp": "2026-02-17T10:00:00Z",
    "version": "1.0"
  },
  "errors": [ /* if any */ ]
}
```

## Communication Style

- Explain the "why" behind recommendations
- Provide code examples
- Reference REST standards (RFC 7231, etc.)
- Be specific about improvements
```

**Testing the Agent**:
```
In Copilot Chat:
"@api-expert review the CustomersController endpoints"

Expected:
"Analyzing REST API design...

✓ Good: Using plural noun '/api/customers'
✓ Good: Proper HTTP methods (GET, POST, PATCH)
🟡 Suggestion: Consider using PUT for full updates
🟡 Suggestion: Add API versioning (e.g., /api/v1/customers)
🔴 Issue: Inconsistent status codes - CreateCustomer returns 200 instead of 201

Recommended changes: [detailed code examples...]"
```

## Part 2: Custom Instructions

### Repository-Level Instructions

**File**: `.github/copilot-instructions.md`

```markdown
# Creditro Demo - Copilot Instructions

## Project Context

This is a KYC (Know Your Customer) and AML (Anti-Money Laundering) compliance management system.

## Technologies

- Backend: .NET 10.0, ASP.NET Core
- Frontend: Angular 19+
- Database: In-memory (for demo purposes)

## Coding Standards

### General
- Follow SOLID principles
- Use dependency injection
- Write XML documentation for public APIs
- Include unit tests for new features

### .NET/C#
- Use async/await for I/O operations
- Prefer `System.Text.Json` over Newtonsoft.Json
- Use nullable reference types
- Follow Microsoft naming conventions

### API Design
- RESTful endpoints with proper HTTP methods
- Use Data Transfer Objects (DTOs)
- Include input validation with FluentValidation
- Return appropriate status codes

### Security
- Never hardcode secrets or API keys
- Use ASP.NET Core Identity for authentication
- Implement proper authorization with policies
- Validate and sanitize all user input
- Use parameterized queries (always)

## Domain-Specific Terms

- **KYC**: Know Your Customer - identity verification
- **AML**: Anti-Money Laundering - compliance checks
- **Risk Level**: Low, Medium, High - customer risk assessment
- **Compliance Check**: Verification step (Identity, Address, Business, Financial)
- **KYC Status**: Pending, In Progress, Completed, Rejected

## File Organization

```
backend/
  Controllers/      # API endpoints
  Services/         # Business logic
  Models/          # Domain models
  Interfaces/      # Abstractions
  Validators/      # Input validation
  Tests/           # Unit tests

frontend/
  components/      # Angular components
  services/        # HTTP services
  models/          # TypeScript interfaces
```

## Common Tasks

### Adding a New API Endpoint
1. Create/modify controller in Controllers/
2. Add service method in Services/
3. Create/update models in Models/
4. Add validation if needed
5. Create unit tests
6. Update OpenAPI/Swagger documentation

### Adding a New Feature
1. Design the feature (discuss if complex)
2. Update models and DTOs
3. Implement backend services and controllers
4. Add frontend components and services
5. Write tests (unit + integration)
6. Update documentation

## Testing Requirements

- Unit tests required for all service methods
- Test happy path and edge cases
- Use xUnit for .NET tests
- Use Jasmine/Karma for Angular tests
- Aim for 80%+ code coverage
```

**Demo Effect**:
```
In Copilot Chat (any mode):
"Add a new customer endpoint"

Copilot automatically:
- Uses .NET 10.0 syntax
- Follows repository structure
- Includes XML documentation
- Uses proper DTOs
- Adds validation
- Creates unit tests
- Follows REST principles
```

### Folder-Level Instructions

**File**: `.github/instructions/api.instructions.md`

```markdown
# API Development Instructions

When working on files in `backend/CreditroDemo.API/Controllers/`:

## Controller Standards

1. **Inheritance**: All controllers inherit from `ControllerBase`
2. **Routing**: Use `[Route("api/[controller]")]`
3. **Attributes**: Include `[ApiController]`
4. **HTTP Attributes**: Use `[HttpGet]`, `[HttpPost]`, etc.

## Method Structure

```csharp
/// <summary>
/// Brief description of what this endpoint does
/// </summary>
/// <param name="paramName">Parameter description</param>
/// <returns>Description of return value</returns>
/// <response code="200">Success description</response>
/// <response code="400">Error description</response>
[HttpGet("{id}")]
[ProducesResponseType(typeof(CustomerDto), StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<ActionResult<CustomerDto>> GetCustomer(int id)
{
    try
    {
        var customer = await _service.GetCustomerAsync(id);
        if (customer == null)
            return NotFound();

        return Ok(customer);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error retrieving customer {CustomerId}", id);
        return StatusCode(500, "An error occurred");
    }
}
```

## Required Elements

- [ ] XML documentation comments
- [ ] ProducesResponseType attributes
- [ ] Try-catch blocks with logging
- [ ] Async methods for I/O
- [ ] Proper status codes
- [ ] Input validation

## Error Handling

```csharp
return BadRequest(new { error = "Invalid input", details = ModelState });
return NotFound(new { error = "Customer not found" });
return StatusCode(500, new { error = "Internal server error" });
```

## Validation

```csharp
if (!ModelState.IsValid)
    return BadRequest(ModelState);

if (id <= 0)
    return BadRequest("Invalid customer ID");
```
```

**File**: `.github/instructions/database.instructions.md`

```markdown
# Database & Models Instructions

When working with data models and services:

## Model Design

### Domain Models
- Located in `Models/` directory
- Represent business entities
- Include navigation properties
- Use data annotations for validation

```csharp
public class Customer
{
    public int Id { get; set; }

    [Required, MaxLength(100)]
    public string FirstName { get; set; } = string.Empty;

    public RiskLevel RiskLevel { get; set; }

    // Navigation property
    public ICollection<ComplianceCheck> ComplianceChecks { get; set; } = new List<ComplianceCheck>();
}
```

### DTOs (Data Transfer Objects)
- Located in `Models/Dtos/` directory
- Used for API requests/responses
- Don't expose internal IDs or sensitive data
- Include only necessary fields

```csharp
public class CustomerDto
{
    public int Id { get; set; }
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string Phone { get; set; } = string.Empty;
    public string CompanyName { get; set; } = string.Empty;
    public KycStatus KycStatus { get; set; }
    public RiskLevel RiskLevel { get; set; }
}
```

## Service Layer

### Service Pattern
- One service per entity
- Interface + Implementation
- Async methods for data access

```csharp
public interface ICustomerService
{
    Task<IEnumerable<CustomerDto>> GetAllCustomersAsync();
    Task<CustomerDto?> GetCustomerByIdAsync(int id);
    Task<CustomerDto> CreateCustomerAsync(CreateCustomerDto dto);
    Task<bool> UpdateCustomerAsync(int id, UpdateCustomerDto dto);
    Task<bool> DeleteCustomerAsync(int id);
}
```

## Data Access Rules

1. **Always async**: Use `Task<T>` for database operations
2. **No raw SQL**: Use LINQ or Entity Framework methods
3. **Include error handling**: Try-catch with logging
4. **Use cancellation tokens**: For long-running operations
5. **Validate input**: Before database access

## Testing Data Models

```csharp
[Fact]
public void Customer_Validation_RequiresFirstName()
{
    var customer = new Customer { FirstName = "" };

    var context = new ValidationContext(customer);
    var results = new List<ValidationResult>();
    var isValid = Validator.TryValidateObject(customer, context, results, true);

    Assert.False(isValid);
    Assert.Contains(results, r => r.MemberNames.Contains(nameof(Customer.FirstName)));
}
```
```

**Demo Effect**:
```
In CustomersController.cs:
"Add a new endpoint to bulk import customers"

Copilot includes:
- [HttpPost("bulk")]
- [ProducesResponseType(...)]
- XML documentation
- Try-catch with logging
- Async method
- Validation
- Proper status codes

In CustomerService.cs:
"Add method to validate customer data"

Copilot includes:
- Async method with Task<T>
- Input validation
- Error handling
- Returns appropriate result
```

## Part 3: Agent Skills

### What are Agent Skills?
Reusable workflows that agents can invoke using slash commands.

### Demo: Using Existing Skill

**File**: `.github/skills/dotnet-api-testing/skill.md`

```
In Copilot Chat:
"/dotnet-api-testing for CustomersController"

Expected output:
"Generating comprehensive test suite for CustomersController...

Creating: CustomersControllerTests.cs

Test Cases Generated:
✓ GetAllCustomers_ReturnsOkResult_WithListOfCustomers
✓ GetAllCustomers_EmptyDatabase_ReturnsEmptyList
✓ GetCustomerById_ValidId_ReturnsOkResult
✓ GetCustomerById_InvalidId_ReturnsNotFound
✓ CreateCustomer_ValidData_ReturnsCreatedResult
✓ CreateCustomer_InvalidModel_ReturnsBadRequest
✓ CreateCustomer_DuplicateEmail_ReturnsConflict
✓ UpdateKycStatus_ValidId_ReturnsNoContent
✓ UpdateKycStatus_InvalidId_ReturnsNotFound
✓ UpdateKycStatus_InvalidStatus_ReturnsBadRequest
... [15 more tests]

All tests follow AAA pattern (Arrange, Act, Assert)
Using xUnit and Moq for mocking
100% coverage of public methods"
```

### Demo: Creating a Custom Skill

**File**: `.github/skills/api-documentation/skill.md`

```markdown
---
name: api-documentation
description: Generate comprehensive API documentation for controllers
---

# API Documentation Generator Skill

Generate complete API documentation including OpenAPI/Swagger annotations, README sections, and usage examples.

## Usage

```
/api-documentation for [ControllerName]
```

## Process

1. Analyze controller methods and their signatures
2. Generate XML documentation comments if missing
3. Add ProducesResponseType attributes
4. Create Swagger examples with SchemaFilter
5. Generate README.md section with:
   - Endpoint list
   - Request/response examples
   - cURL commands
   - Common use cases
6. Create Postman collection (optional)

## Output

### XML Documentation
```csharp
/// <summary>
/// Retrieves a customer by their unique identifier
/// </summary>
/// <param name="id">The unique customer identifier</param>
/// <returns>The customer details if found</returns>
/// <response code="200">Returns the customer details</response>
/// <response code="404">If the customer is not found</response>
/// <example>
/// GET /api/customers/123
/// </example>
```

### README Section
```markdown
## Customer API Endpoints

### Get All Customers
**GET** `/api/customers`

Returns a list of all customers in the system.

**Response**: 200 OK
```json
[
  {
    "id": 1,
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "kycStatus": "Completed"
  }
]
```

**cURL Example**:
```bash
curl -X GET "http://localhost:5000/api/customers" \
  -H "Authorization: Bearer YOUR_TOKEN"
```
```

### Testing the Skill
```
In Copilot Chat:
"/api-documentation for CustomersController"

Expected:
"Generating API documentation for CustomersController...

✓ Added XML comments to 8 methods
✓ Added ProducesResponseType attributes
✓ Created Swagger examples
✓ Generated README section (see API-DOCS.md)
✓ Created Postman collection (see postman/customers.json)

Documentation complete!"
```

### Demo: Skill with Parameters

**File**: `.github/skills/feature-scaffold/skill.md`

```markdown
---
name: feature-scaffold
description: Scaffold complete feature with controller, service, models, tests
parameters:
  - name: feature_name
    description: Name of the feature (e.g., AuditLog, Notification)
    required: true
  - name: include_tests
    description: Whether to generate test files
    required: false
    default: true
---

# Feature Scaffold Skill

Quickly scaffold a complete feature with all necessary files.

## Usage

```
/feature-scaffold feature_name=AuditLog include_tests=true
```

## Generated Structure

```
backend/CreditroDemo.API/
  Controllers/
    AuditLogController.cs         # RESTful controller
  Services/
    IAuditLogService.cs            # Interface
    AuditLogService.cs             # Implementation
  Models/
    AuditLog.cs                    # Domain model
    Dtos/
      AuditLogDto.cs               # Response DTO
      CreateAuditLogDto.cs         # Create DTO
  Tests/
    AuditLogControllerTests.cs     # Controller tests
    AuditLogServiceTests.cs        # Service tests
```

## Code Templates

Each file includes:
- Proper namespaces
- XML documentation
- Interface implementations
- Error handling
- Validation
- Logging
- Unit tests (if enabled)

## Example Output

```csharp
// Controllers/AuditLogController.cs
[ApiController]
[Route("api/[controller]")]
public class AuditLogController : ControllerBase
{
    private readonly IAuditLogService _service;
    private readonly ILogger<AuditLogController> _logger;

    public AuditLogController(
        IAuditLogService service,
        ILogger<AuditLogController> logger)
    {
        _service = service;
        _logger = logger;
    }

    /// <summary>
    /// Retrieves all audit log entries
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<AuditLogDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<AuditLogDto>>> GetAll()
    {
        // Implementation...
    }

    // ... more endpoints
}
```
```

## Hands-On Exercises

### Exercise 1: Create a Custom Agent (15 min)

**Task**: Create a "@database-expert" agent that helps with Entity Framework and database design.

**Steps**:
1. Create `.github/agents/database-expert.agent.md`
2. Define expertise (EF Core, migrations, indexing, performance)
3. Add workflow for analyzing models and queries
4. Test with: "@database-expert review the Customer model"

### Exercise 2: Add Folder Instructions (10 min)

**Task**: Create instructions for the frontend Angular code.

**Steps**:
1. Create `.github/instructions/frontend.instructions.md`
2. Define Angular best practices
3. Include component structure standards
4. Add service patterns
5. Test by editing a component

### Exercise 3: Create a Skill (20 min)

**Task**: Create a skill to generate integration tests.

**Steps**:
1. Create `.github/skills/integration-testing/skill.md`
2. Define skill name and description
3. Add workflow for generating integration tests
4. Include test templates
5. Test with: "/integration-testing for CustomersController"

## Discussion Questions

1. How would custom agents change your development workflow?
2. What agents would be most useful for your team?
3. How do folder-level instructions help with large codebases?
4. What skills would save you the most time?
5. How would you maintain and update these customizations?

## Best Practices

### Custom Agents
- Keep focused on one expertise area
- Include clear workflows
- Add subagents for specialized tasks
- Test thoroughly before rolling out

### Instructions
- Be specific and actionable
- Include code examples
- Update as standards evolve
- Keep security guidelines prominent

### Skills
- Make reusable and flexible
- Include parameter validation
- Provide clear usage examples
- Version your skill templates

## Resources

- Custom Agents Guide: https://docs.github.com/en/copilot/customizing-copilot/creating-custom-agents
- Copilot Instructions: https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
- Agent Skills: https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-agent-skills
