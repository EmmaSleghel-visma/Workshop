namespace CreditroDemo.API.Models;

public class CreateCustomerRequest
{
    public required string FullName { get; set; }
    public required string Email { get; set; }
    public string? PhoneNumber { get; set; }
    public required string CompanyName { get; set; }
    public string? BusinessNumber { get; set; }
    public required string Country { get; set; }
    public string? Address { get; set; }
}
