using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;

namespace CreditroDemo.API.Services.Demo
{
    /// <summary>
    /// DEMO FILE: This file contains INTENTIONAL performance issues for Demo 4 (Subagent Code Review)
    /// DO NOT USE IN PRODUCTION!
    ///
    /// Purpose: Demonstrate how the performance subagent identifies bottlenecks
    /// </summary>
    public class BadPerformanceService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<BadPerformanceService> _logger;

        public BadPerformanceService(ApplicationDbContext context, ILogger<BadPerformanceService> logger)
        {
            _context = context;
            _logger = logger;
        }

        /// <summary>
        /// PERFORMANCE ISSUE: N+1 Query Problem
        /// </summary>
        public async Task<List<OrderSummary>> GetOrderSummaries()
        {
            // ❌ PERFORMANCE ISSUE: N+1 queries!
            // For 1000 orders, this creates 1000+ database queries
            var orders = await _context.Orders.ToListAsync();

            var summaries = new List<OrderSummary>();
            foreach (var order in orders)
            {
                // Each iteration makes a separate database call!
                var customer = await _context.Customers.FindAsync(order.CustomerId);
                var items = await _context.OrderItems.Where(i => i.OrderId == order.Id).ToListAsync();

                summaries.Add(new OrderSummary
                {
                    OrderId = order.Id,
                    CustomerName = customer.Name,
                    ItemCount = items.Count,
                    Total = items.Sum(i => i.Price * i.Quantity)
                });
            }

            return summaries;
        }

        /// <summary>
        /// PERFORMANCE ISSUE: Missing async/await
        /// </summary>
        public List<Customer> GetActiveCustomers()
        {
            // ❌ PERFORMANCE ISSUE: Blocking synchronous call!
            // This blocks the thread instead of awaiting
            return _context.Customers
                .Where(c => c.IsActive)
                .ToList();  // Should be ToListAsync()
        }

        /// <summary>
        /// PERFORMANCE ISSUE: String concatenation in loop
        /// </summary>
        public string GenerateReport(List<Order> orders)
        {
            // ❌ PERFORMANCE ISSUE: String concatenation in loop!
            // Creates a new string object on each iteration
            string report = "";
            foreach (var order in orders)
            {
                report += $"Order {order.Id}: ${order.Total}\n";  // Very inefficient!
            }
            return report;
        }

        /// <summary>
        /// PERFORMANCE ISSUE: No pagination
        /// </summary>
        public async Task<List<Customer>> GetAllCustomers()
        {
            // ❌ PERFORMANCE ISSUE: Loading ALL records without pagination!
            // With 1 million customers, this loads everything into memory
            return await _context.Customers.ToListAsync();
        }

        /// <summary>
        /// PERFORMANCE ISSUE: Inefficient LINQ
        /// </summary>
        public async Task<List<Customer>> SearchCustomers(string searchTerm)
        {
            // ❌ PERFORMANCE ISSUE: Inefficient query pattern!
            // Loads all customers into memory THEN filters
            var allCustomers = await _context.Customers.ToListAsync();

            return allCustomers
                .Where(c => c.Name.Contains(searchTerm))  // In-memory filtering!
                .ToList();
        }

        /// <summary>
        /// PERFORMANCE ISSUE: Multiple database calls
        /// </summary>
        public async Task<CustomerDetails> GetCustomerDetails(Guid customerId)
        {
            // ❌ PERFORMANCE ISSUE: Multiple separate database calls!
            // Should use single query with Include()
            var customer = await _context.Customers.FindAsync(customerId);
            var orders = await _context.Orders.Where(o => o.CustomerId == customerId).ToListAsync();
            var complianceChecks = await _context.ComplianceChecks.Where(c => c.CustomerId == customerId).ToListAsync();

            return new CustomerDetails
            {
                Customer = customer,
                Orders = orders,
                ComplianceChecks = complianceChecks
            };
        }

        /// <summary>
        /// PERFORMANCE ISSUE: Inefficient collection operation
        /// </summary>
        public List<Order> FilterOrdersByStatus(List<Order> orders, string status)
        {
            // ❌ PERFORMANCE ISSUE: O(n²) complexity!
            // Nested loops create quadratic time complexity
            var result = new List<Order>();
            foreach (var order in orders)
            {
                foreach (var otherOrder in orders)
                {
                    if (otherOrder.Status == status && order.Id == otherOrder.Id)
                    {
                        result.Add(order);
                        break;
                    }
                }
            }
            return result;
        }

        /// <summary>
        /// PERFORMANCE ISSUE: Undisposed resources
        /// </summary>
        public async Task ProcessLargeFile(string filePath)
        {
            // ❌ PERFORMANCE ISSUE: FileStream not disposed!
            // Memory leak - resources not released
            var stream = new FileStream(filePath, FileMode.Open);
            var reader = new StreamReader(stream);

            var content = await reader.ReadToEndAsync();

            // Processing...

            // Missing: stream.Dispose() and reader.Dispose()
        }

        /// <summary>
        /// PERFORMANCE ISSUE: No caching for expensive operation
        /// </summary>
        public async Task<List<ComplianceRule>> GetComplianceRules()
        {
            // ❌ PERFORMANCE ISSUE: Expensive calculation repeated on every call!
            // This should be cached as rules rarely change
            _logger.LogInformation("Calculating compliance rules (expensive operation)...");

            await Task.Delay(2000);  // Simulates expensive operation

            return await _context.ComplianceRules
                .Include(r => r.Conditions)
                .Include(r => r.Actions)
                .ToListAsync();
        }

        /// <summary>
        /// PERFORMANCE ISSUE: Boxing in tight loop
        /// </summary>
        public void ProcessNumbers(List<int> numbers)
        {
            // ❌ PERFORMANCE ISSUE: Boxing value types in loop!
            // Each Add causes boxing allocation
            var list = new ArrayList();  // Non-generic collection
            foreach (var number in numbers)
            {
                list.Add(number);  // Boxing int to object
            }
        }

        /// <summary>
        /// GOOD EXAMPLE: Fixed version of GetOrderSummaries
        /// </summary>
        public async Task<List<OrderSummary>> GetOrderSummaries_Fixed()
        {
            // ✅ FIXED: Single query with eager loading
            return await _context.Orders
                .Include(o => o.Customer)
                .Include(o => o.Items)
                .Select(o => new OrderSummary
                {
                    OrderId = o.Id,
                    CustomerName = o.Customer.Name,
                    ItemCount = o.Items.Count,
                    Total = o.Items.Sum(i => i.Price * i.Quantity)
                })
                .ToListAsync();
        }
    }

    #region Supporting Classes

    public class OrderSummary
    {
        public Guid OrderId { get; set; }
        public string CustomerName { get; set; }
        public int ItemCount { get; set; }
        public decimal Total { get; set; }
    }

    public class CustomerDetails
    {
        public Customer Customer { get; set; }
        public List<Order> Orders { get; set; }
        public List<ComplianceCheck> ComplianceChecks { get; set; }
    }

    #endregion
}
