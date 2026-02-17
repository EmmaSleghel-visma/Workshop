#!/bin/bash

# Workshop Setup Verification Script
# Run this before the workshop to verify everything is configured correctly

echo "=========================================="
echo "GitHub Copilot Workshop - Setup Verification"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2 - MISSING: $1"
        ((FAILED++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $2 - MISSING: $1"
        ((FAILED++))
    fi
}

echo "Checking directory structure..."
echo ""

# Check main directories
check_dir ".github" ".github folder exists"
check_dir ".github/agents" "Agents folder exists"
check_dir ".github/instructions" "Instructions folder exists"
check_dir ".github/skills" "Skills folder exists"
check_dir "backend" "Backend folder exists"
check_dir "DEMO-FILES" "Demo files folder exists"

echo ""
echo "Checking agent configuration files..."
echo ""

# Check agent files
check_file ".github/agents/reviewer.md" "Reviewer agent configured"
check_file ".github/agents/subagent-security.md" "Security subagent configured"
check_file ".github/agents/subagent-performance.md" "Performance subagent configured"

echo ""
echo "Checking instruction files..."
echo ""

# Check instruction files
check_file ".github/copilot-instructions.md" "Root copilot instructions"
check_file ".github/instructions/api.instructions.md" "API instructions"
check_file ".github/instructions/database.instructions.md" "Database instructions"

echo ""
echo "Checking skill files..."
echo ""

# Check skills
check_file ".github/skills/dotnet-api-testing/skill.md" "API testing skill"
check_file ".github/skills/dotnet-api-testing/templates/controller-test-template.cs" "Test template"

echo ""
echo "Checking demo files..."
echo ""

# Check demo files
check_file "DEMO-FILES/README.md" "Demo files README"
check_file "DEMO-FILES/BadAuthController.cs" "Security demo file"
check_file "DEMO-FILES/BadPerformanceService.cs" "Performance demo file"

echo ""
echo "Checking documentation..."
echo ""

# Check documentation
check_file "WORKSHOP-SETUP.md" "Workshop setup guide"
check_file "WORKSHOP-README.md" "Workshop README"

echo ""
echo "Verifying agent YAML front matter..."
echo ""

# Check for infer: true in subagents
if grep -q "infer: true" .github/agents/subagent-security.md 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Security subagent has 'infer: true'"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Security subagent missing 'infer: true'"
    ((FAILED++))
fi

if grep -q "infer: true" .github/agents/subagent-performance.md 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Performance subagent has 'infer: true'"
    ((PASSED++))
else
    echo -e "${RED}✗${NC} Performance subagent missing 'infer: true'"
    ((FAILED++))
fi

echo ""
echo "Checking .NET project..."
echo ""

# Check if backend builds
if [ -d "backend/CreditroDemo.API" ]; then
    echo "Attempting to build backend project..."
    cd backend/CreditroDemo.API

    if dotnet build > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Backend builds successfully"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} Backend build failed (may need 'dotnet restore')"
        echo "  Try running: cd backend/CreditroDemo.API && dotnet restore"
    fi

    cd ../..
else
    echo -e "${RED}✗${NC} Backend project not found"
    ((FAILED++))
fi

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo ""
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Workshop setup is complete.${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Read WORKSHOP-README.md for overview"
    echo "2. Review WORKSHOP-SETUP.md for detailed instructions"
    echo "3. Test Copilot agents in VS Code"
    echo "4. Practice demos from DEMO-FILES/README.md"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please review the issues above.${NC}"
    echo ""
    echo "Common fixes:"
    echo "- Ensure you're in the Workshop root directory"
    echo "- Run 'dotnet restore' in backend/CreditroDemo.API"
    echo "- Check that .github folder structure is correct"
    echo "- Verify YAML front matter in agent files"
    exit 1
fi
