#!/usr/bin/env python3
"""
Pattern selection script - selects next RAG pattern from queue
and generates a prompt file for Claude Code headless mode.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_patterns():
    """Load patterns from queue/patterns.json"""
    queue_file = Path("queue/patterns.json")
    with open(queue_file, 'r') as f:
        data = json.load(f)
    return data['patterns']

def select_next_pattern(patterns):
    """Select the next pending pattern from the queue"""
    for pattern in patterns:
        if pattern.get('status', 'pending') == 'pending':
            return pattern
    # If all are complete, start over from the beginning
    return patterns[0] if patterns else None

def update_pattern_status(pattern_name, status):
    """Update the status of a pattern in the queue"""
    queue_file = Path("queue/patterns.json")
    with open(queue_file, 'r') as f:
        data = json.load(f)

    for pattern in data['patterns']:
        if pattern['name'] == pattern_name:
            pattern['status'] = status
            break

    with open(queue_file, 'w') as f:
        json.dump(data, f, indent=2)

def generate_prompt(pattern):
    """Generate Claude Code prompt for building the demo"""
    prompt = f"""Build a production-quality RAG demo for: {pattern['name']}

Description: {pattern['description']}
Difficulty: {pattern['difficulty']}
Key Concepts: {', '.join(pattern['key_concepts'])}

Requirements:
1. Create demos/{pattern['name']}/demo.py with a complete, working implementation
2. Create demos/{pattern['name']}/test_demo.py with pytest tests
3. Create demos/{pattern['name']}/requirements.txt with dependencies
4. Use the Rich library for colored ASCII art terminal output:
   - Queries/Input: cyan panels with 📥 icon
   - Retrieval Results: green panels with 🔎 icon
   - LLM Output: yellow panels with 🧠 icon
   - Errors: red panels with ❌ icon
5. Include a main() function that demonstrates the pattern with sample data
6. Add inline comments explaining engineering decisions
7. Make it minimal, focused, and teaching-oriented

Technical Stack:
- Use LangChain or LlamaIndex for RAG implementation
- Use OpenAI or Anthropic for embeddings/LLM (configurable via env vars)
- Include proper error handling
- Keep the demo self-contained and runnable

ASCII Art Output Example:
```python
from rich.console import Console
from rich.panel import Panel

console = Console()
console.print(Panel("User query text", title="📥 Input", border_style="cyan"))
console.print(Panel("Retrieved documents", title="🔎 Results", border_style="green"))
console.print(Panel("Generated answer", title="🧠 Output", border_style="yellow"))
```

The demo should be production-ready but minimal - focus on teaching the core concept clearly.
"""
    return prompt

def main():
    """Main execution"""
    # Load patterns and select next one
    patterns = load_patterns()
    pattern = select_next_pattern(patterns)

    if not pattern:
        print("ERROR: No patterns found in queue")
        exit(1)

    print(f"Selected pattern: {pattern['name']}")
    print(f"Description: {pattern['description']}")
    print(f"Difficulty: {pattern['difficulty']}")

    # Generate prompt
    prompt = generate_prompt(pattern)

    # Save prompt to file for Claude Code
    prompt_file = Path("outputs/claude_prompt.txt")
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    with open(prompt_file, 'w') as f:
        f.write(prompt)

    # Save pattern info to environment file
    env_file = Path("outputs/current_pattern.json")
    with open(env_file, 'w') as f:
        json.dump(pattern, f, indent=2)

    print(f"✓ Prompt saved to {prompt_file}")
    print(f"✓ Pattern info saved to {env_file}")

    # Mark as in-progress
    update_pattern_status(pattern['name'], 'in-progress')

if __name__ == "__main__":
    main()
