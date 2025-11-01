#!/usr/bin/env python3
"""
Demo builder using Claude API directly
Generates demo files based on the selected RAG pattern
"""

import os
import sys
import json
from pathlib import Path
from anthropic import Anthropic


def load_prompt():
    """Load the generated prompt"""
    prompt_file = Path("outputs/claude_prompt.txt")
    if not prompt_file.exists():
        print("ERROR: Prompt file not found")
        print("Run python scripts/generate_demo.py first")
        sys.exit(1)

    with open(prompt_file, 'r') as f:
        return f.read()


def load_pattern():
    """Load current pattern info"""
    pattern_file = Path("outputs/current_pattern.json")
    with open(pattern_file, 'r') as f:
        return json.load(f)


def build_with_claude(prompt, pattern_name):
    """Use Claude API to generate demo files"""

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    print(f"🤖 Building demo for: {pattern_name}")
    print("Invoking Claude API...")

    # Enhanced prompt with file generation instructions
    enhanced_prompt = f"""{prompt}

Please generate the complete implementation as three separate files:

1. **demo.py** - The main demo implementation with Rich ASCII art output
2. **test_demo.py** - Comprehensive pytest tests
3. **requirements.txt** - Dependencies (at minimum: rich>=13.0.0, pytest>=7.4.0)

Return your response in the following JSON format:
{{
  "demo.py": "...full demo.py content...",
  "test_demo.py": "...full test_demo.py content...",
  "requirements.txt": "...full requirements.txt content..."
}}

Make the code production-ready, well-documented, and focused on teaching the concept clearly.
"""

    # Call Claude API
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8000,
        messages=[
            {"role": "user", "content": enhanced_prompt}
        ]
    )

    response_text = message.content[0].text

    print("✓ Response received from Claude")

    # Parse JSON response
    try:
        # Extract JSON if wrapped in markdown code blocks
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
        else:
            json_str = response_text

        files = json.loads(json_str)

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON response: {e}")
        print("Response text:", response_text[:500])
        sys.exit(1)

    return files


def save_demo_files(pattern_name, files):
    """Save generated files to demo directory"""

    demo_dir = Path(f"demos/{pattern_name}")
    demo_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 Saving files to {demo_dir}")

    for filename, content in files.items():
        file_path = demo_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Created {file_path}")

    # Make demo.py and test_demo.py executable
    os.chmod(demo_dir / "demo.py", 0o755)
    os.chmod(demo_dir / "test_demo.py", 0o755)

    print(f"✅ Demo built successfully in {demo_dir}")


def main():
    """Main execution"""

    # Load prompt and pattern
    prompt = load_prompt()
    pattern = load_pattern()
    pattern_name = pattern['name']

    print(f"Building: {pattern['name']}")
    print(f"Description: {pattern['description']}")
    print()

    # Build demo using Claude API
    files = build_with_claude(prompt, pattern_name)

    # Validate required files
    required_files = ['demo.py', 'test_demo.py', 'requirements.txt']
    missing_files = [f for f in required_files if f not in files]

    if missing_files:
        print(f"ERROR: Missing required files: {missing_files}")
        print("Available files:", list(files.keys()))
        sys.exit(1)

    # Save files
    save_demo_files(pattern_name, files)

    print()
    print("🎉 Demo build complete!")


if __name__ == "__main__":
    main()
