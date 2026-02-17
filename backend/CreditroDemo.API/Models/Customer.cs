namespace CreditroDemo.API.Models;

public class Customer
{
    public Guid Id { get; set; }
    public required string FullName { get; set; }
    public required string Email { get; set; }
    public string? PhoneNumber { get; set; }
    public required string CompanyName { get; set; }
    public string? BusinessNumber { get; set; }
    public required string Country { get; set; }
    public string? Address { get; set; }
    public DateTime CreatedAt { get; set; }
    public KycStatus KycStatus { get; set; }
    public RiskLevel RiskLevel { get; set; }
    public List<ComplianceCheck> ComplianceChecks { get; set; } = new();
}

public enum KycStatus
{
    Pending,
    InProgress,
    Completed,
    Rejected
}

public enum RiskLevel
{
    Low,
    Medium,
    High
}
