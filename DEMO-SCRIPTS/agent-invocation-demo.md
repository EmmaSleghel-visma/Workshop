# Agent & Subagent Invocation Demo

## Demo: Seeing Agents in Action

**Duration**: 10 minutes
**Purpose**: Show participants how main agents orchestrate subagents

---

## Setup (1 minute)

1. Open VS Code with Workshop folder
2. Open Copilot Chat (Ctrl/Cmd + Shift + I)
3. Have DEMO-FILES/BadAuthController.cs ready
4. Have Output panel visible (View → Output → GitHub Copilot)

**Projector Setup:**
- Split screen: Chat on left, Output panel on right
- Font size: 18pt minimum for readability

---

## Part 1: Show Agent Autocomplete (2 minutes)

### Demonstrate Main Agent

**Script:**
```
INSTRUCTOR: "First, let's see what agents are available."

[In Copilot Chat, type:]
@

[Pause - show autocomplete list]

INSTRUCTOR: "See? The @reviewer agent appears in the list.
This is a MAIN agent - we can invoke it directly."

[Type:]
@reviewer

[Show it autocompletes]
```

### Try Subagent (Show It Doesn't Work)

**Script:**
```
INSTRUCTOR: "Now let's try a subagent..."

[Clear chat, type:]
@subagent-

[Pause - show it doesn't autocomplete]

INSTRUCTOR: "Notice - subagents DON'T appear in the autocomplete!
That's because users can't invoke them directly.
They're automatically called by main agents."
```

**Key Point to Emphasize:**
> "If you see it in @ autocomplete, it's a main agent.
> Subagents are invisible to you - they work behind the scenes."

---

## Part 2: Invoke Reviewer & Watch Workflow (5 minutes)

### The Full Invocation

**Script:**
```
INSTRUCTOR: "Now let's see the magic happen. Watch the chat carefully."

[In Copilot Chat, type:]
@reviewer please review DEMO-FILES/BadAuthController.cs for security and performance issues

[Press Enter]

INSTRUCTOR: "Watch as the reviewer orchestrates the review..."
```

### What You'll See (Point Out Each Step)

**Step 1: Main Agent Starts**
```
👉 Point to chat output:

Copilot (reviewer):
"I'll analyze this code and check for security and performance issues."
```

**Step 2: Subagent Invocations**
```
👉 Point to chat output:

"Invoking @subagent-security for security analysis..."
```

**PAUSE HERE and say:**
```
INSTRUCTOR: "See this? The MAIN agent is calling the subagent.
We didn't type @subagent-security - the reviewer did it automatically!

This is the power of the agent architecture."
```

**Step 3: Subagent Response**
```
👉 Point to chat output:

@subagent-security found:
🔴 CRITICAL: SQL Injection Vulnerability
Location: line 28
...
```

**PAUSE and say:**
```
INSTRUCTOR: "The subagent has ISOLATED context - it only sees the code
and the security checklist. It doesn't know about the full conversation.
This gives cleaner, more focused results."
```

**Step 4: Second Subagent (Parallel!)**
```
👉 Point to chat output:

"Invoking @subagent-performance for performance analysis..."

@subagent-performance found:
🔴 Missing async/await
...
```

**HIGHLIGHT:**
```
INSTRUCTOR: "Did you notice both subagents ran?
As of January 2026, they run IN PARALLEL!
The main agent coordinates everything."
```

**Step 5: Consolidation**
```
👉 Point to chat output:

Copilot (reviewer):
"Based on the security and performance reviews, here are the key issues:

📊 CRITICAL ISSUES FOUND:
1. SQL Injection (from security review)
2. Missing async/await (from performance review)
...

Recommendations:
[Main agent consolidates everything]
```

**EMPHASIZE:**
```
INSTRUCTOR: "The main agent took both subagent responses,
consolidated them, and presented ONE unified review.
This is orchestration!"
```

---

## Part 3: Show in Output Panel (2 minutes)

**Script:**
```
INSTRUCTOR: "Now let's look under the hood..."

[Show Output panel: View → Output → Select "GitHub Copilot"]

👉 Point to logs:

"You can see detailed timing:
- Agent selection: 50ms
- Subagent-security invocation: 1.2s
- Subagent-performance invocation: 1.1s (parallel!)
- Consolidation: 0.3s
- Total: ~2.6s for full review"
```

---

## Part 4: Manual Subagent Attempt (1 minute)

**Show What Happens If You Try to Force It**

**Script:**
```
INSTRUCTOR: "What if we try to invoke a subagent directly?"

[In chat, type:]
@subagent-security review this code

[Show result]

INSTRUCTOR: "Copilot doesn't recognize it! It's not designed
for direct invocation. You MUST go through the main agent."
```

---

## Part 5: Explain the Architecture (1 minute)

**Visual Explanation:**

Draw or show on screen:

```
┌─────────────────────────────────────────┐
│           USER                          │
│                                         │
│   Types: @reviewer review code         │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│      MAIN AGENT (reviewer.md)           │
│                                         │
│  • Receives user request                │
│  • Decides what's needed                │
│  • Orchestrates subagents               │
│  • Consolidates results                 │
└─────────┬───────────────┬───────────────┘
          │               │
          ↓               ↓
┌──────────────┐  ┌──────────────────┐
│ SUBAGENT-    │  │ SUBAGENT-        │
│ SECURITY     │  │ PERFORMANCE      │
│              │  │                  │
│ infer: true  │  │ infer: true      │
│              │  │                  │
│ Focused on   │  │ Focused on       │
│ security     │  │ performance      │
└──────────────┘  └──────────────────┘
    RUN IN PARALLEL (Jan 2026)
```

---

## Key Takeaways to Emphasize

1. **Main agents** = User-facing (@reviewer)
2. **Subagents** = Automatically invoked (infer: true)
3. **Subagents run in parallel** (January 2026 feature)
4. **Clean context** = Better results per subagent
5. **Orchestration** = Main agent coordinates everything

---

## Common Questions from Participants

### Q: "Can I invoke subagents directly?"
**A:** "No, and you shouldn't want to! The main agent provides the orchestration and consolidation. Going directly to a subagent would bypass this."

### Q: "How many subagents can one agent invoke?"
**A:** "As many as you configure! The reviewer could invoke 10 different subagents if needed."

### Q: "Can subagents invoke other subagents?"
**A:** "No - only ONE level deep. This prevents complexity and keeps execution predictable."

### Q: "How fast is this?"
**A:** "Very fast! With parallel execution (Jan 2026), multiple subagents run simultaneously. Total time is limited by the slowest subagent, not the sum of all."

### Q: "Where do I see which subagents will be invoked?"
**A:** "Look in the main agent's .md file - it explicitly mentions which subagents to use: 'Use @subagent-security to check...'."

---

## Practice Exercise for Participants

**After Demo:**

```
INSTRUCTOR: "Now you try! Open BadPerformanceService.cs
and invoke the reviewer. Watch the chat output carefully.
Can you spot when each subagent is invoked?"
```

**Expected Output:**
- Main agent starts
- @subagent-security invoked
- @subagent-performance invoked
- Both return findings
- Main agent consolidates

---

## Verification Checklist

Before this demo, verify:
- [ ] Agents configured in .github/agents/
- [ ] reviewer.md references subagents
- [ ] Subagents have `infer: true`
- [ ] BadAuthController.cs exists
- [ ] Copilot Chat is working
- [ ] Output panel accessible

---

## Troubleshooting

**If subagents don't invoke:**
1. Check `infer: true` in subagent files
2. Verify main agent mentions subagents by name
3. Reload VS Code window
4. Check Copilot extension is latest version

**If output is too fast to see:**
- Record demo with screen capture
- Show recording in slow motion
- Use Output panel for detailed view

---

## Time Allocation

- Setup: 1 min
- Part 1 (Autocomplete): 2 min
- Part 2 (Full invocation): 5 min
- Part 3 (Output panel): 2 min
- Part 4 (Manual attempt): 1 min
- Part 5 (Architecture): 1 min
- Q&A: 3 min

**Total: ~15 minutes with Q&A**

---

## Next Demo

After participants understand the invocation model, proceed to:
→ Demo 4: Subagent Code Review (Full Demo)
