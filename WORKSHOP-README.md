# GitHub Copilot Ultimate Workshop

**Welcome!** This repository contains everything you need for the full-day GitHub Copilot Advanced Features workshop.

## 📁 Repository Structure

```
Workshop/
├── .github/                          ← Copilot Configuration
│   ├── agents/                       ← Custom AI agents
│   │   ├── reviewer.md               ← Main code reviewer agent
│   │   ├── subagent-security.md      ← Security vulnerability checker
│   │   └── subagent-performance.md   ← Performance analyzer
│   ├── instructions/                 ← Project-specific instructions
│   │   ├── copilot-instructions.md   ← Repo-level instructions
│   │   ├── api.instructions.md       ← API development guidelines
│   │   └── database.instructions.md  ← Database & models guidelines
│   └── skills/                       ← Reusable AI skills
│       └── dotnet-api-testing/       ← API testing skill
│           ├── skill.md              ← Skill definition
│           └── templates/            ← Code templates
│
├── .copilot-personal-example/        ← Personal skills example
│   └── skills/                       ← Copy to ~/.copilot/skills/
│       └── code-review-checklist/    ← Personal review standards
│
├── backend/                          ← .NET 8 API
│   └── CreditroDemo.API/
│       ├── Controllers/              ← API endpoints
│       ├── Services/                 ← Business logic
│       └── Models/                   ← Data models
│
├── frontend/                         ← Angular 21 app
│   └── src/
│
├── DEMO-FILES/                       ← Workshop demo code
│   ├── README.md                     ← Demo instructions
│   ├── BadAuthController.cs          ← Security vulnerabilities demo
│   └── BadPerformanceService.cs      ← Performance issues demo
│
└── WORKSHOP-SETUP.md                 ← Setup guide (START HERE!)
```

---

## 🚀 Quick Start

### 1. Read Setup Guide First!
👉 **[WORKSHOP-SETUP.md](WORKSHOP-SETUP.md)** - Complete setup instructions

### 2. Verify Prerequisites
- ✅ VS Code installed
- ✅ GitHub Copilot extensions
- ✅ .NET 8 SDK
- ✅ Git 2.5+
- ✅ Copilot Enterprise license

### 3. Clone & Build
```bash
git clone [REPO_URL]
cd Workshop/backend/CreditroDemo.API
dotnet restore
dotnet build
```

### 4. Test Your Setup
```bash
# Open VS Code
code .

# In VS Code:
# 1. Open any .cs file
# 2. Try inline suggestions (start typing)
# 3. Open Copilot Chat (Ctrl/Cmd + Shift + I)
# 4. Type: @reviewer
# 5. ✅ Should auto-complete!
```

---

## 📚 Workshop Materials

### Presentations (in parent folder)
- **GitHub_Copilot_Ultimate_Workshop.pptx** - Main presentation (30 slides)
- **Workshop_Plan_Ultimate.md** - Detailed session plan with demos

### Configuration Files (Ready to Use!)
All files in `.github/` are pre-configured:
- **Custom Agents**: @reviewer, @subagent-security, @subagent-performance
- **Custom Instructions**: API and database coding standards
- **Skills**: /dotnet-api-testing for generating tests

### Demo Files
- **DEMO-FILES/README.md** - How to use demo files
- **BadAuthController.cs** - Security vulnerabilities (intentional!)
- **BadPerformanceService.cs** - Performance issues (intentional!)

---

## 🎯 What You'll Learn

### Morning Sessions (09:00 - 13:00)

**Session 1: What's New Timeline**
- 10-month evolution overview
- Feature comparison: April 2025 vs February 2026
- Why VS Code is the best choice

**Session 2: Context Control ⭐ MOST CRUCIAL**
- 4 sources of context
- Manual file linking with #file
- 5-layer customization hierarchy

**Session 3: Multi-Agent Architecture**
- Local agents (fast, in VS Code)
- Background agents (non-blocking, parallel)
- Cloud agents (GitHub-hosted, full environment)

**Session 4: Subagents & Remote Delegation**
- Context-isolated subagents
- Parallel execution (January 2026)
- Cloud agent delegation
- Working trees integration

**Session 5: Advanced Features**
- Copilot Workspace (issue-to-PR)
- Next Edit Suggestions (TAB navigation)
- Agent Skills (slash commands)
- Agentic Workflows (CI/CD in Markdown)
- Copilot Memories (VS 2026)

### Afternoon Labs (13:30 - 16:00)

**Lab 1: Multi-Agent Mastery (60 min)**
- Configure all three agent types
- Create custom agent with subagents
- Practice cloud delegation
- Explore working trees

**Lab 2: Copilot Workspace & Skills (45 min)**
- Issue-to-PR workflow
- Create project skills
- Create personal skills
- Test skill invocations

**Lab 3: Team Discussion (30 min)**
- Share experiences
- Real-world applications
- Next steps planning

---

## 🔧 Key Features Demonstrated

### 🆕 January 2026 Features
- ✨ **Multi-Agent Architecture** - Local, Background, Cloud
- ⚡ **Parallel Subagents** - Multiple reviews simultaneously
- 🎯 **Agent Skills** - Slash commands for workflows
- 🧠 **Copilot Memories** - Auto-learns coding standards (VS 2026)

### 🆕 February 2026 Features
- 📝 **Agentic Workflows** - CI/CD in Markdown
- ⌨️ **Next Edit Suggestions** - TAB-based code navigation
- 🏗️ **Copilot Workspace** - Full agentic dev environment

### October 2025 Features
- 📋 **Plan Mode** - Review before execution
- 🤖 **Subagents** - Context-isolated agents

### December 2025 Features
- 🎨 **Multi-Model Support** - GPT-5.1, Claude Opus 4.5, Gemini 3 Pro

---

## 💡 Usage Examples

### Example 1: Using Custom Agents

```plaintext
In Copilot Chat:

You: @reviewer please review CustomersController.cs

Copilot (reviewer agent):
  - Analyzing code...
  - Invoking @subagent-security for security review...
  - Invoking @subagent-performance for performance review...

@subagent-security found:
  🔴 Missing [Authorize] attribute on line 42
  🟡 No input validation on CreateCustomer endpoint

@subagent-performance found:
  🔴 N+1 query problem on line 67
  🟠 Missing async/await on line 89

Consolidated Review:
  [Detailed recommendations with code examples...]
```

### Example 2: Using Skills

```plaintext
In Copilot Chat:

You: /dotnet-api-testing for CustomersController

Copilot:
  Generating comprehensive test suite...

  ✅ Created: CustomersControllerTests.cs
     - GetAll_ReturnsOkResult_WithListOfCustomers
     - GetById_ValidId_ReturnsOkResult
     - GetById_InvalidId_ReturnsNotFound
     - Create_ValidRequest_ReturnsCreatedResult
     - Create_InvalidModel_ReturnsBadRequest
     [+ 15 more tests...]
```

### Example 3: Cloud Agent Delegation

```plaintext
In your code:

// TODO: Implement JWT token refresh functionality

[Hover over TODO → Code Action appears]
[Click: "Delegate to Coding Agent"]

Cloud Agent:
  ✓ Creating isolated environment...
  ✓ Analyzing requirements...
  ✓ Implementing RefreshTokenController...
  ✓ Adding token validation middleware...
  ✓ Writing unit tests...
  ✓ Running tests... All passed ✓
  ✓ Creating PR #42...

Result: Full feature implemented with tests in 3 minutes!
```

---

## 🎓 Learning Paths

### Beginner Track
If you're new to GitHub Copilot:
1. Start with basic inline suggestions
2. Practice Copilot Chat
3. Learn context control (Session 2)
4. Try local agents only

### Intermediate Track
If you've used Copilot before:
1. Skip basic features
2. Focus on multi-agent architecture
3. Master context control
4. Practice cloud agent delegation

### Advanced Track
If you're a Copilot power user:
1. Jump to advanced features
2. Create custom agents immediately
3. Build skills library
4. Experiment with agentic workflows

---

## 📖 Additional Resources

### Official Documentation
- **GitHub Copilot**: https://docs.github.com/copilot
- **VS Code Copilot**: https://code.visualstudio.com/docs/copilot
- **Agent Skills**: https://docs.github.com/copilot/concepts/agents/about-agent-skills
- **Agentic Workflows**: https://github.github.io/gh-aw

### Community
- **Awesome Copilot**: https://github.com/github/awesome-copilot
- **Discussions**: https://github.com/orgs/community/discussions
- **Skills Repository**: https://github.com/anthropics/skills

### Research & Articles
- **Subagents Deep Dive**: https://medium.com/@xorets/using-github-copilot-subagents
- **Multi-Agent Development**: https://code.visualstudio.com/blogs/2025/11/03/unified-agent-experience
- **VS Code January 2026 Update**: https://alexop.dev/posts/whats-new-vscode-copilot-january-2026/

---

## 🐛 Troubleshooting

### Common Issues

**Copilot Not Working**
```bash
# Check sign-in status
# Bottom-left corner of VS Code → Should show GitHub username

# Re-sign in if needed
F1 → "GitHub Copilot: Sign Out"
F1 → "GitHub Copilot: Sign In"
```

**Agents Not Appearing**
```bash
# Verify folder structure
ls .github/agents/

# Reload VS Code
F1 → "Developer: Reload Window"

# Check agent configuration
# Open .github/agents/reviewer.md
# Verify YAML front matter is correct
```

**Skills Not Working**
```bash
# Check folder structure
ls .github/skills/dotnet-api-testing/

# Must have:
# - skill.md (with YAML front matter)
# - Front matter must include: name, description

# Reload window
F1 → "Developer: Reload Window"
```

**Subagents Not Triggering**
```bash
# Check subagent files have:
# infer: true

# In .github/agents/subagent-security.md:
---
name: subagent-security
description: Security review
infer: true    ← Must have this!
---
```

For more troubleshooting: See [WORKSHOP-SETUP.md](WORKSHOP-SETUP.md#troubleshooting)

---

## 👥 Getting Help

### During Workshop
- Raise your hand
- Ask in team chat
- Check with neighbor
- Flag instructor

### After Workshop
- GitHub Community Discussions
- Workshop materials repository
- Instructor email (provided during workshop)

---

## ✅ Pre-Workshop Checklist

Print this and bring it to the workshop:

```
□ VS Code installed (latest stable)
□ GitHub Copilot extensions installed
□ GitHub Copilot Chat extension installed
□ .NET 8 SDK installed
□ Git 2.5+ installed
□ Signed into GitHub in VS Code
□ Copilot Enterprise license verified
□ Workshop repository cloned
□ Backend builds successfully (dotnet build)
□ Can see inline suggestions
□ Copilot Chat responds
□ Can see session type dropdown
□ @reviewer agent auto-completes
□ Notebook for taking notes
□ Questions prepared
```

---

## 📝 Workshop Notes Space

Use this space during the workshop:

**Key Learnings**:
```
Session 1:


Session 2:


Session 3:


Lab 1:


Lab 2:

```

**Questions to Ask**:
```
1.

2.

3.
```

**Features to Try After Workshop**:
```
□
□
□
```

---

## 🎉 Let's Get Started!

1. **Read** [WORKSHOP-SETUP.md](WORKSHOP-SETUP.md) thoroughly
2. **Verify** all prerequisites are met
3. **Clone** this repository
4. **Test** your setup
5. **Come prepared** with questions

See you at the workshop! 🚀

---

**Workshop Version**: 2.0 (Ultimate Edition)
**Last Updated**: February 17, 2026
**Duration**: Full Day (8:30 AM - 4:00 PM)
**Format**: Theory-heavy morning + Hands-on afternoon

**Questions before the workshop?**
Contact: [Your Email]
