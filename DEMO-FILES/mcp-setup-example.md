# MCP Setup Demo

## Overview
This guide demonstrates how to set up and use Model Context Protocol (MCP) servers with GitHub Copilot.

## What is MCP?
Model Context Protocol allows GitHub Copilot to connect to external tools, databases, and data sources. Think of it as giving Copilot superpowers to access your real-world systems.

## Demo Scenario: GitHub MCP Server

### 1. Prerequisites
- VS Code with GitHub Copilot installed
- GitHub CLI (`gh`) installed and authenticated
- Copilot Enterprise license

### 2. Installation

#### Option A: Using VS Code Settings
1. Open VS Code Settings (Cmd/Ctrl + ,)
2. Search for "MCP"
3. Click "Edit in settings.json"
4. Add MCP configuration (see example below)

#### Option B: Manual Configuration
Create or edit `.vscode/mcp.json` in your workspace:

```json
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
```

### 3. Demo Script

**Step 1: Verify Connection**
```
In Copilot Chat:
"Are you connected to any MCP servers?"

Expected: Copilot should confirm GitHub MCP server is available
```

**Step 2: Query GitHub Issues**
```
In Copilot Chat:
"Show me open issues in this repository"

Expected: Copilot uses GitHub MCP to fetch and display issues
```

**Step 3: Create an Issue**
```
In Copilot Chat:
"Create a new issue titled 'Add input validation to CustomersController' with a description about missing email validation"

Expected: Copilot creates the issue via GitHub API
```

**Step 4: Check Pull Requests**
```
In Copilot Chat:
"What pull requests are currently open? Summarize each one."

Expected: Copilot fetches PRs and provides summaries
```

### 4. Common MCP Servers to Demo

#### Filesystem MCP Server
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/directory"]
    }
  }
}
```

**Demo**: "List all .cs files in the Controllers directory and tell me which ones don't have XML documentation"

#### Postgres MCP Server
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    }
  }
}
```

**Demo**: "What tables exist in the database? Show me the schema for the Customers table"

#### Slack MCP Server
```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    }
  }
}
```

**Demo**: "Check #engineering channel for any mentions of the customer API in the last week"

### 5. Security Demo

**⚠️ IMPORTANT: Security Considerations**

Show attendees the warning signs:

1. **Token Consumption Warning**
```
Copilot Chat:
"Explain the structure of this codebase"

With GitHub MCP connected, this query consumes ~29,000 tokens!
Without MCP, it consumes ~2,000 tokens.
```

2. **Trust Verification**
- Only use MCP servers from trusted sources
- Verify the npm package or source code
- Check what data the server exposes
- Review permissions required

3. **Data Exposure Demo**
```
# Bad Example - Exposes everything
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/"]
    }
  }
}

# Good Example - Limited scope
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}/src"]
    }
  }
}
```

### 6. Troubleshooting

**MCP Server Not Connecting**
```bash
# Check if MCP server is running
# VS Code Output panel → MCP Logs

# Verify npm package exists
npx -y @modelcontextprotocol/server-github --version

# Check environment variables
echo $GITHUB_TOKEN
```

**Server Crashes or Errors**
- Check VS Code Developer Tools (Help → Toggle Developer Tools)
- Look for MCP-related errors in Console
- Verify JSON syntax in mcp.json

### 7. MCP Registry Demo

Show the MCP Registry at: https://github.com/modelcontextprotocol/servers

Popular servers to explore:
- `@modelcontextprotocol/server-github` - GitHub integration
- `@modelcontextprotocol/server-gitlab` - GitLab integration
- `@modelcontextprotocol/server-postgres` - PostgreSQL database
- `@modelcontextprotocol/server-sqlite` - SQLite database
- `@modelcontextprotocol/server-filesystem` - File system access
- `@modelcontextprotocol/server-slack` - Slack integration
- `@modelcontextprotocol/server-google-drive` - Google Drive access

### 8. Hands-On Exercise

**Exercise**: Set up a GitHub MCP server and use it to:
1. List all open issues in the repository
2. Find issues assigned to you
3. Create a new issue for a bug you found
4. Check the status of recent pull requests

**Time**: 10 minutes

### 9. Discussion Points

- When would you use MCP in your workflow?
- What concerns do you have about token consumption?
- What other tools would you want MCP servers for?
- How do you balance convenience vs. security?

## Resources

- MCP Documentation: https://modelcontextprotocol.io/
- MCP Registry: https://github.com/modelcontextprotocol/servers
- GitHub Copilot MCP Guide: https://docs.github.com/en/copilot/using-github-copilot/using-extensions/using-mcp-servers-in-github-copilot
