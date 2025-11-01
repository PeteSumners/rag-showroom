#!/bin/bash
# Workflow status checker

echo "📊 Checking GitHub Actions Workflow Status"
echo "==========================================="
echo

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found"
    exit 1
fi

# Check if in a repo
if ! gh repo view &> /dev/null; then
    echo "❌ Not in a GitHub repository"
    exit 1
fi

REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Repository: $REPO"
echo

# Get workflow runs
echo "Recent workflow runs:"
echo "--------------------"

gh run list --workflow="daily-showcase.yml" --limit 5 --json conclusion,status,createdAt,headBranch,displayTitle | \
  python3 -c "
import json, sys
runs = json.load(sys.stdin)
for run in runs:
    status = run['status']
    conclusion = run.get('conclusion', 'in_progress')
    title = run['displayTitle']
    date = run['createdAt'][:10]

    if conclusion == 'success':
        icon = '✅'
    elif conclusion == 'failure':
        icon = '❌'
    elif status == 'in_progress':
        icon = '🔄'
    else:
        icon = '⏸️'

    print(f'{icon} {date} - {title} ({conclusion})')
"

echo
echo "--------------------"
echo

# Check secrets
echo "Configured secrets:"
echo "-------------------"

secrets=$(gh secret list --json name -q '.[].name')

required_secrets=("ANTHROPIC_API_KEY" "LINKEDIN_ACCESS_TOKEN" "LINKEDIN_URN")

for secret in "${required_secrets[@]}"; do
    if echo "$secrets" | grep -q "^$secret$"; then
        echo "✓ $secret"
    else
        echo "✗ $secret (missing)"
    fi
done

# Optional secrets
if echo "$secrets" | grep -q "^OPENAI_API_KEY$"; then
    echo "✓ OPENAI_API_KEY (optional)"
else
    echo "○ OPENAI_API_KEY (optional, not set)"
fi

echo
echo "--------------------"
echo

# Check next scheduled run
echo "Next scheduled run:"
echo "-------------------"
echo "Daily at 9:00 AM UTC"
echo "Current UTC time: $(date -u +"%Y-%m-%d %H:%M:%S")"
echo

# Manual trigger info
echo "Manual trigger:"
echo "---------------"
echo "Run: gh workflow run daily-showcase.yml"
echo "Or visit: https://github.com/$REPO/actions/workflows/daily-showcase.yml"
echo

# Check pattern queue
echo "Pattern queue status:"
echo "---------------------"

if [ -f "queue/patterns.json" ]; then
    python3 -c "
import json
with open('queue/patterns.json') as f:
    data = json.load(f)
    patterns = data['patterns']
    total = len(patterns)
    completed = sum(1 for p in patterns if p.get('status') == 'completed')
    pending = total - completed

    print(f'Total patterns: {total}')
    print(f'Completed: {completed}')
    print(f'Pending: {pending}')
    print()

    # Next pattern
    for p in patterns:
        if p.get('status', 'pending') != 'completed':
            print(f'Next up: {p[\"name\"]} ({p[\"difficulty\"]})')
            break
"
else
    echo "❌ queue/patterns.json not found"
fi

echo
echo "======================================"
echo "✅ Status check complete"
