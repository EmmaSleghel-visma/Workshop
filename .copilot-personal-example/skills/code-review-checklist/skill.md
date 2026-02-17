---
name: code-review-checklist
description: Personal code review standards and checklist
---

# Personal Code Review Checklist

This is a personal skill that applies YOUR code review standards.

## Installation

Copy this folder to your home directory:
```bash
# Windows
mkdir %USERPROFILE%\.copilot\skills
xcopy .copilot-personal-example\skills %USERPROFILE%\.copilot\skills /E

# Mac/Linux
mkdir -p ~/.copilot/skills
cp -r .copilot-personal-example/skills/* ~/.copilot/skills/
```

## Usage

```
/code-review-checklist
Review the changes in CustomersController.cs using my personal standards
```

## Review Standards

When reviewing code, check for:

### Critical Issues
- ✅ **Null Reference Safety**: All nullable types handled properly
- ✅ **Async/Await**: Properly used throughout (no .Result or .Wait())
- ✅ **Exception Handling**: Try-catch blocks with proper logging
- ✅ **Resource Disposal**: All IDisposable resources properly disposed

### Code Quality
- ✅ **No Magic Values**: Use constants or configuration
- ✅ **DRY Principle**: No duplicate code
- ✅ **Single Responsibility**: Each method does one thing
- ✅ **Meaningful Names**: Clear, descriptive variable/method names

### Documentation
- ✅ **XML Comments**: All public methods documented
- ✅ **Complex Logic Comments**: Non-obvious code explained
- ✅ **TODO/HACK Notes**: None left unaddressed

### Testing
- ✅ **Unit Tests**: Included for new functionality
- ✅ **Test Coverage**: >80% coverage maintained
- ✅ **Edge Cases**: Covered in tests

### Performance
- ✅ **Database Queries**: Optimized (no N+1 problems)
- ✅ **Collection Operations**: Efficient LINQ usage
- ✅ **String Operations**: StringBuilder in loops

### Security
- ✅ **Input Validation**: All user input validated
- ✅ **SQL Injection**: Parameterized queries only
- ✅ **Authentication**: Required on all endpoints (unless public)
- ✅ **Sensitive Data**: Not logged or exposed

## Output Format

Provide feedback in this structure:

```markdown
# Code Review Results

## Critical Issues Found: [COUNT]
[List issues with severity, location, and fix]

## Code Quality Issues: [COUNT]
[List issues]

## Documentation Issues: [COUNT]
[List issues]

## Security Issues: [COUNT]
[List issues]

## Recommendations
[List positive improvements]

## Overall Assessment
[Summary with approval status: ✅ Approved | ⚠️ Needs Minor Changes | ❌ Needs Major Changes]
```

## Example Review

```markdown
# Code Review Results

## Critical Issues Found: 1

🔴 **Null Reference Exception Risk**
Location: CustomerService.cs, line 42
Code: `return customer.Email.ToLower();`
Risk: If customer is null, this will throw NullReferenceException
Fix: Add null check or use null-conditional operator
```csharp
return customer?.Email?.ToLower() ?? string.Empty;
```

## Code Quality Issues: 2

🟡 **Magic String**
Location: CustomerService.cs, line 38
Code: `if (status == "Active")`
Fix: Use constant
```csharp
private const string ACTIVE_STATUS = "Active";
if (status == ACTIVE_STATUS)
```

🟡 **Method Too Long**
Location: OrderService.cs, ProcessOrder method (78 lines)
Fix: Extract sub-methods for validation, calculation, and persistence

## Documentation Issues: 1

⚪ **Missing XML Comment**
Location: CustomerService.CreateAsync method
Fix: Add XML documentation

## Security Issues: 0
✅ No security issues found

## Recommendations
- Consider adding caching for frequently accessed customer data
- Extract validation logic to separate validator classes
- Use FluentValidation library for complex validation rules

## Overall Assessment
⚠️ **Needs Minor Changes** - Address null safety and magic string issues before merging.
The code is well-structured and follows most best practices. Good use of async/await throughout.
```

## Customization

Modify this skill to match YOUR preferences:
- Add/remove checklist items
- Change severity levels
- Add project-specific standards
- Include your preferred patterns
