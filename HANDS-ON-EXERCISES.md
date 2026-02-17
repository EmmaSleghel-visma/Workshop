# Hands-On Exercises - GitHub Copilot Workshop

## Overview
This document contains all hands-on exercises for the workshop. Each exercise includes objectives, step-by-step instructions, expected outcomes, and discussion points.

---

## Exercise 1: Context Control & File Linking (20 min)

### Objective
Master the art of providing the right context to Copilot for better suggestions.

### Background
Copilot's quality depends on context. The 4 sources of context are:
1. Currently open files in editor
2. Files explicitly linked with #file
3. Repository instructions (.github/copilot-instructions.md)
4. Workspace-wide knowledge (@workspace)

### Task
Improve Copilot's suggestions by providing better context.

### Steps

**Step 1: Poor Context Example**
```
1. Close all open files in VS Code
2. Open a new file: "NewFeature.cs"
3. In Copilot Chat: "Add a method to get customers by email"

Result: Generic code without knowledge of your project structure
```

**Step 2: Better Context with File Linking**
```
1. In Copilot Chat:
   "#file:Models/Customer.cs #file:Services/CustomerService.cs
    Add a method to get customers by email"

Result: Code that uses your actual Customer model and follows your service patterns
```

**Step 3: Best Context with @workspace**
```
1. In Copilot Chat:
   "@workspace Add a method to CustomerService to get customers by email.
    Follow the existing patterns in the service."

Result: Perfectly integrated code following all your conventions
```

### Expected Outcomes
- Understand how context affects suggestions
- Learn to use #file for specific references
- Master @workspace for codebase-wide understanding

### Discussion
- When would you use #file vs @workspace?
- What happens if you provide too much context?
- How can you verify Copilot understood your context?

---

## Exercise 2: MCP Server Setup (30 min)

### Objective
Connect GitHub Copilot to external tools using Model Context Protocol.

### Prerequisites
- GitHub CLI installed and authenticated (`gh auth status`)
- Node.js and npm installed

### Task
Set up GitHub MCP server and use it to interact with your repository.

### Steps

**Step 1: Create MCP Configuration**
```
1. In VS Code, create: `.vscode/mcp.json`
2. Add this configuration:

{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}

3. Save the file
4. Reload VS Code (F1 → "Developer: Reload Window")
```

**Step 2: Verify Connection**
```
1. Open Copilot Chat
2. Type: "Are you connected to any MCP servers?"
3. Copilot should confirm GitHub MCP is connected
```

**Step 3: Query Issues**
```
1. In Copilot Chat:
   "What issues are currently open in this repository?"

2. Expected: List of open issues with titles and numbers
```

**Step 4: Create an Issue**
```
1. In Copilot Chat:
   "Create a new issue titled 'Add email validation' with label 'enhancement'"

2. Verify: Go to GitHub → Issues → See the new issue
```

**Step 5: Query Pull Requests**
```
1. In Copilot Chat:
   "Summarize all open pull requests"

2. Expected: Summary of each PR with status
```

### Expected Outcomes
- MCP server successfully connected
- Ability to query repository data
- Ability to create issues via Copilot

### Troubleshooting
- If connection fails, check GitHub token: `echo $GITHUB_TOKEN`
- Check MCP logs: VS Code Output → MCP Server Logs
- Verify npm package: `npx -y @modelcontextprotocol/server-github --version`

### Discussion
- What other MCP servers would be useful?
- How does this change your workflow?
- What are the security implications?

---

## Exercise 3: Custom Agent Creation (25 min)

### Objective
Create a custom agent tailored to your team's needs.

### Task
Create a "@security-reviewer" agent that focuses on security best practices.

### Steps

**Step 1: Create Agent File**
```
1. Create: `.github/agents/security-reviewer.agent.md`
2. Add this content:

---
name: security-reviewer
description: Security-focused code reviewer
---

# Security Reviewer Agent

You are a security expert specializing in .NET application security.

## Your Focus Areas

- Authentication and authorization
- Input validation and sanitization
- SQL injection prevention
- XSS (Cross-Site Scripting) prevention
- Secrets management
- Cryptography and hashing
- API security

## Review Checklist

When reviewing code, check for:

### Authentication
- [ ] No hardcoded credentials
- [ ] Proper use of Identity framework
- [ ] JWT tokens properly validated
- [ ] Session management secure

### Authorization
- [ ] [Authorize] attributes on endpoints
- [ ] Policy-based authorization used
- [ ] Least privilege principle
- [ ] No authorization bypass

### Input Validation
- [ ] All user input validated
- [ ] Parameterized queries used
- [ ] No eval() or similar dangerous functions
- [ ] File upload restrictions

### Data Protection
- [ ] Passwords properly hashed (BCrypt/PBKDF2)
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS enforced
- [ ] No sensitive data in logs

## Communication Style

- Mark critical issues with 🔴 CRITICAL
- Mark high priority with 🔴 HIGH
- Mark medium priority with 🟡 MEDIUM
- Provide specific remediation steps
- Include code examples for fixes

3. Save and close
```

**Step 2: Test the Agent**
```
1. Open: DEMO-FILES/BadAuthController.cs
2. In Copilot Chat:
   "@security-reviewer review this authentication controller"

3. Expected: Detailed security analysis with prioritized issues
```

**Step 3: Request Fixes**
```
1. In Copilot Chat:
   "@security-reviewer fix the critical security issues"

2. Review proposed changes
3. Accept or modify
```

### Expected Outcomes
- Custom agent appears in @mention list
- Agent provides security-focused review
- Agent follows defined checklist
- Clear prioritization of issues

### Bonus Challenge
Add a subagent for OWASP Top 10 checks:

```
1. Create: `.github/agents/subagent-owasp.agent.md`
2. Add OWASP-specific checks
3. Reference it from @security-reviewer
4. Test the delegation
```

### Discussion
- What other specialized agents would help your team?
- How would you maintain agent definitions?
- Should agents have subagents or stay simple?

---

## Exercise 4: Agent Mode vs Coding Agent (30 min)

### Objective
Understand when to use local Agent Mode vs cloud-based Coding Agent.

### Task Part A: Quick Edit with Agent Mode (10 min)

**Scenario**: Add input validation to an existing endpoint.

```
1. Open: Controllers/CustomersController.cs
2. Select the CreateCustomer method
3. In Copilot Chat, select "Agent" mode
4. Request:
   "Add input validation to check:
    - Email is valid format
    - Phone number is valid format
    - Company name is not empty"

5. Review changes in the editor
6. Accept changes
7. Time how long this took
```

### Task Part B: Feature with Coding Agent (20 min)

**Scenario**: Add complete audit logging feature.

```
1. Create a GitHub Issue:
   Title: "Add audit logging for customer changes"
   Description:
   "Create an audit log system that tracks:
   - All customer Create/Update/Delete operations
   - Who made the change (user ID)
   - When the change occurred
   - What changed (before/after values)

   Requirements:
   - AuditLog model
   - AuditLogService with interface
   - Log automatically on customer changes
   - API endpoint to view audit logs
   - Unit tests for all components"

2. In VS Code:
   Copilot Chat → "Implement the audit logging feature from issue #X"

   OR

   On GitHub issue page → "Generate with Copilot"

3. Wait for Coding Agent to:
   - Clone repository
   - Analyze requirements
   - Implement all components
   - Write tests
   - Create pull request

4. Review the PR when complete
5. Check all files created
6. Review test coverage
7. Time how long this took
```

### Comparison Table

Fill this in based on your experience:

| Aspect | Agent Mode | Coding Agent |
|--------|-----------|--------------|
| **Time to complete** | ______ min | ______ min |
| **Files modified** | ______ | ______ |
| **Tests generated** | ❌ or ✓ | ❌ or ✓ |
| **Your involvement** | High/Medium/Low | High/Medium/Low |
| **Code quality** | 1-5 ⭐ | 1-5 ⭐ |
| **Best for...** | ____________ | ____________ |

### Expected Outcomes
- Clear understanding of trade-offs
- Experience with both approaches
- Ability to choose the right tool

### Discussion
- When would you prefer Agent Mode?
- When is Coding Agent worth the wait?
- How would this affect code review processes?
- What concerns do you have about autonomous agents?

---

## Exercise 5: Custom Instructions Hierarchy (20 min)

### Objective
Understand and utilize the 5-layer instruction hierarchy.

### Background
Instructions apply in this order (most specific wins):
1. Base Copilot (default behavior)
2. Repository instructions (`.github/copilot-instructions.md`)
3. Folder instructions (`.github/instructions/*.instructions.md`)
4. Custom agent instructions (`.github/agents/*.agent.md`)
5. Chat context (your specific request)

### Task
Create layered instructions and see how they interact.

### Steps

**Step 1: Repository-Level Standards**
```
1. Edit: `.github/copilot-instructions.md`
2. Add section:

## Error Handling Standard

All methods must include try-catch blocks with logging:

```csharp
try
{
    // Method logic
}
catch (Exception ex)
{
    _logger.LogError(ex, "Error in {MethodName}", nameof(MethodName));
    throw;
}
```

3. Save file
```

**Step 2: Folder-Level Override**
```
1. Create: `.github/instructions/controllers.instructions.md`
2. Add:

# Controller Error Handling

Controllers should NOT throw exceptions. Instead, return appropriate status codes:

```csharp
try
{
    // Controller logic
}
catch (ValidationException ex)
{
    _logger.LogWarning(ex, "Validation failed");
    return BadRequest(ex.Message);
}
catch (NotFoundException ex)
{
    _logger.LogWarning(ex, "Resource not found");
    return NotFound();
}
catch (Exception ex)
{
    _logger.LogError(ex, "Unexpected error");
    return StatusCode(500, "An error occurred");
}
```

3. Save file
```

**Step 3: Test the Hierarchy**
```
Test A - In a Service file:
1. Open: Services/CustomerService.cs
2. Request: "Add a method to delete a customer"
3. Observe: Try-catch THROWS exception (repo-level rule)

Test B - In a Controller file:
1. Open: Controllers/CustomersController.cs
2. Request: "Add a method to delete a customer"
3. Observe: Try-catch RETURNS status codes (folder-level override)

Test C - With Agent Override:
1. In Copilot Chat: "@api-expert add delete customer endpoint"
2. Observe: Follows @api-expert's specific guidelines
```

### Expected Outcomes
- Understand instruction precedence
- See how overrides work
- Learn to organize standards effectively

### Discussion
- How would you organize instructions in a large codebase?
- What standards should be repo-level vs folder-level?
- How do you prevent conflicting instructions?

---

## Exercise 6: Create a Useful Skill (30 min)

### Objective
Create a reusable skill that solves a common problem.

### Task
Create a "/code-review-checklist" skill that generates a PR checklist.

### Steps

**Step 1: Design the Skill**
```
Think about what a good code review checklist needs:
- Security checks
- Performance checks
- Testing requirements
- Documentation requirements
- Code style compliance
```

**Step 2: Create Skill File**
```
1. Create: `.github/skills/code-review-checklist/skill.md`
2. Add content:

---
name: code-review-checklist
description: Generate comprehensive code review checklist for PRs
---

# Code Review Checklist Generator

Creates a customized checklist based on the files changed in a PR.

## Usage

```
/code-review-checklist
```

## Generated Checklist

### Security ✓
- [ ] No hardcoded secrets or API keys
- [ ] All user input validated
- [ ] Parameterized queries used (no SQL injection)
- [ ] Authentication/authorization checked
- [ ] No sensitive data in logs

### Performance ✓
- [ ] Async/await used for I/O operations
- [ ] No N+1 query problems
- [ ] Database queries optimized with indexes
- [ ] Large collections use pagination
- [ ] Caching considered for expensive operations

### Testing ✓
- [ ] Unit tests added for new code
- [ ] Edge cases covered in tests
- [ ] Integration tests for API endpoints
- [ ] Test coverage ≥ 80%
- [ ] All tests passing

### Code Quality ✓
- [ ] SOLID principles followed
- [ ] No code duplication
- [ ] Methods are single-responsibility
- [ ] Naming conventions followed
- [ ] Comments added for complex logic

### Documentation ✓
- [ ] XML documentation for public APIs
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Migration guide if breaking changes

### Deployment ✓
- [ ] Database migrations included
- [ ] Environment variables documented
- [ ] Breaking changes documented
- [ ] Rollback plan exists

## File-Specific Checks

If PR includes Controllers:
- [ ] Proper HTTP status codes
- [ ] Input validation
- [ ] Error handling
- [ ] API versioning considered

If PR includes Database Migrations:
- [ ] Migration tested locally
- [ ] Rollback migration created
- [ ] Data integrity preserved
- [ ] Performance impact assessed

If PR includes Frontend Changes:
- [ ] Accessibility (A11Y) checked
- [ ] Responsive design verified
- [ ] Browser compatibility tested
- [ ] Loading states handled

## Output Format

The skill generates a markdown file: `.github/PULL_REQUEST_CHECKLIST.md`
that can be used as a PR template.
```

**Step 3: Create Template**
```
1. Create: `.github/skills/code-review-checklist/templates/checklist.md`
2. Add template content with placeholders
```

**Step 4: Test the Skill**
```
1. In Copilot Chat: "/code-review-checklist"
2. Expected: Generated checklist tailored to your project
3. Review the checklist
4. Save to: `.github/PULL_REQUEST_CHECKLIST.md`
```

**Step 5: Use in a PR**
```
1. Create a test branch with changes
2. Open a PR on GitHub
3. Copy checklist into PR description
4. Walk through each item
```

### Expected Outcomes
- Working skill accessible via /command
- Generated checklist relevant to your project
- Template reusable for all PRs

### Bonus Challenge
Extend the skill to:
- Detect file types and add specific checks
- Generate different checklists for features vs bugs
- Include team-specific requirements
- Auto-assign reviewers based on files changed

### Discussion
- What other skills would save you time?
- How would you share skills across teams?
- Should skills be project-specific or company-wide?

---

## Exercise 7: Full Feature Implementation (45 min)

### Objective
Put it all together: Use custom agents, instructions, and skills to implement a complete feature.

### Task
Implement a "Customer Notes" feature that allows adding timestamped notes to customer records.

### Requirements
- Backend: Note model, service, controller endpoints
- Frontend: Notes display component, add note form
- Validation: Note text required, max 500 characters
- Security: Only authenticated users can add notes
- Tests: Unit tests for all components
- Documentation: API documentation and README

### Steps

**Step 1: Plan with @workspace** (5 min)
```
In Copilot Chat:
"@workspace I need to add a customer notes feature. What files will need to be modified or created?"

Review the plan before proceeding.
```

**Step 2: Backend Implementation** (15 min)
```
Option A - Local Agent Mode:
1. Create the Note model manually
2. Use Agent mode to create NoteService
3. Use Agent mode to add controller endpoints
4. Use @reviewer to check your code

Option B - Coding Agent:
1. Create GitHub issue with full requirements
2. Delegate to Coding Agent
3. Wait for PR
4. Review and merge
```

**Step 3: Generate Tests** (10 min)
```
In Copilot Chat:
"/dotnet-api-testing for NotesController"

Review and run tests.
```

**Step 4: Documentation** (10 min)
```
In Copilot Chat:
"/api-documentation for NotesController"

Review generated documentation.
```

**Step 5: Security Review** (5 min)
```
In Copilot Chat:
"@security-reviewer review the NotesController and NoteService"

Address any issues found.
```

### Verification Checklist
- [ ] All backend endpoints working
- [ ] Tests passing (run: `dotnet test`)
- [ ] API documented
- [ ] Security review passed
- [ ] README updated
- [ ] No hardcoded values
- [ ] Error handling in place
- [ ] Logging added

### Expected Outcomes
- Complete feature implementation
- High code quality
- Comprehensive tests
- Good documentation
- Security validated

### Discussion
- How long did this take vs manual implementation?
- What parts did Copilot excel at?
- What required human intervention?
- How confident are you in the generated code?
- What would you change in your process?

---

## Exercise 8: Subagents & Parallel Reviews (20 min)

### Objective
Use subagents for specialized parallel analysis.

### Background
The @reviewer agent in this workshop uses three subagents:
- @subagent-security: Security vulnerabilities
- @subagent-performance: Performance issues
- @subagent-improver: Code improvements

### Task
Experience parallel subagent execution.

### Steps

**Step 1: Review Bad Code**
```
1. Open: DEMO-FILES/BadAuthController.cs
2. In Copilot Chat:
   "@reviewer please thoroughly review this controller"

3. Watch the workflow:
   - @reviewer analyzes the code
   - Spawns @subagent-security
   - Spawns @subagent-performance
   - Both run in parallel
   - @reviewer consolidates results
```

**Step 2: Analyze Results**
```
Count the issues found:
- Security issues: _____
- Performance issues: _____
- Total time: _____ seconds

Note: Without subagents, this would be sequential and slower.
```

**Step 3: Request Improvements**
```
In Copilot Chat:
"@reviewer please implement the top 3 critical fixes"

Watch:
- @reviewer invokes @subagent-improver
- @subagent-improver implements fixes
- Changes are presented for review
```

**Step 4: Create Your Own Subagent**
```
1. Create: `.github/agents/subagent-testing.agent.md`
2. Add test-specific analysis
3. Update @reviewer to invoke it
4. Test the new workflow
```

### Expected Outcomes
- Experience parallel subagent execution
- Understand delegation patterns
- See consolidated results
- Create your own subagent

### Discussion
- When are subagents better than a single agent?
- What's the trade-off between speed and accuracy?
- How many subagents is too many?
- What other subagents would be useful?

---

## Exercise 9: Real-World Integration (30 min)

### Objective
Apply what you've learned to your actual codebase.

### Task
Set up Copilot customization for your real project.

### Steps

**Step 1: Analyze Your Codebase**
```
Questions to answer:
1. What languages and frameworks do you use?
2. What are your coding standards?
3. What security requirements exist?
4. What repetitive tasks could be automated?
5. What types of code do you review most often?
```

**Step 2: Create Instructions**
```
1. Create `.github/copilot-instructions.md` for your project
2. Document:
   - Tech stack
   - Coding standards
   - Security requirements
   - Domain-specific terms
   - Project structure
```

**Step 3: Identify Useful Agents**
```
Based on your work, what agents would help?

Examples:
- @migration-expert for database changes
- @api-reviewer for REST APIs
- @frontend-reviewer for UI code
- @deployment-helper for CI/CD

Create at least one agent for your team.
```

**Step 4: Design Skills**
```
What repetitive tasks could become skills?

Examples:
- /generate-migration
- /add-logging
- /create-test-data
- /scaffold-crud

Create at least one skill for your workflow.
```

**Step 5: Setup MCP**
```
What external tools do you use?

Examples:
- Jira (for issue tracking)
- Slack (for team communication)
- PostgreSQL (for database access)
- Jenkins (for build status)

Configure at least one MCP server.
```

### Deliverables
- [ ] Repository instructions file
- [ ] At least one custom agent
- [ ] At least one skill
- [ ] At least one MCP server configured
- [ ] Documentation for your team

### Expected Outcomes
- Working Copilot customization for your project
- Clear documentation for team members
- Identified opportunities for further automation

### Discussion
- What was hardest to configure?
- What provides the most value?
- How will you maintain these customizations?
- How will you onboard team members?

---

## Bonus Challenges

### Challenge 1: Advanced Subagent Chain
Create a chain of subagents: @reviewer → @subagent-analyzer → @subagent-fixer → @subagent-tester

### Challenge 2: Multi-Model Comparison
Configure Copilot to use different models (GPT-4, Claude, Gemini) and compare results.

### Challenge 3: Copilot Workspace Flow
Use Copilot Workspace to implement a feature from issue to merged PR without touching VS Code.

### Challenge 4: CI/CD Integration
Create a GitHub Action that uses Copilot to review PRs automatically.

### Challenge 5: Team Skills Library
Create a shared skills repository that multiple projects can reference.

---

## Troubleshooting Guide

### Agent Not Appearing
```
1. Check file location: .github/agents/[name].agent.md
2. Verify YAML front matter syntax
3. Reload VS Code (F1 → Reload Window)
4. Check Copilot is signed in (bottom-left)
```

### Skill Not Working
```
1. Check file location: .github/skills/[name]/skill.md
2. Verify front matter has 'name' and 'description'
3. Reload VS Code
4. Try typing the full command: /skill-name
```

### MCP Server Not Connecting
```
1. Check .vscode/mcp.json syntax
2. Verify npm package exists
3. Check environment variables
4. Look at MCP logs (VS Code Output → MCP)
```

### Instructions Not Applied
```
1. Verify file location and naming
2. Check markdown syntax
3. Reload VS Code
4. Try with #file to force inclusion
```

---

## Workshop Feedback

After completing the exercises, please provide feedback:

### What Worked Well?
```
1.
2.
3.
```

### What Was Confusing?
```
1.
2.
3.
```

### Most Useful Feature?
```

```

### What Will You Use Tomorrow?
```
1.
2.
3.
```

### Suggestions for Improvement?
```

```

---

## Next Steps

After the workshop:

1. **This Week**:
   - Set up basic repository instructions
   - Create one custom agent
   - Configure one MCP server

2. **This Month**:
   - Create 2-3 useful skills
   - Add folder-level instructions
   - Train team members

3. **This Quarter**:
   - Build comprehensive agent library
   - Establish team standards
   - Measure productivity improvements

4. **Ongoing**:
   - Refine and update instructions
   - Share learnings with team
   - Explore new Copilot features

---

**End of Exercises** - Great work! 🎉
