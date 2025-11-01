#!/bin/bash
# GitHub Repository Setup Script

set -e

echo "🚀 Setting up RAG Showroom on GitHub"
echo "====================================="
echo

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found"
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

echo "✓ GitHub CLI found"

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Please authenticate with GitHub:"
    gh auth login
fi

echo "✓ GitHub authenticated"
echo

# Get repository details
echo "Repository Configuration:"
echo "-------------------------"
read -p "Repository name [rag-showroom]: " REPO_NAME
REPO_NAME=${REPO_NAME:-rag-showroom}

read -p "Make repository public? (y/n) [y]: " IS_PUBLIC
IS_PUBLIC=${IS_PUBLIC:-y}

if [[ $IS_PUBLIC == "y" ]]; then
    VISIBILITY="--public"
else
    VISIBILITY="--private"
fi

echo

# Initialize git if not already
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✓ Git initialized"
fi

# Create .gitignore if missing
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
.env

# Node
node_modules/

# Outputs
outputs/
!outputs/.gitkeep

# IDE
.vscode/
.idea/
EOF
fi

# Stage and commit
echo "📝 Creating initial commit..."
git add .
git commit -m "feat: initial RAG Showroom automation system

- Complete pipeline automation (pattern selection → build → test → post)
- 10 RAG patterns queued (semantic-chunking demo included)
- GitHub Actions workflow for daily execution
- LinkedIn API integration for posting
- Rich ASCII art terminal visualization" || echo "Files already committed"

echo "✓ Initial commit ready"
echo

# Create repository
echo "🌐 Creating GitHub repository..."
gh repo create "$REPO_NAME" $VISIBILITY --source=. --remote=origin --push

if [ $? -eq 0 ]; then
    echo "✓ Repository created and pushed!"
    echo
    echo "Repository URL: https://github.com/$(gh repo view --json owner,name -q '.owner.login + "/" + .name')"
else
    echo "❌ Failed to create repository"
    exit 1
fi

echo
echo "✅ GitHub setup complete!"
echo
echo "Next steps:"
echo "1. Run ./setup-secrets.sh to configure API keys"
echo "2. Follow LINKEDIN_SETUP.md to get LinkedIn credentials"
echo "3. Test the workflow manually from GitHub Actions"
