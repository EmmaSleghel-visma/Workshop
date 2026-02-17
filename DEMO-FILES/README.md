# Workshop Demo Files

This folder contains intentionally flawed code files for workshop demonstrations.

⚠️ **DO NOT USE THESE FILES IN PRODUCTION** ⚠️

## Purpose

These files contain intentional security vulnerabilities and performance issues to demonstrate:
- How Copilot subagents identify problems
- The effectiveness of code review agents
- Context control and proper usage patterns

## Demo Files

### 1. BadAuthController.cs
**Used in**: Demo 4 - Subagent Code Review (Security Focus)

**Intentional Issues**:
- 🔴 SQL Injection vulnerability (line 28)
- 🔴 Plain text password comparison (line 34)
- 🔴 Missing authorization on admin endpoint (line 42)
- 🔴 Hardcoded API secrets (line 54-55)
- 🔴 Open redirect vulnerability (line 68)
- 🔴 Information disclosure via stack traces (line 83-88)
- 🔴 Missing input validation (line 99-108)

**Demo Script**:
1. Open BadAuthController.cs
2. Use `@reviewer` agent to review the file
3. Watch as security subagent is automatically invoked
4. Receive comprehensive security analysis
5. Copilot suggests fixes for each issue

**Expected Output**:
- Security subagent should identify all 7 critical security issues
- Each issue should include:
  - Severity level
  - Location (file and line number)
  - Description of the vulnerability
  - Security risk explanation
  - Code example with fix

---

### 2. BadPerformanceService.cs
**Used in**: Demo 4 - Subagent Code Review (Performance Focus)

**Intentional Issues**:
- 🔴 N+1 Query Problem (lines 27-41)
- 🔴 Missing async/await blocking call (lines 47-54)
- 🔴 String concatenation in loop (lines 60-69)
- 🔴 No pagination for large datasets (lines 75-81)
- 🔴 Inefficient LINQ - loading all to memory (lines 87-96)
- 🔴 Multiple unnecessary database calls (lines 102-115)
- 🔴 O(n²) nested loop complexity (lines 121-135)
- 🔴 Undisposed resources/memory leak (lines 141-153)
- 🔴 No caching for expensive operations (lines 159-171)
- 🔴 Boxing/unboxing in tight loop (lines 177-185)

**Good Example Included**:
- Lines 191-204: Fixed version of GetOrderSummaries showing proper approach

**Demo Script**:
1. Open BadPerformanceService.cs
2. Use `@reviewer` agent to review the file
3. Watch as performance subagent is automatically invoked
4. Receive performance analysis with impact estimates
5. Compare with the "Fixed" version at the bottom

**Expected Output**:
- Performance subagent should identify all 10 performance issues
- Each issue should include:
  - Severity level
  - Time/space complexity analysis
  - Impact estimate (e.g., "10x slower")
  - Optimized code example

---

## How to Use These Files

### Setup

1. **DO NOT** add these files to your actual project
2. Keep them in this DEMO-FILES folder
3. Reference them during workshop demonstrations

### Demo 4: Subagent Code Review

**Part 1: Security Review (8 minutes)**

```
Step 1: Open BadAuthController.cs in VS Code

Step 2: In Copilot Chat, type:
@reviewer please review BadAuthController.cs for security issues

Step 3: Watch the workflow:
- Main reviewer agent analyzes the code
- Automatically invokes @subagent-security
- Security subagent runs in parallel (Jan 2026 feature!)
- Returns detailed security findings

Step 4: Review the output:
- Should find all 7 critical security issues
- Each with location, risk, and fix

Step 5: Ask for fixes:
"Please fix the SQL injection vulnerability"

Step 6: Compare before/after code
```

**Part 2: Performance Review (8 minutes)**

```
Step 1: Open BadPerformanceService.cs in VS Code

Step 2: In Copilot Chat, type:
@reviewer please review BadPerformanceService.cs for performance issues

Step 3: Watch the workflow:
- Main reviewer agent analyzes the code
- Automatically invokes @subagent-performance
- Performance subagent runs in parallel
- Returns performance analysis

Step 4: Review the output:
- Should find all 10 performance issues
- Impact estimates for each (e.g., "N+1 queries = 1000x more DB calls")

Step 5: Compare with fixed version:
Scroll to GetOrderSummaries_Fixed() method to see the proper implementation

Step 6: Ask for optimization:
"Please optimize the GetOrderSummaries method"
```

---

## Context Control Demo Files

For Demo 1 & 2 (Context Control), use the actual project files:

### Demo 1: Wrong Context → Wrong Code
**File**: `backend/CreditroDemo.API/Controllers/CustomersController.cs`

**Script**:
1. Close all open files
2. Start new chat (fresh context)
3. Ask: "Add logging to the CustomersController"
4. **Result**: Gets generic Console.WriteLine
5. **Why**: No context about your logging patterns

### Demo 2: Right Context → Right Code
**File**: `backend/CreditroDemo.API/Controllers/CustomersController.cs`

**Script**:
1. In chat, use #file to add:
   - CustomersController.cs
   - (Add your LoggingService.cs if it exists)
   - appsettings.json
2. Ask: "Add logging to the CustomersController using our logging standards"
3. **Result**: Perfect implementation following your patterns
4. **Why**: Explicit context provided

---

## Lab Exercise Files

During hands-on labs, participants will create:

### Lab 1: Multi-Agent Mastery
- Custom agent configurations in `.github/agents/`
- Their own subagent definitions
- Working tree configurations

### Lab 2: Copilot Workspace & Skills
- Custom skills in `.github/skills/`
- Personal skills in `~/.copilot/skills/`
- Test skill invocations

---

## Verification Checklist

Before workshop, verify:
- [ ] All demo files are in `DEMO-FILES/` folder only
- [ ] Demo files are NOT in actual project directories
- [ ] `.github/agents/reviewer.md` exists and is configured
- [ ] `.github/agents/subagent-security.md` exists with `infer: true`
- [ ] `.github/agents/subagent-performance.md` exists with `infer: true`
- [ ] Can invoke `@reviewer` agent in Copilot Chat
- [ ] Subagents are automatically triggered
- [ ] Parallel execution works (Jan 2026 feature)

---

## Troubleshooting

**Issue**: Subagents not being invoked
- **Fix**: Check `infer: true` is set in subagent .md files
- **Fix**: Ensure using `@reviewer` agent, not default Copilot

**Issue**: Security/performance issues not found
- **Fix**: Make sure files are open or referenced with #file
- **Fix**: Use explicit instruction: "check for security issues"

**Issue**: Parallel execution not working
- **Fix**: Ensure VS Code is updated to January 2026 or later
- **Fix**: Verify Copilot extension is latest version

---

## Clean Code Versions

After demonstrating the issues, show participants how to fix them:

### Fixed Security Example
```csharp
[HttpPost("login")]
[AllowAnonymous]
public async Task<IActionResult> Login([FromBody] LoginRequest request)
{
    // ✅ FIXED: Using parameterized query via Entity Framework
    var user = await _context.Users
        .FirstOrDefaultAsync(u => u.Username == request.Username);

    if (user == null)
        return Unauthorized();

    // ✅ FIXED: Using password hashing
    var passwordHash = _passwordHasher.HashPassword(user, request.Password);
    if (!_passwordHasher.VerifyHashedPassword(user, user.PasswordHash, request.Password))
        return Unauthorized();

    // ✅ Generate secure token
    var token = _tokenService.GenerateToken(user);

    return Ok(new { token });
}
```

### Fixed Performance Example
```csharp
public async Task<List<OrderSummary>> GetOrderSummaries(int page, int pageSize)
{
    // ✅ FIXED: Single query with eager loading and pagination
    return await _context.Orders
        .Include(o => o.Customer)
        .Include(o => o.Items)
        .OrderByDescending(o => o.CreatedAt)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .Select(o => new OrderSummary
        {
            OrderId = o.Id,
            CustomerName = o.Customer.Name,
            ItemCount = o.Items.Count,
            Total = o.Items.Sum(i => i.Price * i.Quantity)
        })
        .ToListAsync();
}
```

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [.NET Performance Best Practices](https://docs.microsoft.com/en-us/dotnet/framework/performance/performance-tips)
- [Entity Framework Performance](https://docs.microsoft.com/en-us/ef/core/performance/)
- [Secure Coding Guidelines](https://docs.microsoft.com/en-us/dotnet/standard/security/)

---

**Questions?**
Refer to Workshop_Plan_Ultimate.md for full demo scripts and timing.
