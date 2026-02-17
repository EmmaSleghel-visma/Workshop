using System.Collections.Concurrent;
using CreditroDemo.API.Models;

namespace CreditroDemo.API.Services;

public interface ICustomerService
{
    Task<List<Customer>> GetAllCustomersAsync();
    Task<Customer?> GetCustomerByIdAsync(Guid id);
    Task<Customer> CreateCustomerAsync(CreateCustomerRequest request);
    Task<Customer?> UpdateCustomerKycStatusAsync(Guid id, KycStatus status);
    Task<Customer?> UpdateCustomerRiskLevelAsync(Guid id, RiskLevel riskLevel);
    Task<Customer?> AddComplianceCheckAsync(Guid customerId, ComplianceCheck check);
}

public class CustomerService : ICustomerService
{
    private readonly ConcurrentBag<Customer> _customers = new();

    public CustomerService()
    {
        // Seed with some demo data
        SeedDemoData();
    }

    private void SeedDemoData()
    {
        var customer1 = new Customer
        {
            Id = Guid.NewGuid(),
            FullName = "John Anderson",
            Email = "john.anderson@techcorp.com",
            PhoneNumber = "+1-555-0101",
            CompanyName = "TechCorp Solutions",
            BusinessNumber = "12-3456789",
            Country = "United States",
            Address = "123 Tech Street, San Francisco, CA 94105",
            CreatedAt = DateTime.UtcNow.AddDays(-7),
            KycStatus = KycStatus.Completed,
            RiskLevel = RiskLevel.Low,
            ComplianceChecks = new List<ComplianceCheck>
            {
                new ComplianceCheck
                {
                    Id = Guid.NewGuid(),
                    CustomerId = Guid.Empty,
                    CheckType = "Identity Verification",
                    Status = CheckStatus.Passed,
                    Notes = "All documents verified",
                    CheckedAt = DateTime.UtcNow.AddDays(-6)
                },
                new ComplianceCheck
                {
                    Id = Guid.NewGuid(),
                    CustomerId = Guid.Empty,
                    CheckType = "AML Screening",
                    Status = CheckStatus.Passed,
                    Notes = "No matches found in watchlists",
                    CheckedAt = DateTime.UtcNow.AddDays(-6)
                }
            }
        };

        var customer2 = new Customer
        {
            Id = Guid.NewGuid(),
            FullName = "Maria Garcia",
            Email = "maria.garcia@financegroup.com",
            PhoneNumber = "+34-555-0202",
            CompanyName = "Finance Group Ltd",
            BusinessNumber = "ES-987654321",
            Country = "Spain",
            Address = "456 Finance Ave, Madrid, 28001",
            CreatedAt = DateTime.UtcNow.AddDays(-3),
            KycStatus = KycStatus.InProgress,
            RiskLevel = RiskLevel.Medium,
            ComplianceChecks = new List<ComplianceCheck>
            {
                new ComplianceCheck
                {
                    Id = Guid.NewGuid(),
                    CustomerId = Guid.Empty,
                    CheckType = "Identity Verification",
                    Status = CheckStatus.Passed,
                    Notes = "Documents verified",
                    CheckedAt = DateTime.UtcNow.AddDays(-2)
                },
                new ComplianceCheck
                {
                    Id = Guid.NewGuid(),
                    CustomerId = Guid.Empty,
                    CheckType = "Credit Assessment",
                    Status = CheckStatus.RequiresReview,
                    Notes = "Manual review required for credit history",
                    CheckedAt = DateTime.UtcNow.AddDays(-1)
                }
            }
        };

        var customer3 = new Customer
        {
            Id = Guid.NewGuid(),
            FullName = "Lars Nielsen",
            Email = "lars.nielsen@nordicbank.dk",
            PhoneNumber = "+45-555-0303",
            CompanyName = "Nordic Bank A/S",
            BusinessNumber = "DK-11223344",
            Country = "Denmark",
            Address = "789 Bank Street, Copenhagen, 1050",
            CreatedAt = DateTime.UtcNow.AddHours(-5),
            KycStatus = KycStatus.Pending,
            RiskLevel = RiskLevel.Low,
            ComplianceChecks = new List<ComplianceCheck>()
        };

        foreach (var customer in new[] { customer1, customer2, customer3 })
        {
            _customers.Add(customer);
        }
    }

    public Task<List<Customer>> GetAllCustomersAsync()
    {
        return Task.FromResult(_customers.OrderByDescending(c => c.CreatedAt).ToList());
    }

    public Task<Customer?> GetCustomerByIdAsync(Guid id)
    {
        var customer = _customers.FirstOrDefault(c => c.Id == id);
        return Task.FromResult(customer);
    }

    public Task<Customer> CreateCustomerAsync(CreateCustomerRequest request)
    {
        var customer = new Customer
        {
            Id = Guid.NewGuid(),
            FullName = request.FullName,
            Email = request.Email,
            PhoneNumber = request.PhoneNumber,
            CompanyName = request.CompanyName,
            BusinessNumber = request.BusinessNumber,
            Country = request.Country,
            Address = request.Address,
            CreatedAt = DateTime.UtcNow,
            KycStatus = KycStatus.Pending,
            RiskLevel = RiskLevel.Medium,
            ComplianceChecks = new List<ComplianceCheck>()
        };

        _customers.Add(customer);
        return Task.FromResult(customer);
    }

    public Task<Customer?> UpdateCustomerKycStatusAsync(Guid id, KycStatus status)
    {
        var customer = _customers.FirstOrDefault(c => c.Id == id);
        if (customer != null)
        {
            customer.KycStatus = status;
        }
        return Task.FromResult(customer);
    }

    public Task<Customer?> UpdateCustomerRiskLevelAsync(Guid id, RiskLevel riskLevel)
    {
        var customer = _customers.FirstOrDefault(c => c.Id == id);
        if (customer != null)
        {
            customer.RiskLevel = riskLevel;
        }
        return Task.FromResult(customer);
    }

    public Task<Customer?> AddComplianceCheckAsync(Guid customerId, ComplianceCheck check)
    {
        var customer = _customers.FirstOrDefault(c => c.Id == customerId);
        if (customer != null)
        {
            check.Id = Guid.NewGuid();
            check.CustomerId = customerId;
            check.CheckedAt = DateTime.UtcNow;
            customer.ComplianceChecks.Add(check);
        }
        return Task.FromResult(customer);
    }
}
