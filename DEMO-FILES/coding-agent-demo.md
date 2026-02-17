# Copilot Coding Agent Demo

## Overview
The Coding Agent is a cloud-based autonomous agent that runs in a GitHub Actions environment. It can implement entire features, fix bugs, and create pull requests independently.

## Key Differences: Agent Mode vs Coding Agent

| Feature | Agent Mode (Local) | Coding Agent (Cloud) |
|---------|-------------------|---------------------|
| **Location** | Runs in VS Code | Runs in GitHub Actions |
| **Context** | Current workspace only | Full repository clone |
| **Environment** | Your machine | Isolated VM with tools |
| **Speed** | Fast (local) | Slower (network + setup) |
| **Capabilities** | Edit files | Clone, build, test, commit, PR |
| **When to use** | Quick edits, refactoring | Feature implementation, complex tasks |

## Demo Scenario 1: Feature Implementation

### Setup
1. Open the Creditro demo app in VS Code
2. Navigate to `backend/CreditroDemo.API/Controllers/CustomersController.cs`

### Task
Implement a new endpoint to search customers by company name.

### Using Agent Mode (Local)
```
In Copilot Chat:
Select "Agent" from session type dropdown

"Add a new GET endpoint /api/customers/search?companyName={name} that searches
customers by company name (case-insensitive). Return a list of matching customers."

Copilot will:
- Edit CustomersController.cs locally
- Add the new method
- You review and accept/reject changes
```

**Time**: ~30 seconds
**Result**: Code changes in your editor

### Using Coding Agent (Cloud)
```
In your code, add a comment:

// TODO: Add endpoint to search customers by company name

Right-click the TODO → "Delegate to Coding Agent"

Coding Agent will:
1. Clone the repository
2. Analyze the codebase
3. Implement the endpoint
4. Write unit tests
5. Run tests
6. Create a pull request

GitHub creates PR #42 with full implementation + tests
```

**Time**: ~3-5 minutes
**Result**: Complete PR ready for review

## Demo Scenario 2: Bug Fix with Tests

### Setup
Open `backend/CreditroDemo.API/Services/CustomerService.cs`

### Task
The service doesn't validate email addresses properly.

### Demo Script

**Step 1: Create an Issue**
```
GitHub Issues:
Title: "Email validation missing in CustomerService"
Description: "The CreateCustomer method doesn't validate email format.
This allows invalid emails like 'notanemail' to be stored."

Assign to: @me
Labels: bug, priority:high
```

**Step 2: Delegate to Coding Agent**
```
In VS Code:
Copilot Chat → "Fix the email validation bug in issue #X"

OR

In the issue on GitHub:
Click "Generate with Copilot" button
```

**Step 3: Watch the Magic**
```
Coding Agent activity:
✓ Analyzing issue #X
✓ Cloning repository
✓ Reading CustomerService.cs
✓ Adding email validation logic
✓ Creating unit tests for edge cases
✓ Running all tests (23/23 passed)
✓ Creating PR #43 "Fix: Add email validation to CustomerService"
```

**Step 4: Review the PR**
```
GitHub PR #43 includes:
- CustomerService.cs: Email validation with regex
- CustomerServiceTests.cs: 5 new test cases
  - Valid email passes
  - Invalid format rejected
  - Empty email rejected
  - Null email rejected
  - Edge cases (spaces, special chars)
- All tests passing ✓
```

## Demo Scenario 3: Copilot Workspace

### What is Copilot Workspace?
A full development environment in GitHub that uses agents to:
- Plan feature implementation
- Generate code across multiple files
- Run tests
- Create PRs

### Demo Script

**Step 1: Open Copilot Workspace**
```
GitHub → Repository → Issues → Select an issue
Click "Open in Copilot Workspace"

OR

Go directly to: https://copilot-workspace.githubnext.com
```

**Step 2: Natural Language Task**
```
In Workspace:
"Add a feature to export customer data to CSV format. Include all customer fields,
compliance checks, and risk assessment. Add a download button to the Angular frontend."
```

**Step 3: Review the Plan**
```
Copilot Workspace generates:
📋 Implementation Plan
1. Backend: Add CSVExportService
2. Backend: Add /api/customers/export endpoint in CustomersController
3. Frontend: Add export button to customer-list component
4. Frontend: Add CSV download handling
5. Tests: Unit tests for CSV generation
6. Tests: Integration tests for export endpoint

Estimated files: 6 modified, 3 created
```

**Step 4: Approve and Implement**
```
Click "Implement Plan"

Watch as Copilot Workspace:
✓ Creates CSVExportService.cs
✓ Modifies CustomersController.cs
✓ Modifies customer-list.component.ts
✓ Modifies customer-list.component.html
✓ Creates CSVExportServiceTests.cs
✓ Creates CustomerExportIntegrationTests.cs
✓ Runs all tests (31/31 passed)
✓ Creates PR #44

Time: ~5 minutes
Result: Complete feature with tests
```

## Demo Scenario 4: Working Trees Integration

### What are Working Trees?
Multiple working directories from the same repository, allowing parallel work without branch switching.

### Demo Script

**Step 1: Create Working Trees**
```bash
# Main work in main branch
cd Workshop/

# Create working tree for feature A
git worktree add ../Workshop-feature-a feature/csv-export

# Create working tree for feature B
git worktree add ../Workshop-feature-b feature/email-validation

# List working trees
git worktree list
```

**Step 2: Delegate to Coding Agent with Working Trees**
```
In VS Code (main workspace):
"Delegate CSV export feature to Coding Agent in working tree feature-a"

In VS Code (open ../Workshop-feature-a):
"Delegate email validation fix to Coding Agent in working tree feature-b"

Both agents work in parallel without conflicts!
```

**Step 3: Benefits**
- Work on multiple features simultaneously
- No branch switching disruption
- Each agent has isolated environment
- Easy to compare implementations

## Demo Scenario 5: Plan Mode

### What is Plan Mode?
Preview what Copilot will do before it makes changes.

### Demo Script

**Step 1: Enable Plan Mode**
```
VS Code Settings:
Search "Copilot Plan Mode"
Enable "GitHub Copilot: Plan Mode"

OR

In Copilot Chat:
Click "Plan" session type
```

**Step 2: Request a Change**
```
In Copilot Chat (Plan mode):
"Refactor CustomerService to use dependency injection for the validator"

Copilot shows:
📋 PLAN
1. Create ICustomerValidator interface
2. Implement EmailValidator class
3. Register validator in Program.cs (DI container)
4. Inject ICustomerValidator into CustomerService
5. Update constructor and validation calls
6. Update unit tests to use mocks

Files to modify:
- Services/CustomerService.cs
- Interfaces/ICustomerValidator.cs (new)
- Validators/EmailValidator.cs (new)
- Program.cs
- Tests/CustomerServiceTests.cs

Approve to implement? [Yes] [Modify Plan] [Cancel]
```

**Step 3: Review and Approve**
```
Review the plan, then:
- Click "Yes" to implement
- Click "Modify Plan" to adjust
- Click "Cancel" to abort

After approval, Copilot implements exactly what was planned.
```

## Hands-On Exercise

### Exercise 1: Simple Feature (15 min)
**Task**: Add a new endpoint to get customers by risk level
- Use **Agent Mode** for quick implementation
- Endpoint: `GET /api/customers/by-risk/{level}`
- Return filtered list

**Steps**:
1. Open CustomersController.cs
2. Use Copilot Chat with "Agent" mode
3. Request the feature
4. Review and accept changes
5. Test the endpoint

### Exercise 2: Complex Feature (20 min)
**Task**: Add audit logging for all customer changes
- Use **Coding Agent** (cloud) for complete implementation
- Create AuditLog model and service
- Log all Create/Update/Delete operations
- Add audit log viewing endpoint
- Include unit tests

**Steps**:
1. Create a GitHub issue describing the feature
2. Assign to yourself
3. Delegate to Coding Agent
4. Wait for PR creation (~3-5 min)
5. Review the PR
6. Check tests pass
7. Merge if satisfied

### Exercise 3: Copilot Workspace (15 min)
**Task**: Bulk import customers from CSV
- Open Copilot Workspace
- Describe the feature in natural language
- Review the generated plan
- Approve and watch implementation
- Review the resulting PR

## Comparison Summary

Use **Agent Mode** when:
- Making quick, focused edits
- Refactoring existing code
- You want instant feedback
- Working offline or with slow network

Use **Coding Agent** when:
- Implementing complete features
- Need tests generated automatically
- Want a full PR ready for review
- Complex multi-file changes

Use **Copilot Workspace** when:
- Planning large features
- Need to discuss approach first
- Want to see full plan before implementation
- Coordinating multiple related changes

## Discussion Questions

1. When would you prefer local Agent Mode over cloud Coding Agent?
2. How would Coding Agent change your code review process?
3. What concerns do you have about autonomous code generation?
4. How would you ensure code quality with agent-generated code?
5. What types of tasks would you NOT delegate to Coding Agent?

## Resources

- Coding Agent Docs: https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-coding-agent
- Copilot Workspace: https://githubnext.com/projects/copilot-workspace
- Working Trees: https://git-scm.com/docs/git-worktree
- Plan Mode: https://code.visualstudio.com/docs/copilot/copilot-chat#_plan-mode
