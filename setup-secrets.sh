#!/bin/bash
# GitHub Secrets Configuration Script

set -e

echo "🔐 Configuring GitHub Secrets"
echo "=============================="
echo

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found"
    exit 1
fi

# Check if in a repo
if ! gh repo view &> /dev/null; then
    echo "❌ Not in a GitHub repository"
    echo "Run ./setup-github.sh first"
    exit 1
fi

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Repository: $REPO"
echo

# Function to set a secret
set_secret() {
    local secret_name=$1
    local secret_description=$2
    local is_optional=$3

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$secret_description"
    echo

    if [[ $is_optional == "optional" ]]; then
        read -p "Enter value (or press Enter to skip): " secret_value
        if [[ -z "$secret_value" ]]; then
            echo "⊘ Skipped"
            echo
            return
        fi
    else
        read -sp "Enter value: " secret_value
        echo

        while [[ -z "$secret_value" ]]; do
            echo "❌ This secret is required"
            read -sp "Enter value: " secret_value
            echo
        done
    fi

    echo "$secret_value" | gh secret set "$secret_name"

    if [ $? -eq 0 ]; then
        echo "✓ $secret_name configured"
    else
        echo "❌ Failed to set $secret_name"
    fi
    echo
}

echo "This script will configure the following secrets:"
echo "1. ANTHROPIC_API_KEY (required)"
echo "2. OPENAI_API_KEY (optional)"
echo "3. LINKEDIN_ACCESS_TOKEN (required for posting)"
echo "4. LINKEDIN_URN (required for posting)"
echo
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 0
fi
echo

# Set ANTHROPIC_API_KEY
set_secret "ANTHROPIC_API_KEY" \
    "🤖 ANTHROPIC_API_KEY (REQUIRED)
Get from: https://console.anthropic.com/settings/keys
Used for: Claude Code demo building + content generation" \
    "required"

# Set OPENAI_API_KEY
set_secret "OPENAI_API_KEY" \
    "🔑 OPENAI_API_KEY (OPTIONAL)
Get from: https://platform.openai.com/api-keys
Used for: Embeddings in demos (can use Anthropic instead)" \
    "optional"

# LinkedIn instructions
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 LinkedIn API Setup Required"
echo
echo "To post to LinkedIn, you need:"
echo "1. A LinkedIn App with Share on LinkedIn API access"
echo "2. An OAuth 2.0 access token"
echo "3. Your LinkedIn person URN"
echo
echo "See LINKEDIN_SETUP.md for detailed instructions"
echo
read -p "Do you have your LinkedIn credentials ready? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    set_secret "LINKEDIN_ACCESS_TOKEN" \
        "🔐 LINKEDIN_ACCESS_TOKEN
Your OAuth 2.0 access token with w_member_social scope" \
        "required"

    set_secret "LINKEDIN_URN" \
        "🆔 LINKEDIN_URN
Format: urn:li:person:YOUR_ID
Get from: curl -H 'Authorization: Bearer YOUR_TOKEN' https://api.linkedin.com/v2/me" \
        "required"
else
    echo "⊘ Skipping LinkedIn secrets (you can add them later)"
    echo "   Run: gh secret set LINKEDIN_ACCESS_TOKEN"
    echo "   Run: gh secret set LINKEDIN_URN"
fi

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Secrets configuration complete!"
echo

# List configured secrets
echo "Configured secrets:"
gh secret list

echo
echo "Next steps:"
echo "1. If you skipped LinkedIn, follow LINKEDIN_SETUP.md to get credentials"
echo "2. Go to your repo: https://github.com/$REPO"
echo "3. Navigate to: Actions → Daily RAG Showcase → Run workflow"
echo "4. Monitor the first run to verify everything works"
