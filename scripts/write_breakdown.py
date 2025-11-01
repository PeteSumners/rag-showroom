#!/usr/bin/env python3
"""
Technical breakdown writer - uses Claude API to generate LinkedIn post content
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic

def load_current_pattern():
    """Load the current pattern info"""
    pattern_file = Path("outputs/current_pattern.json")
    with open(pattern_file, 'r') as f:
        return json.load(f)

def read_demo_code(pattern_name):
    """Read the demo implementation code"""
    demo_file = Path(f"demos/{pattern_name}/demo.py")
    with open(demo_file, 'r') as f:
        return f.read()

def read_terminal_output():
    """Read the captured terminal output"""
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = Path(f"outputs/{today}/terminal_output.txt")
    with open(output_file, 'r', encoding='utf-8') as f:
        return f.read()

def generate_breakdown(pattern, code, terminal_output):
    """Use Claude API to generate technical breakdown and LinkedIn post"""

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    prompt = f"""You are writing a technical LinkedIn post about a RAG pattern demonstration.

Pattern: {pattern['name']}
Description: {pattern['description']}
Difficulty: {pattern['difficulty']}
Key Concepts: {', '.join(pattern['key_concepts'])}

Implementation Code:
```python
{code}
```

Terminal Output:
```
{terminal_output}
```

Write a LinkedIn post following this exact format:

🔍 RAG Pattern #X: [Pattern Name]

[2-3 sentence hook explaining the problem this pattern solves]

Key insight: [One impactful sentence]

🛠️ What it does:
• [Bullet 1]
• [Bullet 2]
• [Bullet 3]

📊 Implementation details:
• [Technical detail 1]
• [Technical detail 2]
• [Technical detail 3]

Code + full breakdown: [GitHub link placeholder]

#AI #MachineLearning #RAG #LLM #AIEngineering

Also write a longer technical breakdown (300-500 words) that explains:
1. The problem this pattern solves
2. How it works under the hood
3. Key engineering decisions in the implementation
4. When to use this pattern vs alternatives
5. Performance considerations

Format the response as JSON:
{{
  "linkedin_post": "...",
  "technical_breakdown": "..."
}}
"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Parse JSON response
    response_text = message.content[0].text

    # Try to extract JSON (handle markdown code blocks)
    if "```json" in response_text:
        json_str = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        json_str = response_text.split("```")[1].split("```")[0].strip()
    else:
        json_str = response_text

    return json.loads(json_str)

def save_outputs(linkedin_post, technical_breakdown):
    """Save the generated content"""
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(f"outputs/{today}")

    # Save LinkedIn post
    post_file = output_dir / "linkedin_post.md"
    with open(post_file, 'w', encoding='utf-8') as f:
        f.write(linkedin_post)

    # Save technical breakdown
    breakdown_file = output_dir / "technical_breakdown.md"
    with open(breakdown_file, 'w', encoding='utf-8') as f:
        f.write(technical_breakdown)

    print(f"✓ LinkedIn post saved to {post_file}")
    print(f"✓ Technical breakdown saved to {breakdown_file}")

def main():
    """Main execution"""
    print("✍️  Generating technical breakdown and LinkedIn post...")

    # Load pattern info
    pattern = load_current_pattern()
    pattern_name = pattern['name']

    print(f"Pattern: {pattern_name}")

    # Read demo code and output
    code = read_demo_code(pattern_name)
    terminal_output = read_terminal_output()

    # Generate content using Claude
    result = generate_breakdown(pattern, code, terminal_output)

    # Save outputs
    save_outputs(result['linkedin_post'], result['technical_breakdown'])

    print("✅ Content generation complete")

    # Display preview
    print("\n" + "="*60)
    print("LINKEDIN POST PREVIEW:")
    print("="*60)
    print(result['linkedin_post'])
    print("="*60)

if __name__ == "__main__":
    main()
