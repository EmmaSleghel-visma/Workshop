using Microsoft.AspNetCore.Mvc;
using System;
using System.Threading.Tasks;

namespace CreditroDemo.API.Controllers.Demo
{
    /// <summary>
    /// DEMO FILE: This file contains INTENTIONAL security vulnerabilities for Demo 4 (Subagent Code Review)
    /// DO NOT USE IN PRODUCTION!
    ///
    /// Purpose: Demonstrate how the security subagent identifies vulnerabilities
    /// </summary>
    [ApiController]
    [Route("api/[controller]")]
    public class BadAuthController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public BadAuthController(ApplicationDbContext context)
        {
            _context = context;
        }

        /// <summary>
        /// VULNERABLE: SQL Injection vulnerability
        /// </summary>
        [HttpPost("login")]
        public async Task<IActionResult> Login(string username, string password)
        {
            // ❌ CRITICAL SECURITY ISSUE: SQL Injection vulnerability!
            // String concatenation in SQL query allows attackers to inject malicious SQL
            var query = $"SELECT * FROM Users WHERE Username='{username}' AND Password='{password}'";

            var user = await _context.Database.ExecuteSqlRawAsync(query);

            if (user != null)
            {
                // ❌ SECURITY ISSUE: Plain text password comparison
                // Passwords should be hashed!
                return Ok(new { token = "jwt-token-here" });
            }

            return Unauthorized();
        }

        /// <summary>
        /// VULNERABLE: No authorization check
        /// </summary>
        [HttpGet("admin/users")]
        public async Task<IActionResult> GetAllUsers()
        {
            // ❌ SECURITY ISSUE: No [Authorize] attribute!
            // Anyone can access this admin endpoint
            var users = await _context.Users.ToListAsync();
            return Ok(users);
        }

        /// <summary>
        /// VULNERABLE: Exposed secrets
        /// </summary>
        [HttpPost("external-service")]
        public async Task<IActionResult> CallExternalService()
        {
            // ❌ SECURITY ISSUE: Hardcoded API key!
            // Secrets should be in environment variables or Key Vault
            var apiKey = "sk_live_123456789abcdef";
            var apiSecret = "secret_abc123def456";

            var client = new HttpClient();
            client.DefaultRequestHeaders.Add("X-API-Key", apiKey);

            // Make call...
            return Ok();
        }

        /// <summary>
        /// VULNERABLE: Open redirect
        /// </summary>
        [HttpGet("redirect")]
        public IActionResult RedirectToUrl(string url)
        {
            // ❌ SECURITY ISSUE: Open redirect vulnerability!
            // Attacker can redirect users to malicious sites
            return Redirect(url);
        }

        /// <summary>
        /// VULNERABLE: Information disclosure
        /// </summary>
        [HttpPost("process")]
        public async Task<IActionResult> ProcessData(string data)
        {
            try
            {
                // Some processing...
                throw new Exception("Database connection failed");
            }
            catch (Exception ex)
            {
                // ❌ SECURITY ISSUE: Exposing stack trace to client!
                // Attackers can learn about internal structure
                return StatusCode(500, new
                {
                    error = ex.Message,
                    stackTrace = ex.StackTrace,
                    source = ex.Source
                });
            }
        }

        /// <summary>
        /// VULNERABLE: Missing input validation
        /// </summary>
        [HttpPost("create-user")]
        public async Task<IActionResult> CreateUser(string email, string role)
        {
            // ❌ SECURITY ISSUE: No input validation!
            // Attacker could inject XSS, set admin role, etc.
            var user = new User
            {
                Email = email,  // Could contain XSS payload
                Role = role     // Could be "Admin" without authorization
            };

            await _context.Users.AddAsync(user);
            await _context.SaveChangesAsync();

            return Ok(user);
        }
    }
}
