#!/bin/bash
# Master setup script for online automation

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 RAG Showroom - Complete Online Setup                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo

# Check prerequisites
echo "Checking prerequisites..."
echo "-------------------------"

# Check gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found"
    echo "Install from: https://cli.github.com/"
    exit 1
fi
echo "✓ GitHub CLI"

# Check Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python not found"
        exit 1
    fi
    PYTHON_CMD=python
else
    PYTHON_CMD=python3
fi
echo "✓ Python ($($PYTHON_CMD --version))"

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found"
    exit 1
fi
echo "✓ Node.js ($(node --version))"

echo

# Step 1: GitHub Repository
echo "════════════════════════════════════════════════════════════"
echo "STEP 1: GitHub Repository Setup"
echo "════════════════════════════════════════════════════════════"
echo

if gh repo view &> /dev/null; then
    echo "✓ Repository already exists"
    REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
    echo "  Repository: $REPO"
else
    echo "Setting up GitHub repository..."
    chmod +x setup-github.sh
    ./setup-github.sh
fi

echo

# Step 2: LinkedIn Credentials
echo "════════════════════════════════════════════════════════════"
echo "STEP 2: LinkedIn API Setup"
echo "════════════════════════════════════════════════════════════"
echo
echo "You need LinkedIn API credentials to enable automated posting."
echo
read -p "Do you have LinkedIn API credentials ready? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "✓ Great! We'll configure them in the next step."
else
    echo
    echo "📖 LinkedIn setup is required for automated posting."
    echo
    echo "Two options:"
    echo
    echo "1. Follow LINKEDIN_SETUP.md for detailed instructions"
    echo "2. Run the helper script: python scripts/linkedin_oauth.py"
    echo
    read -p "Would you like to run the LinkedIn OAuth helper now? (y/n) " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo
        echo "Installing required Python package..."
        $PYTHON_CMD -m pip install requests --quiet
        echo
        $PYTHON_CMD scripts/linkedin_oauth.py
        echo
    else
        echo
        echo "⏭️  Skipping LinkedIn setup for now"
        echo "   You can run it later: python scripts/linkedin_oauth.py"
        echo
    fi
fi

echo

# Step 3: GitHub Secrets
echo "════════════════════════════════════════════════════════════"
echo "STEP 3: Configure GitHub Secrets"
echo "════════════════════════════════════════════════════════════"
echo

chmod +x setup-secrets.sh
./setup-secrets.sh

echo

# Step 4: Test Workflow
echo "════════════════════════════════════════════════════════════"
echo "STEP 4: Test GitHub Actions Workflow"
echo "════════════════════════════════════════════════════════════"
echo

read -p "Trigger a test workflow run now? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo
    echo "Triggering workflow..."
    gh workflow run daily-showcase.yml

    if [ $? -eq 0 ]; then
        echo "✅ Workflow triggered!"
        echo
        echo "Monitor progress:"
        echo "  gh run watch"
        echo "  or visit: https://github.com/$REPO/actions"
        echo
        sleep 2
        echo "Opening browser..."
        gh workflow view daily-showcase.yml --web
    else
        echo "❌ Failed to trigger workflow"
    fi
else
    echo "⏭️  Skipped test run"
fi

echo
echo "════════════════════════════════════════════════════════════"
echo "✅ Setup Complete!"
echo "════════════════════════════════════════════════════════════"
echo
echo "Your RAG Showroom is now set up for automated operation!"
echo
echo "📅 Schedule:"
echo "   - Runs daily at 9:00 AM UTC"
echo "   - Builds one RAG pattern demo per day"
echo "   - Posts results to LinkedIn automatically"
echo
echo "🎯 Next Steps:"
echo "   1. Monitor your first workflow run"
echo "   2. Check LinkedIn for the posted demo"
echo "   3. Review outputs in the repo under outputs/"
echo
echo "📊 Useful Commands:"
echo "   - Check status: ./scripts/check_workflow.sh"
echo "   - Manual trigger: gh workflow run daily-showcase.yml"
echo "   - View runs: gh run list"
echo "   - Watch run: gh run watch"
echo
echo "📚 Documentation:"
echo "   - SETUP.md - Full setup guide"
echo "   - LINKEDIN_SETUP.md - LinkedIn API details"
echo "   - CLAUDE.md - Development guidance"
echo
echo "🌟 Pattern Queue: 10 RAG patterns ready to showcase"
echo "   First up: semantic-chunking (already built as demo)"
echo
echo "════════════════════════════════════════════════════════════"
