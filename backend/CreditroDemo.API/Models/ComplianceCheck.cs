namespace CreditroDemo.API.Models;

public class ComplianceCheck
{
    public Guid Id { get; set; }
    public Guid CustomerId { get; set; }
    public required string CheckType { get; set; }
    public CheckStatus Status { get; set; }
    public string? Notes { get; set; }
    public DateTime CheckedAt { get; set; }
}

public enum CheckStatus
{
    Pending,
    Passed,
    Failed,
    RequiresReview
}
