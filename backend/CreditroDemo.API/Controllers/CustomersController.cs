using Microsoft.AspNetCore.Mvc;
using CreditroDemo.API.Models;
using CreditroDemo.API.Services;

namespace CreditroDemo.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class CustomersController : ControllerBase
{
    private readonly ICustomerService _customerService;

    public CustomersController(ICustomerService customerService)
    {
        _customerService = customerService;
    }

    [HttpGet]
    public async Task<ActionResult<List<Customer>>> GetAllCustomers()
    {
        var customers = await _customerService.GetAllCustomersAsync();
        return Ok(customers);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<Customer>> GetCustomer(Guid id)
    {
        var customer = await _customerService.GetCustomerByIdAsync(id);
        if (customer == null)
        {
            return NotFound();
        }
        return Ok(customer);
    }

    [HttpPost]
    public async Task<ActionResult<Customer>> CreateCustomer(CreateCustomerRequest request)
    {
        var customer = await _customerService.CreateCustomerAsync(request);
        return CreatedAtAction(nameof(GetCustomer), new { id = customer.Id }, customer);
    }

    [HttpPatch("{id}/kyc-status")]
    public async Task<ActionResult<Customer>> UpdateKycStatus(Guid id, [FromBody] KycStatus status)
    {
        var customer = await _customerService.UpdateCustomerKycStatusAsync(id, status);
        if (customer == null)
        {
            return NotFound();
        }
        return Ok(customer);
    }

    [HttpPatch("{id}/risk-level")]
    public async Task<ActionResult<Customer>> UpdateRiskLevel(Guid id, [FromBody] RiskLevel riskLevel)
    {
        var customer = await _customerService.UpdateCustomerRiskLevelAsync(id, riskLevel);
        if (customer == null)
        {
            return NotFound();
        }
        return Ok(customer);
    }

    [HttpPost("{id}/compliance-checks")]
    public async Task<ActionResult<Customer>> AddComplianceCheck(Guid id, [FromBody] ComplianceCheck check)
    {
        var customer = await _customerService.AddComplianceCheckAsync(id, check);
        if (customer == null)
        {
            return NotFound();
        }
        return Ok(customer);
    }
}
