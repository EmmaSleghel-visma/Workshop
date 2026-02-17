# GitHub Copilot Ultimate Workshop - Setup Guide

## Pre-Workshop Setup (1 Day Before)

Send this section to all participants 24 hours before the workshop.

---

### Required Software

#### 1. Visual Studio Code
- **Version**: Latest stable (NOT Insiders for this workshop)
- **Download**: https://code.visualstudio.com/
- **Why**: VS Code has the best Copilot experience with all latest features

#### 2. GitHub Copilot Extensions
Install these extensions in VS Code:

```
1. GitHub Copilot (github.copilot)
2. GitHub Copilot Chat (github.copilot-chat)
3. GitHub Pull Requests (github.vscode-pull-request-github) - Optional but recommended
```

**Installation**:
- Open VS Code
- Go to Extensions (Ctrl/Cmd + Shift + X)
- Search for "GitHub Copilot"
- Install both Copilot and Copilot Chat extensions

#### 3. .NET SDK
- **Version**: .NET 8.0 or later
- **Download**: https://dotnet.microsoft.com/download
- **Verify**: Run `dotnet --version` in terminal

#### 4. Git
- **Version**: 2.5+ (for working trees support)
- **Download**: https://git-scm.com/downloads
- **Verify**: Run `git --version` in terminal

---

### GitHub Account Setup

#### 1. Verify Copilot Enterprise License
- Log in to https://github.com
- Go to Settings → Copilot
- Verify you have "Copilot Enterprise" access
- This is REQUIRED for multi-agent features

#### 2. Check Feature Access
- Open VS Code
- Sign in with your GitHub account (bottom left corner)
- Open Copilot Chat (Ctrl/Cmd + Shift + I)
- Verify you see:
  - Agent mode toggle
  - Model selection dropdown (GPT-5.1, Claude Opus 4.5, Gemini 3 Pro)
  - Session type selector (Local, Background, Cloud)

---

### Workshop Repository Setup

#### 1. Clone the Workshop Repository

```bash
git clone [WORKSHOP_REPO_URL]
cd Workshop
```

#### 2. Verify Repository Structure

Your Workshop folder should contain:
```
Workshop/
├── .github/
│   ├── agents/
│   │   ├── reviewer.md
│   │   ├── subagent-security.md
│   │   └── subagent-performance.md
│   ├── instructions/
│   │   ├── api.instructions.md
│   │   └── database.instructions.md
│   ├── skills/
│   │   └── dotnet-api-testing/
│   └── copilot-instructions.md
├── backend/
│   └── CreditroDemo.API/
├── frontend/
├── DEMO-FILES/
│   ├── BadAuthController.cs
│   ├── BadPerformanceService.cs
│   └── README.md
└── README.md
```

#### 3. Restore Backend Dependencies

```bash
cd backend/CreditroDemo.API
dotnet restore
dotnet build
```

Verify no build errors.

---

### Copilot Configuration Verification

#### 1. Test Basic Copilot
1. Open any .cs file in the project
2. Start typing a comment: `// Calculate the sum of`
3. Wait for inline suggestion
4. Press Tab to accept
5. ✅ If you see suggestions, basic Copilot works!

#### 2. Test Copilot Chat
1. Open Copilot Chat (Ctrl/Cmd + Shift + I)
2. Type: "What does this project do?"
3. ✅ Should get a response about the Creditro Demo API

#### 3. Test Agent Mode
1. In Copilot Chat, look for session type dropdown
2. Should see options: Local, Background, Cloud
3. ✅ If you see these, multi-agent is available!

#### 4. Test Custom Agent
1. In Copilot Chat, type: `@reviewer`
2. Press space
3. ✅ Should see auto-complete with your custom reviewer agent

---

### Optional: Personal Skills Setup

If you want to practice with personal skills:

#### 1. Copy Personal Skills Example

**Windows**:
```powershell
mkdir $env:USERPROFILE\.copilot\skills
xcopy .copilot-personal-example\skills $env:USERPROFILE\.copilot\skills /E /I
```

**Mac/Linux**:
```bash
mkdir -p ~/.copilot/skills
cp -r .copilot-personal-example/skills/* ~/.copilot/skills/
```

#### 2. Verify Personal Skills
1. In Copilot Chat, type: `/`
2. Press Tab
3. ✅ Should see your personal skills in the list

---

### Troubleshooting

#### Issue: Copilot Extension Not Working
**Symptoms**: No inline suggestions, chat not responding

**Solution**:
1. Check GitHub sign-in (bottom left in VS Code)
2. Verify Copilot license at github.com/settings/copilot
3. Restart VS Code
4. Try `F1` → "GitHub Copilot: Sign Out" → Sign back in

---

#### Issue: Multi-Agent Features Not Available
**Symptoms**: No session type dropdown, can't select Background/Cloud

**Solution**:
1. Verify you have Copilot Enterprise (NOT just Pro)
2. Update VS Code to latest version
3. Update Copilot extensions to latest
4. Restart VS Code

---

#### Issue: Custom Agents Not Appearing
**Symptoms**: `@reviewer` not auto-completing

**Solution**:
1. Verify `.github/agents/` folder exists in workspace
2. Check `reviewer.md` file format (YAML front matter)
3. Reload VS Code window (F1 → "Reload Window")
4. Try typing `@` again in chat

---

#### Issue: Subagents Not Working
**Symptoms**: Reviewer doesn't invoke subagents

**Solution**:
1. Check `infer: true` is set in subagent .md files
2. Verify subagent names match references in reviewer.md
3. Try explicit command: `@subagent-security review this code`

---

#### Issue: Skills Not Appearing in / Menu
**Symptoms**: `/` menu doesn't show custom skills

**Solution**:
1. Check skill folder structure (`.github/skills/[skill-name]/skill.md`)
2. Verify YAML front matter in skill.md
3. Reload VS Code window
4. Update Copilot Chat extension

---

## Instructor Setup (Day Before Workshop)

### 1. Presentation & Materials
- [ ] Load GitHub_Copilot_Ultimate_Workshop.pptx
- [ ] Print Workshop_Plan_Ultimate.md for reference
- [ ] Have backup PDF of presentation
- [ ] Test all demos in sequence

### 2. Demo Environment
- [ ] Clone workshop repo to clean directory
- [ ] Verify all demo files work
- [ ] Test `@reviewer` agent with demo files
- [ ] Confirm subagents trigger automatically
- [ ] Test cloud agent delegation (if available)

### 3. Lab Materials
- [ ] Prepare lab instructions handouts (optional)
- [ ] Have troubleshooting guide ready
- [ ] Setup checklist printed for participants

### 4. Technical Checks
- [ ] Projector/screen working
- [ ] VS Code displayed clearly
- [ ] Terminal font size readable (18-20pt minimum)
- [ ] Internet connection stable (for cloud agents)
- [ ] Backup internet (mobile hotspot)

### 5. Accounts & Access
- [ ] GitHub logged in and working
- [ ] Copilot Enterprise features verified
- [ ] Can delegate to cloud agents
- [ ] All subagents working

---

## Day-of Workshop Setup

### Participant Check-in (08:00 - 08:30)

#### Quick Verification Checklist
Have each participant verify:

1. ✅ VS Code installed and updated
2. ✅ GitHub Copilot extensions installed
3. ✅ Signed into GitHub in VS Code
4. ✅ Repository cloned and built successfully
5. ✅ Can see Copilot inline suggestions
6. ✅ Copilot Chat responding
7. ✅ Can see session type dropdown (Local/Background/Cloud)
8. ✅ `@reviewer` agent auto-completes

#### Common Issues During Check-in

**Quick Fixes**:
- Not signed in → Sign in via bottom-left corner
- No suggestions → Restart VS Code
- Build errors → `dotnet restore` in backend folder
- Can't see agents → Reload window (F1 → Reload Window)

---

## Workshop Session Setup

### Session 1: Welcome + IDE Setup (08:30 - 09:00)

**Instructor Actions**:
1. Welcome participants
2. Quick poll: Who has used Copilot before?
3. Verify everyone has setup working
4. Brief overview of day's agenda

**Participant Actions**:
1. Open VS Code with Workshop folder
2. Verify all features working
3. Ask questions about setup issues
4. Get comfortable with VS Code interface

---

### Between Sessions

**Instructor**:
- Verify demo files are ready for next session
- Check time is on track
- Answer any lingering questions

**Participants**:
- Take notes on key learnings
- Practice commands shown
- Experiment during breaks

---

## Lab Setup

### Lab 1: Multi-Agent Mastery (13:30 - 14:30)

**Prerequisites**:
- Workshop repo cloned ✅
- Custom agents configured ✅
- Can access all three agent types ✅

**Verification**:
```bash
# Check agent files exist
ls .github/agents/

# Should see:
# reviewer.md
# subagent-security.md
# subagent-performance.md
```

---

### Lab 2: Copilot Workspace & Skills (14:45 - 15:30)

**Prerequisites**:
- Lab 1 completed ✅
- Skills folder accessible ✅
- GitHub account with Workspace access ✅

**Verification**:
```bash
# Check skills folder
ls .github/skills/

# Should see:
# dotnet-api-testing/
```

---

## Post-Workshop

### Participant Next Steps
1. Keep Workshop folder for reference
2. Copy custom agents to your projects
3. Create your own skills
4. Experiment with cloud agents
5. Share learnings with your team

### Instructor Follow-up
1. Share presentation slides
2. Send additional resources document
3. Collect feedback via survey
4. Address any remaining questions

---

## Emergency Contacts & Resources

### During Workshop Issues

**Copilot Not Working**:
1. Try participant's neighbor's machine
2. Use instructor's machine for demo
3. Show screen recording if needed

**Internet Outage**:
- Switch to mobile hotspot
- Focus on local agent features only
- Skip cloud agent demos if necessary

**Project Won't Build**:
- Provide pre-built version
- Use DEMO-FILES only for examples
- Continue with other participants

### Resources

- GitHub Copilot Documentation: https://docs.github.com/copilot
- VS Code Copilot Features: https://code.visualstudio.com/docs/copilot
- Community Discussions: https://github.com/orgs/community/discussions
- Workshop Materials: [INSERT YOUR LINK]

---

## Quick Reference Card

Print this for each participant:

```
╔══════════════════════════════════════════════════════════════╗
║          GITHUB COPILOT WORKSHOP - QUICK REFERENCE           ║
╚══════════════════════════════════════════════════════════════╝

KEYBOARD SHORTCUTS:
  Ctrl/Cmd + I          Inline Chat
  Ctrl/Cmd + Shift + I  Open Chat Sidebar
  Tab                   Accept suggestion
  Esc                   Dismiss suggestion

CHAT COMMANDS:
  @reviewer             Invoke custom reviewer agent
  @subagent-security    Security review subagent
  @subagent-performance Performance review subagent
  /dotnet-api-testing   API testing skill
  /skills               Configure skills
  /clear                Clear chat context

CONTEXT CONTROL:
  #file                 Reference specific file
  @workspace            Search entire workspace
  Reload VS Code        Clear Copilot memory

SESSION TYPES:
  Local                 Fast, in VS Code
  Background            Non-blocking, parallel work
  Cloud                 GitHub-hosted, full environment

AGENT WORKFLOW:
  1. Open file or use #file
  2. Type @reviewer in chat
  3. Describe what to review
  4. Subagents run automatically
  5. Review consolidated feedback
  6. Ask for fixes

TROUBLESHOOTING:
  No suggestions?       Check sign-in status
  Agents not working?   Reload window (F1 → Reload)
  Chat not responding?  Check internet connection
  Build errors?         Run: dotnet restore

RESOURCES:
  Docs: https://docs.github.com/copilot
  Community: github.com/orgs/community/discussions

╔══════════════════════════════════════════════════════════════╗
║  Questions? Ask the instructor or check WORKSHOP-SETUP.md    ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Success Metrics

### Immediate (End of Session 1)
- [ ] All participants have Copilot working
- [ ] Everyone can see inline suggestions
- [ ] Chat is responding for all
- [ ] Custom agents are accessible

### By Lunch (12:00)
- [ ] All participants tested multi-agent architecture
- [ ] Everyone has invoked subagents
- [ ] Context control concepts understood
- [ ] Customization hierarchy set up

### End of Day (16:00)
- [ ] Everyone completed Lab 1 (Multi-Agent Mastery)
- [ ] Everyone completed Lab 2 (Workspace & Skills)
- [ ] All participants can delegate to cloud agents
- [ ] Custom skills created and working

---

## Feedback Collection

### During Workshop
- Check understanding after each major concept
- Ask for show of hands: "Who's following along?"
- Address confusion immediately

### End of Day Survey
Questions to ask:
1. How would you rate the workshop overall? (1-5)
2. Which feature was most impressive?
3. What will you implement first?
4. Any topics that need more coverage?
5. Technical difficulty level (too easy/just right/too hard)?
6. Would you recommend to colleagues?

---

**Workshop Materials Version**: 2.0 (Ultimate Edition)
**Last Updated**: February 17, 2026
**Next Review**: After workshop completion
