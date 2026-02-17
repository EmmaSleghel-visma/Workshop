# Agent vs Subagent: Configuration Comparison

## Side-by-Side File Comparison

### Main Agent: reviewer.md
```yaml
---
name: reviewer
description: Code reviewer with security and performance subagents
# ❌ NO "infer: true" - This makes it a MAIN agent
---

# Code Reviewer Agent

You are an expert code reviewer specializing in .NET/C# applications.

## Your Workflow

1. **Analyze the code** provided by the user
2. **Invoke subagents** for specialized reviews:
   - Use `@subagent-security` to check for security vulnerabilities
   - Use `@subagent-performance` to analyze performance issues
3. **Consolidate feedback** from all subagents
4. **Provide actionable recommendations** with code examples

[... rest of instructions ...]
```

**Key Points:**
- ✅ User can type `@reviewer` to invoke
- ❌ NO `infer: true` field
- ✅ Instructions mention other subagents by name
- ✅ Orchestrates the workflow

---

### Subagent: subagent-security.md
```yaml
---
name: subagent-security
description: Security vulnerability checker specializing in .NET applications
infer: true    # ✅ THIS MAKES IT A SUBAGENT!
---

# Security Review Subagent

You are a security expert specializing in .NET/C# application security.

## Your Mission

Perform deep security analysis on code and identify vulnerabilities.

## Security Checklist

### Critical Issues
- 🔴 **SQL Injection**: Check for string concatenation in SQL queries
- 🔴 **XSS (Cross-Site Scripting)**: Unencoded output in views/APIs
[... rest of checklist ...]
```

**Key Points:**
- ❌ User CANNOT type `@subagent-security` directly
- ✅ HAS `infer: true` field (THE KEY DIFFERENCE!)
- ✅ Focused on ONE specific task (security)
- ✅ Called automatically by main agents

---

### Subagent: subagent-performance.md
```yaml
---
name: subagent-performance
description: Performance analysis specialist for .NET applications
infer: true    # ✅ THIS MAKES IT A SUBAGENT!
---

# Performance Review Subagent

You are a performance optimization expert for .NET/C# applications.

## Your Mission

Analyze code for performance bottlenecks and optimization opportunities.

## Performance Checklist

### Critical Issues
- 🔴 **N+1 Query Problem**: Multiple database queries in loops
- 🔴 **Missing Async/Await**: Blocking calls on async operations
[... rest of checklist ...]
```

**Key Points:**
- ❌ User CANNOT type `@subagent-performance` directly
- ✅ HAS `infer: true` field
- ✅ Focused on ONE specific task (performance)
- ✅ Called automatically by main agents

---

## The ONE Line That Makes the Difference

### Main Agent (NO infer)
```yaml
---
name: reviewer
description: Code reviewer with security and performance subagents
---
```
**Result:** User can invoke with `@reviewer`

### Subagent (WITH infer: true)
```yaml
---
name: subagent-security
description: Security vulnerability checker
infer: true    ← THIS SINGLE LINE!
---
```
**Result:** Only callable by other agents, not by users

---

## File Naming Convention

### Main Agents
```
.github/agents/
├── reviewer.md         ✅ Main agent
├── architect.md        ✅ Main agent (if you create one)
└── tester.md           ✅ Main agent (if you create one)
```

### Subagents
```
.github/agents/
├── subagent-security.md      ✅ Subagent
├── subagent-performance.md   ✅ Subagent
└── subagent-validation.md    ✅ Subagent (if you create one)
```

**Naming Pattern:**
- Main agents: `<name>.md`
- Subagents: `subagent-<name>.md`

This isn't required, but it's a helpful convention!

---

## How Main Agents Reference Subagents

### In reviewer.md:
```markdown
## Your Workflow

1. **Analyze the code** provided by the user
2. **Invoke subagents** for specialized reviews:
   - Use `@subagent-security` to check for security vulnerabilities
   - Use `@subagent-performance` to analyze performance issues
3. **Consolidate feedback** from all subagents
```

**Important:**
- Main agent explicitly mentions subagent names
- Uses `@subagent-name` syntax
- Describes WHEN to invoke each one

---

## Complete Example: Three-Agent System

### File Structure
```
.github/agents/
├── reviewer.md                    (Main Agent - infer: false/missing)
├── subagent-security.md          (Subagent - infer: true)
└── subagent-performance.md       (Subagent - infer: true)
```

### Workflow
```
User types: @reviewer review my code

→ reviewer.md receives request
  → Decides to check security
    → Invokes @subagent-security
      → subagent-security.md runs (infer: true allows this)
      ← Returns security findings
  → Decides to check performance
    → Invokes @subagent-performance
      → subagent-performance.md runs (infer: true allows this)
      ← Returns performance findings
  → Consolidates both sets of findings
← Returns unified review to user
```

---

## Testing Your Configuration

### Test Main Agent
```bash
# In VS Code Copilot Chat:
@

# Expected: Should show "reviewer" in autocomplete
```

### Test Subagent (Should Fail)
```bash
# In VS Code Copilot Chat:
@subagent-security

# Expected: Should NOT autocomplete (this is correct!)
```

### Test Full Workflow
```bash
# In VS Code Copilot Chat:
@reviewer review DEMO-FILES/BadAuthController.cs

# Expected: Should see:
# 1. Main agent response
# 2. "Invoking @subagent-security..." message
# 3. Security findings
# 4. "Invoking @subagent-performance..." message
# 5. Performance findings
# 6. Consolidated review
```

---

## Verification Script

Run this to verify your configuration:

```bash
#!/bin/bash

echo "Checking agent configuration..."

# Check main agent (should NOT have infer: true)
if grep -q "infer: true" .github/agents/reviewer.md; then
    echo "❌ ERROR: reviewer.md has 'infer: true' (should NOT have it)"
else
    echo "✅ reviewer.md correctly configured as main agent"
fi

# Check security subagent (SHOULD have infer: true)
if grep -q "infer: true" .github/agents/subagent-security.md; then
    echo "✅ subagent-security.md correctly configured as subagent"
else
    echo "❌ ERROR: subagent-security.md missing 'infer: true'"
fi

# Check performance subagent (SHOULD have infer: true)
if grep -q "infer: true" .github/agents/subagent-performance.md; then
    echo "✅ subagent-performance.md correctly configured as subagent"
else
    echo "❌ ERROR: subagent-performance.md missing 'infer: true'"
fi

echo ""
echo "Configuration check complete!"
```

---

## Common Mistakes

### ❌ Mistake 1: Main agent with infer: true
```yaml
---
name: reviewer
description: Code reviewer
infer: true    ← DON'T DO THIS!
---
```
**Problem:** Users won't be able to invoke it directly

### ❌ Mistake 2: Subagent without infer: true
```yaml
---
name: subagent-security
description: Security checker
# Missing infer: true    ← PROBLEM!
---
```
**Problem:** Main agents can't invoke it automatically

### ❌ Mistake 3: Wrong subagent reference
```yaml
# In reviewer.md:
Use `@security` to check...    ← WRONG NAME!
```
**Problem:** Must match exact subagent name: `@subagent-security`

### ✅ Correct Configuration
```yaml
# reviewer.md (Main Agent)
---
name: reviewer
description: Code reviewer
# NO infer field
---

# subagent-security.md (Subagent)
---
name: subagent-security
description: Security checker
infer: true    ← MUST HAVE THIS!
---

# In reviewer.md instructions:
Use `@subagent-security` to check...    ← EXACT NAME!
```

---

## Quick Reference Table

| Feature | Main Agent | Subagent |
|---------|-----------|----------|
| **File example** | `reviewer.md` | `subagent-security.md` |
| **Has `infer: true`?** | ❌ No | ✅ Yes |
| **User can invoke?** | ✅ Yes with `@name` | ❌ No |
| **Shows in autocomplete?** | ✅ Yes | ❌ No |
| **Called by other agents?** | ⚠️ Possible but uncommon | ✅ Always |
| **Can call subagents?** | ✅ Yes | ❌ No (1 level only) |
| **Context** | Full conversation | Isolated/clean |
| **Naming convention** | `<name>.md` | `subagent-<name>.md` |

---

## Summary

**The ONLY difference in the YAML front matter:**

```yaml
# Main Agent: NO infer field
---
name: reviewer
description: Code reviewer
---

# Subagent: HAS infer: true field
---
name: subagent-security
description: Security checker
infer: true    ← THIS IS THE ONLY DIFFERENCE!
---
```

**That's it!** One line makes all the difference. 🎯

---

## Workshop Teaching Tip

**Show this to participants:**

Print two agent files side-by-side, highlight the YAML front matter, and point to the ONE LINE difference:

```
reviewer.md               subagent-security.md
-----------               --------------------
---                       ---
name: reviewer            name: subagent-security
description: ...          description: ...
                          infer: true    ← THIS LINE!
---                       ---
```

**Say:**
> "See this ONE line? `infer: true`? That's literally the only
> difference between a main agent and a subagent. Everything
> else works the same way!"

This makes it crystal clear! ✨
