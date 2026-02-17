using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using CreditroDemo.API.Models;
using CreditroDemo.API.Services;

namespace CreditroDemo.API.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class CustomersController : ControllerBase
{
    private readonly ICustomerService _customerService;

    public CustomersController(ICustomerService customerService)
    {
        _customerService = customerService;
    }

    /// <summary>
    /// Returns all customers.
    /// </summary>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Ordered customer collection.</returns>
    [HttpGet]
    public async Task<ActionResult<List<Customer>>> GetAllCustomers(CancellationToken cancellationToken)
    {
        var customers = await _customerService.GetAllCustomersAsync(cancellationToken);
        return Ok(customers);
    }

    /// <summary>
    /// Returns a customer by id.
    /// </summary>
    /// <param name="id">Customer id.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Customer if found.</returns>
    [HttpGet("{id}")]
    public async Task<ActionResult<Customer>> GetCustomer(Guid id, CancellationToken cancellationToken)
    {
        var customer = await _customerService.GetCustomerByIdAsync(id, cancellationToken);
        if (customer == null)
        {
            return NotFound();
        }
        return Ok(customer);
    }

    /// <summary>
    /// Creates a new customer.
    /// </summary>
    /// <param name="request">Customer creation payload.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Created customer.</returns>
    [HttpPost]
    public async Task<ActionResult<Customer>> CreateCustomer([FromBody] CreateCustomerRequest request, CancellationToken cancellationToken)
    {
        if (!ModelState.IsValid)
        {
            return ValidationProblem(ModelState);
        }

        var customer = await _customerService.CreateCustomerAsync(request, cancellationToken);
        return CreatedAtAction(nameof(GetCustomer), new { id = customer.Id }, customer);
    }

    /// <summary>
    /// Updates the KYC status for a customer.
    /// </summary>
    /// <param name="id">Customer id.</param>
    /// <param name="status">Target KYC status.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Updated customer.</returns>
    [Authorize(Policy = "ComplianceWriter")]
    [HttpPatch("{id}/kyc-status")]
    public async Task<ActionResult<Customer>> UpdateKycStatus(Guid id, [FromBody] KycStatus status, CancellationToken cancellationToken)
    {
        var customer = await _customerService.UpdateCustomerKycStatusAsync(id, status, cancellationToken);
        if (customer == null)
        {
            return NotFound();
        }
        return Ok(customer);
    }

    /// <summary>
    /// Updates the risk level for a customer.
    /// </summary>
    /// <param name="id">Customer id.</param>
    /// <param name="riskLevel">Target risk level.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Updated customer.</returns>
    [Authorize(Policy = "ComplianceWriter")]
    [HttpPatch("{id}/risk-level")]
    public async Task<ActionResult<Customer>> UpdateRiskLevel(Guid id, [FromBody] RiskLevel riskLevel, CancellationToken cancellationToken)
    {
        var customer = await _customerService.UpdateCustomerRiskLevelAsync(id, riskLevel, cancellationToken);
        if (customer == null)
        {
            return NotFound();
        }
        return Ok(customer);
    }

    /// <summary>
    /// Adds a compliance check to a customer.
    /// </summary>
    /// <param name="id">Customer id.</param>
    /// <param name="request">Compliance check payload.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Updated customer.</returns>
    [Authorize(Policy = "ComplianceWriter")]
    [HttpPost("{id}/compliance-checks")]
    public async Task<ActionResult<Customer>> AddComplianceCheck(Guid id, [FromBody] AddComplianceCheckRequest request, CancellationToken cancellationToken)
    {
        if (!ModelState.IsValid)
        {
            return ValidationProblem(ModelState);
        }

        var customer = await _customerService.AddComplianceCheckAsync(id, request, cancellationToken);
        if (customer == null)
        {
            return NotFound();
        }
        return Ok(customer);
    }
}
