using System.ComponentModel.DataAnnotations;

namespace CreditroDemo.API.Models;

public class CreateCustomerRequest
{
    [Required]
    [MaxLength(150)]
    public required string FullName { get; set; }

    [Required]
    [EmailAddress]
    [MaxLength(200)]
    public required string Email { get; set; }

    [Phone]
    [MaxLength(30)]
    public string? PhoneNumber { get; set; }

    [Required]
    [MaxLength(200)]
    public required string CompanyName { get; set; }

    [MaxLength(100)]
    public string? BusinessNumber { get; set; }

    [Required]
    [MaxLength(100)]
    public required string Country { get; set; }

    [MaxLength(300)]
    public string? Address { get; set; }
}

public class AddComplianceCheckRequest
{
    [Required]
    [MaxLength(100)]
    public required string CheckType { get; set; }

    [Required]
    public CheckStatus Status { get; set; }

    [MaxLength(500)]
    public string? Notes { get; set; }
}
