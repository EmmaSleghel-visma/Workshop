---
name: dotnet-api-testing
description: Generate comprehensive API tests for .NET controllers and services
---

# .NET API Testing Skill

Generate complete test suites for .NET Web API controllers and services.

## What This Skill Does

When invoked, this skill generates:
1. **Unit tests** for controller actions
2. **Integration tests** for API endpoints
3. **Mock setup** for dependencies
4. **Test data builders** for models
5. **Assertion helpers** using FluentAssertions

## Usage

```
/dotnet-api-testing for CustomersController
/dotnet-api-testing create tests for the CustomerService
```

## Testing Framework

- **Framework**: xUnit
- **Mocking**: Moq
- **Assertions**: FluentAssertions
- **HTTP Testing**: Microsoft.AspNetCore.Mvc.Testing

## Test Structure

### Unit Test Template

```csharp
using Xunit;
using Moq;
using FluentAssertions;
using Microsoft.Extensions.Logging;

public class [ClassName]Tests
{
    private readonly Mock<IDependency> _mockDependency;
    private readonly Mock<ILogger<ClassUnderTest>> _mockLogger;
    private readonly ClassUnderTest _sut; // System Under Test

    public [ClassName]Tests()
    {
        _mockDependency = new Mock<IDependency>();
        _mockLogger = new Mock<ILogger<ClassUnderTest>>();
        _sut = new ClassUnderTest(_mockDependency.Object, _mockLogger.Object);
    }

    [Fact]
    public async Task MethodName_GivenScenario_ExpectedResult()
    {
        // Arrange
        var input = new InputModel { /* ... */ };
        _mockDependency
            .Setup(x => x.MethodAsync(It.IsAny<string>()))
            .ReturnsAsync(expectedValue);

        // Act
        var result = await _sut.MethodAsync(input);

        // Assert
        result.Should().NotBeNull();
        result.Property.Should().Be(expectedValue);
        _mockDependency.Verify(x => x.MethodAsync(It.IsAny<string>()), Times.Once);
    }

    [Theory]
    [InlineData("value1", true)]
    [InlineData("value2", false)]
    public async Task MethodName_MultipleScenarios(string input, bool expected)
    {
        // Arrange & Act
        var result = await _sut.MethodAsync(input);

        // Assert
        result.Should().Be(expected);
    }
}
```

### Controller Test Template

```csharp
public class [Controller]Tests
{
    private readonly Mock<IService> _mockService;
    private readonly [Controller] _controller;

    public [Controller]Tests()
    {
        _mockService = new Mock<IService>();
        _controller = new [Controller](_mockService.Object);
    }

    [Fact]
    public async Task GetAction_ReturnsOkResult_WithData()
    {
        // Arrange
        var expectedData = new List<Model> { /* test data */ };
        _mockService
            .Setup(x => x.GetAllAsync())
            .ReturnsAsync(expectedData);

        // Act
        var result = await _controller.GetAll();

        // Assert
        var okResult = result.Result.Should().BeOfType<OkObjectResult>().Subject;
        var returnedData = okResult.Value.Should().BeAssignableTo<List<Model>>().Subject;
        returnedData.Should().HaveCount(expectedData.Count);
    }

    [Fact]
    public async Task PostAction_InvalidModel_ReturnsBadRequest()
    {
        // Arrange
        _controller.ModelState.AddModelError("Property", "Error message");
        var request = new CreateRequest { /* ... */ };

        // Act
        var result = await _controller.Create(request);

        // Assert
        result.Result.Should().BeOfType<BadRequestObjectResult>();
    }

    [Fact]
    public async Task GetById_NonExistentId_ReturnsNotFound()
    {
        // Arrange
        var id = Guid.NewGuid();
        _mockService
            .Setup(x => x.GetByIdAsync(id))
            .ReturnsAsync((Model?)null);

        // Act
        var result = await _controller.GetById(id);

        // Assert
        result.Result.Should().BeOfType<NotFoundResult>();
    }
}
```

## Test Scenarios to Cover

### Happy Path
- ✅ Valid input returns expected result
- ✅ Successful creation returns 201 Created
- ✅ Successful update returns 200 OK
- ✅ Successful delete returns 204 No Content

### Edge Cases
- ⚠️ Null or empty input
- ⚠️ Invalid IDs (non-existent, wrong format)
- ⚠️ Boundary values (max length, min/max numbers)
- ⚠️ Duplicate entries

### Error Cases
- ❌ Invalid model state returns 400 Bad Request
- ❌ Not found returns 404
- ❌ Server errors return 500
- ❌ Exceptions are logged

### Authorization
- 🔐 Unauthorized access returns 401
- 🔐 Forbidden access returns 403

## Test Data Builders

Create builder classes for complex test data:

```csharp
public class CustomerBuilder
{
    private Guid _id = Guid.NewGuid();
    private string _name = "Test Customer";
    private string _email = "test@example.com";

    public CustomerBuilder WithId(Guid id)
    {
        _id = id;
        return this;
    }

    public CustomerBuilder WithName(string name)
    {
        _name = name;
        return this;
    }

    public CustomerBuilder WithEmail(string email)
    {
        _email = email;
        return this;
    }

    public Customer Build() => new Customer
    {
        Id = _id,
        Name = _name,
        Email = _email,
        CreatedAt = DateTime.UtcNow
    };
}

// Usage in tests
var customer = new CustomerBuilder()
    .WithName("John Doe")
    .WithEmail("john@example.com")
    .Build();
```

## Integration Test Setup

```csharp
public class CustomersControllerIntegrationTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly HttpClient _client;

    public CustomersControllerIntegrationTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetCustomers_ReturnsSuccessStatusCode()
    {
        // Act
        var response = await _client.GetAsync("/api/customers");

        // Assert
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        content.Should().NotBeEmpty();
    }
}
```

## Best Practices

1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **One assertion per test** (when possible)
3. **Clear test names**: MethodName_Scenario_ExpectedResult
4. **Use FluentAssertions** for readable assertions
5. **Mock all external dependencies**
6. **Test both success and failure paths**
7. **Use [Theory] for multiple similar tests**
8. **Clean up resources** in Dispose() if needed

## Running Tests

```bash
# Run all tests
dotnet test

# Run tests with coverage
dotnet test /p:CollectCoverage=true

# Run specific test class
dotnet test --filter FullyQualifiedName~CustomersControllerTests

# Run tests in watch mode
dotnet watch test
```
