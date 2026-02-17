using System.Collections.Concurrent;
using CreditroDemo.API.Models;
using Microsoft.Extensions.Logging;

namespace CreditroDemo.API.Services;

public interface ICustomerService
{
    Task<List<Customer>> GetAllCustomersAsync(CancellationToken cancellationToken);
    Task<Customer?> GetCustomerByIdAsync(Guid id, CancellationToken cancellationToken);
    Task<Customer> CreateCustomerAsync(CreateCustomerRequest request, CancellationToken cancellationToken);
    Task<Customer?> UpdateCustomerKycStatusAsync(Guid id, KycStatus status, CancellationToken cancellationToken);
    Task<Customer?> UpdateCustomerRiskLevelAsync(Guid id, RiskLevel riskLevel, CancellationToken cancellationToken);
    Task<Customer?> AddComplianceCheckAsync(Guid customerId, AddComplianceCheckRequest request, CancellationToken cancellationToken);
}

public class CustomerService : ICustomerService
{
    private readonly ConcurrentDictionary<Guid, Customer> _customers = new();
    private readonly ILogger<CustomerService> _logger;

    public CustomerService(ILogger<CustomerService> logger)
    {
        _logger = logger;
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
            _customers.TryAdd(customer.Id, customer);
        }
    }

    /// <summary>
    /// Returns all customers ordered by creation date descending.
    /// </summary>
    public Task<List<Customer>> GetAllCustomersAsync(CancellationToken cancellationToken)
    {
        try
        {
            cancellationToken.ThrowIfCancellationRequested();
            var customers = _customers.Values
                .OrderByDescending(c => c.CreatedAt)
                .ToList();

            return Task.FromResult(customers);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error while retrieving customers.");
            throw;
        }
    }

    /// <summary>
    /// Returns a customer by identifier.
    /// </summary>
    public Task<Customer?> GetCustomerByIdAsync(Guid id, CancellationToken cancellationToken)
    {
        try
        {
            cancellationToken.ThrowIfCancellationRequested();
            _customers.TryGetValue(id, out var customer);
            return Task.FromResult(customer);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error while retrieving customer {CustomerId}.", id);
            throw;
        }
    }

    /// <summary>
    /// Creates a new customer.
    /// </summary>
    public Task<Customer> CreateCustomerAsync(CreateCustomerRequest request, CancellationToken cancellationToken)
    {
        try
        {
            cancellationToken.ThrowIfCancellationRequested();

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

            _customers.TryAdd(customer.Id, customer);
            _logger.LogInformation("Created customer {CustomerId} with email {Email}", customer.Id, customer.Email);
            return Task.FromResult(customer);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error while creating customer {Email}.", request.Email);
            throw;
        }
    }

    /// <summary>
    /// Updates customer KYC status.
    /// </summary>
    public Task<Customer?> UpdateCustomerKycStatusAsync(Guid id, KycStatus status, CancellationToken cancellationToken)
    {
        try
        {
            cancellationToken.ThrowIfCancellationRequested();

            if (!_customers.TryGetValue(id, out var customer))
            {
                return Task.FromResult<Customer?>(null);
            }

            customer.KycStatus = status;
            _logger.LogInformation("Updated KYC status for customer {CustomerId} to {Status}", id, status);
            return Task.FromResult<Customer?>(customer);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error while updating KYC status for customer {CustomerId}.", id);
            throw;
        }
    }

    /// <summary>
    /// Updates customer risk level.
    /// </summary>
    public Task<Customer?> UpdateCustomerRiskLevelAsync(Guid id, RiskLevel riskLevel, CancellationToken cancellationToken)
    {
        try
        {
            cancellationToken.ThrowIfCancellationRequested();

            if (!_customers.TryGetValue(id, out var customer))
            {
                return Task.FromResult<Customer?>(null);
            }

            customer.RiskLevel = riskLevel;
            _logger.LogInformation("Updated risk level for customer {CustomerId} to {RiskLevel}", id, riskLevel);
            return Task.FromResult<Customer?>(customer);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error while updating risk level for customer {CustomerId}.", id);
            throw;
        }
    }

    /// <summary>
    /// Adds a compliance check for a customer.
    /// </summary>
    public Task<Customer?> AddComplianceCheckAsync(Guid customerId, AddComplianceCheckRequest request, CancellationToken cancellationToken)
    {
        try
        {
            cancellationToken.ThrowIfCancellationRequested();

            if (!_customers.TryGetValue(customerId, out var customer))
            {
                return Task.FromResult<Customer?>(null);
            }

            var check = new ComplianceCheck
            {
                Id = Guid.NewGuid(),
                CustomerId = customerId,
                CheckType = request.CheckType,
                Status = request.Status,
                Notes = request.Notes,
                CheckedAt = DateTime.UtcNow
            };

            lock (customer.ComplianceChecks)
            {
                customer.ComplianceChecks.Add(check);
            }

            _logger.LogInformation("Added compliance check {CheckType} for customer {CustomerId}", request.CheckType, customerId);
            return Task.FromResult<Customer?>(customer);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error while adding compliance check for customer {CustomerId}.", customerId);
            throw;
        }
    }
}
