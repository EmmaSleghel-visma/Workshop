# What You'll See: Agent & Subagent Invocation

This document shows **exactly** what appears in VS Code when you invoke agents.

---

## 🖥️ Screen Layout During Demo

```
┌────────────────────────────────────────────────────────────────┐
│ VS Code Window                                                 │
├──────────────────────┬─────────────────────────────────────────┤
│                      │                                         │
│  CODE EDITOR         │   COPILOT CHAT PANEL                   │
│                      │                                         │
│  BadAuthController   │   [Your conversation appears here]     │
│  .cs                 │                                         │
│                      │   👇 THIS IS WHERE YOU'LL SEE          │
│  (The file being     │      THE AGENT WORKFLOW               │
│   reviewed)          │                                         │
│                      │                                         │
│                      │                                         │
└──────────────────────┴─────────────────────────────────────────┘
```

---

## 📝 Step-by-Step: What Appears in Chat

### Step 1: You Type

**In Copilot Chat, you type:**
```
@reviewer please review DEMO-FILES/BadAuthController.cs
```

**What you see:**
```
┌─────────────────────────────────────────────┐
│ Copilot Chat                                │
├─────────────────────────────────────────────┤
│                                             │
│ 👤 You:                                     │
│ @reviewer please review DEMO-FILES/         │
│ BadAuthController.cs                        │
│                                             │
│ [Copilot is thinking...]                   │
│ ⏳                                          │
└─────────────────────────────────────────────┘
```

---

### Step 2: Main Agent Responds

**Main agent starts processing:**

```
┌─────────────────────────────────────────────┐
│ Copilot Chat                                │
├─────────────────────────────────────────────┤
│ 👤 You:                                     │
│ @reviewer please review DEMO-FILES/         │
│ BadAuthController.cs                        │
│                                             │
│ 🤖 Copilot (@reviewer):                    │
│ I'll analyze this authentication            │
│ controller for security and performance     │
│ issues.                                     │
│                                             │
│ 🔍 Analyzing code structure...             │
│                                             │
└─────────────────────────────────────────────┘
```

---

### Step 3: Subagent Security Invoked

**You'll see this message appear:**

```
┌─────────────────────────────────────────────┐
│ Copilot Chat                                │
├─────────────────────────────────────────────┤
│ 🤖 Copilot (@reviewer):                    │
│ I'll analyze this authentication            │
│ controller for security and performance     │
│ issues.                                     │
│                                             │
│ 🔍 Analyzing code structure...             │
│                                             │
│ 🔐 Invoking @subagent-security for         │
│    security analysis...                     │
│    ⏳ Running...                           │
│                                             │
└─────────────────────────────────────────────┘
```

**👉 THIS IS KEY!**
You see "@subagent-security" mentioned, but YOU didn't type it!
The main agent invoked it automatically.

---

### Step 4: Security Subagent Results

**Security findings appear:**

```
┌─────────────────────────────────────────────┐
│ Copilot Chat                                │
├─────────────────────────────────────────────┤
│ 🔐 Invoking @subagent-security for         │
│    security analysis...                     │
│                                             │
│ 🔴 @subagent-security found:               │
│                                             │
│ CRITICAL ISSUES:                            │
│                                             │
│ 🔴 SQL Injection Vulnerability              │
│    Location: line 28                        │
│    Code: var query = $"SELECT * FROM       │
│          Users WHERE Username='{username}'  │
│    Risk: Attacker can execute arbitrary    │
│          SQL commands                       │
│    Fix: Use parameterized queries          │
│                                             │
│ 🔴 Hardcoded API Secrets                   │
│    Location: line 54-55                     │
│    Code: var apiKey = "sk_live_123..."     │
│    Risk: Secrets exposed in code           │
│    Fix: Use environment variables          │
│                                             │
│ 🟠 Missing Authorization                   │
│    Location: line 42                        │
│    Risk: Admin endpoint accessible to all  │
│    Fix: Add [Authorize] attribute          │
│                                             │
│ [... more security issues ...]             │
│                                             │
└─────────────────────────────────────────────┘
```

---

### Step 5: Performance Subagent Invoked (PARALLEL!)

**While security is still running, this appears:**

```
┌─────────────────────────────────────────────┐
│ Copilot Chat                                │
├─────────────────────────────────────────────┤
│ [Security findings shown above]             │
│                                             │
│ ⚡ Invoking @subagent-performance for      │
│    performance analysis...                  │
│    ⏳ Running in parallel...               │
│                                             │
└─────────────────────────────────────────────┘
```

**👉 PARALLEL EXECUTION!**
Both subagents run at the same time (January 2026 feature)

---

### Step 6: Performance Subagent Results

**Performance findings appear:**

```
┌─────────────────────────────────────────────┐
│ Copilot Chat                                │
├─────────────────────────────────────────────┤
│ ⚡ Invoking @subagent-performance for      │
│    performance analysis...                  │
│                                             │
│ 🔴 @subagent-performance found:            │
│                                             │
│ CRITICAL ISSUES:                            │
│                                             │
│ 🔴 Missing Async/Await                     │
│    Location: line 48                        │
│    Code: return _context.Users.ToList();   │
│    Impact: Thread blocking                 │
│    Fix: Use ToListAsync()                  │
│                                             │
│ 🟠 No Caching                              │
│    Location: GetAllUsers method            │
│    Impact: Repeated database calls         │
│    Fix: Implement caching layer            │
│                                             │
│ [... more performance issues ...]          │
│                                             │
└─────────────────────────────────────────────┘
```

---

### Step 7: Main Agent Consolidates

**The reviewer agent brings it all together:**

```
┌─────────────────────────────────────────────┐
│ Copilot Chat                                │
├─────────────────────────────────────────────┤
│ [Both subagent results shown above]         │
│                                             │
│ 📊 Copilot (@reviewer):                    │
│                                             │
│ CODE REVIEW SUMMARY                         │
│ ═══════════════════════════════════════════ │
│                                             │
│ Based on security and performance reviews:  │
│                                             │
│ 🔴 CRITICAL ISSUES FOUND: 5                │
│    - SQL Injection (Security)               │
│    - Hardcoded Secrets (Security)           │
│    - Missing Async/Await (Performance)      │
│    - Missing Authorization (Security)       │
│    - Information Disclosure (Security)      │
│                                             │
│ 🟠 HIGH PRIORITY: 3                        │
│    - No Caching (Performance)               │
│    - Open Redirect (Security)               │
│    - Missing Input Validation (Security)    │
│                                             │
│ RECOMMENDATIONS:                            │
│                                             │
│ 1. Fix SQL injection IMMEDIATELY           │
│    Use Entity Framework parameterized:     │
│    ```csharp                                │
│    var user = await _context.Users         │
│        .FirstOrDefaultAsync(u =>           │
│            u.Username == request.Username);│
│    ```                                      │
│                                             │
│ 2. Move secrets to environment variables   │
│    ```csharp                                │
│    var apiKey = Environment.GetEnvironment │
│        Variable("API_KEY");                │
│    ```                                      │
│                                             │
│ 3. Convert to async throughout             │
│                                             │
│ Would you like me to provide fixed code    │
│ for any specific issue?                    │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎬 Real-Time Streaming Effect

**What it actually looks like:**

The responses appear **word by word** as they stream:

```
Frame 1 (0.0s):
🤖 Copilot (@reviewer):
I'll analyze

Frame 2 (0.1s):
🤖 Copilot (@reviewer):
I'll analyze this authentication

Frame 3 (0.2s):
🤖 Copilot (@reviewer):
I'll analyze this authentication controller

Frame 4 (1.5s):
🔐 Invoking @subagent-security

Frame 5 (1.6s):
🔐 Invoking @subagent-security for security

Frame 6 (2.8s):
🔴 @subagent-security found:

Frame 7 (3.0s):
CRITICAL ISSUES:

[... continues streaming ...]
```

**This creates a dynamic, engaging demo!**

---

## 🔍 Output Panel View (Developer Details)

**If you open Output panel (View → Output → GitHub Copilot):**

```
┌─────────────────────────────────────────────────────────────┐
│ OUTPUT: GitHub Copilot                                      │
├─────────────────────────────────────────────────────────────┤
│ [Info] Agent selected: reviewer                             │
│ [Info] Loading agent config: .github/agents/reviewer.md    │
│ [Info] Agent context size: 15234 tokens                     │
│ [Info] Subagent invocation: subagent-security              │
│ [Debug] Creating isolated context for subagent             │
│ [Debug] Subagent context: 4521 tokens                      │
│ [Info] Subagent invocation: subagent-performance           │
│ [Debug] Parallel execution enabled (Jan 2026)              │
│ [Info] Subagent-security response time: 1.2s               │
│ [Info] Subagent-performance response time: 1.1s            │
│ [Info] Consolidating results...                            │
│ [Info] Total execution time: 2.8s                          │
│ [Info] Response tokens: 8942                               │
└─────────────────────────────────────────────────────────────┘
```

**This shows:**
- Which agents were invoked
- Timing information
- Context sizes
- Parallel execution confirmation

---

## 📊 Visual Indicators to Point Out

### 1. **Agent Attribution**
```
🤖 Copilot (@reviewer):    ← Main agent speaking
🔴 @subagent-security:     ← Subagent speaking
⚡ @subagent-performance:  ← Subagent speaking
```

### 2. **Invocation Messages**
```
🔐 Invoking @subagent-security...    ← Watch for this!
⚡ Invoking @subagent-performance... ← And this!
```

### 3. **Status Indicators**
```
⏳ Running...              ← In progress
✓ Complete                ← Finished
🔄 Parallel execution     ← Multiple running
```

---

## 🎯 What to Emphasize to Participants

### During Streaming Output:

**Point 1: Automatic Invocation**
```
👉 "See this line? 'Invoking @subagent-security...'
    We didn't type that - the main agent did it automatically!"
```

**Point 2: Parallel Execution**
```
👉 "Notice both subagents are running?
    Security AND performance at the same time!
    This is the January 2026 parallel feature!"
```

**Point 3: Clean Context**
```
👉 "Each subagent gets isolated context.
    Security subagent only sees security rules.
    Performance subagent only sees performance rules.
    This gives better, more focused results."
```

**Point 4: Orchestration**
```
👉 "The main agent coordinates everything:
    - Invokes both subagents
    - Waits for responses
    - Consolidates findings
    - Presents unified review"
```

---

## ⚡ Quick Demo Script

**1-Minute Version:**

```
[Type in chat]:
@reviewer review BadAuthController.cs

[Point to screen as it streams]:
"Watch: Main agent starts...
Now invoking security subagent...
Now performance subagent (parallel!)...
Security findings appear...
Performance findings appear...
Main agent consolidates everything!"

[Finished]:
"That's the agent workflow in action!"
```

---

## 🎓 Practice Exercise

**After showing this, have participants try:**

```
Exercise: Watch Your Own Invocation

1. Open Copilot Chat
2. Type: @reviewer review DEMO-FILES/BadPerformanceService.cs
3. Count how many times you see:
   - "Invoking @subagent-..."
   - Subagent responses
4. Notice the final consolidation

Questions:
- How many subagents were invoked?
- Did they run in parallel?
- What did the main agent do at the end?
```

---

## 📸 Screenshots to Prepare

For your presentation, take screenshots of:

1. **Before**: Typing `@reviewer` in chat
2. **During**: "Invoking @subagent-security..." message
3. **During**: Both subagents shown in parallel
4. **After**: Final consolidated review
5. **Output Panel**: Timing and execution details

Use these if live demo fails!

---

## ✅ Verification Before Demo

**Test your demo:**
```bash
# 1. Check agents are configured
cat .github/agents/reviewer.md | grep "subagent"

# Should show references to subagents

# 2. Check subagents have infer:true
grep "infer: true" .github/agents/subagent-*.md

# Should show both files

# 3. Test the invocation
# Open VS Code → Copilot Chat → Type:
@reviewer review DEMO-FILES/BadAuthController.cs

# Should see full workflow!
```

---

## 🐛 Troubleshooting: What You Might NOT See

**If subagents don't invoke:**

```
❌ You'll see:
🤖 Copilot (@reviewer):
I've reviewed the code and found these issues...
[Direct response without subagents]

✅ You should see:
🤖 Copilot (@reviewer):
I'll analyze this code...
🔐 Invoking @subagent-security...
⚡ Invoking @subagent-performance...
```

**Fix:**
1. Check `infer: true` in subagent files
2. Verify main agent mentions subagents by name
3. Reload VS Code
4. Check Copilot extension version

---

## Summary: What You'll See Checklist

During a successful agent invocation, you'll see:

- [ ] Your `@reviewer` message
- [ ] Main agent's initial response
- [ ] "Invoking @subagent-security..." message
- [ ] Security subagent findings
- [ ] "Invoking @subagent-performance..." message
- [ ] Performance subagent findings
- [ ] Main agent's consolidated summary
- [ ] All within 3-5 seconds total

**If you see all of these, your agent setup is working perfectly!** 🎉
