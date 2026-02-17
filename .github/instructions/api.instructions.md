---
paths:
  - 'backend/**/*.cs'
  - 'backend/CreditroDemo.API/Controllers/**'
  - 'backend/CreditroDemo.API/Services/**'
---

# API Development Instructions

## Project Context

This is the Creditro Demo API - a .NET 8 Web API for credit and compliance management.

## Coding Standards

### Controllers
- Always use async/await for all operations
- Return appropriate HTTP status codes (200, 201, 400, 404, 500)
- Use `[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpDelete]` attributes
- Add XML documentation comments for all public methods
- Use model validation with `[Required]`, `[MaxLength]`, etc.

Example:
```csharp
/// <summary>
/// Creates a new customer
/// </summary>
/// <param name="request">Customer creation request</param>
/// <returns>Created customer</returns>
[HttpPost]
public async Task<ActionResult<Customer>> CreateCustomer([FromBody] CreateCustomerRequest request)
{
    if (!ModelState.IsValid)
        return BadRequest(ModelState);

    var customer = await _customerService.CreateAsync(request);
    return CreatedAtAction(nameof(GetCustomer), new { id = customer.Id }, customer);
}
```

### Services
- Inject dependencies via constructor
- Use interface-based design (`ICustomerService`)
- Always use async/await
- Proper error handling with try-catch
- Log important operations

Example:
```csharp
public class CustomerService : ICustomerService
{
    private readonly ILogger<CustomerService> _logger;
    private readonly ApplicationDbContext _context;

    public CustomerService(ILogger<CustomerService> logger, ApplicationDbContext context)
    {
        _logger = logger;
        _context = context;
    }

    public async Task<Customer> CreateAsync(CreateCustomerRequest request)
    {
        try
        {
            _logger.LogInformation("Creating customer: {Email}", request.Email);
            // Implementation
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error creating customer");
            throw;
        }
    }
}
```

### Error Handling
- Use try-catch in service methods
- Log errors with structured logging
- Return appropriate error responses
- Never expose internal error details to clients

### Logging
- Use ILogger<T> for structured logging
- Log levels:
  - Information: Business operations
  - Warning: Recoverable issues
  - Error: Exceptions and failures
- Include correlation IDs for tracking

## Security Requirements
- All endpoints require authentication (unless explicitly public)
- Use [Authorize] attribute on controllers
- Validate all input data
- Never log sensitive information (passwords, tokens)
- Use HTTPS for all communications

## Performance Guidelines
- Use async/await throughout
- Avoid N+1 query problems (use Include for related data)
- Implement pagination for list endpoints
- Use caching where appropriate
- Optimize database queries

## Testing
- Write unit tests for all services
- Use xUnit as the testing framework
- Mock dependencies with Moq
- Aim for >80% code coverage
