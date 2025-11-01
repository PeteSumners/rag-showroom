#!/bin/bash
# Build demo using Claude Code in headless mode

set -e  # Exit on error

echo "🔨 Building RAG demo with Claude Code..."

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "ERROR: ANTHROPIC_API_KEY environment variable not set"
    exit 1
fi

# Check if prompt file exists
PROMPT_FILE="outputs/claude_prompt.txt"
if [ ! -f "$PROMPT_FILE" ]; then
    echo "ERROR: Prompt file not found at $PROMPT_FILE"
    echo "Run python scripts/generate_demo.py first"
    exit 1
fi

# Read the prompt
PROMPT=$(cat "$PROMPT_FILE")

# Invoke Claude Code in headless mode
# Note: This assumes claude-code CLI is installed and available
# Adjust the command based on the actual Claude Code CLI interface
echo "Invoking Claude Code..."

# Use the @ syntax to pass file content directly
claude-code --headless "@$PROMPT_FILE"

echo "✓ Demo build complete"
