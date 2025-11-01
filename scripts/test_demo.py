#!/usr/bin/env python3
"""
Test runner for RAG demos - runs pytest and captures colored ASCII output
"""

import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def get_current_pattern():
    """Load the current pattern info"""
    pattern_file = Path("outputs/current_pattern.json")
    if not pattern_file.exists():
        print("ERROR: No current pattern file found")
        sys.exit(1)

    with open(pattern_file, 'r') as f:
        return json.load(f)

def run_tests(demo_path):
    """Run pytest tests for the demo"""
    print(f"🧪 Running tests for {demo_path}...")

    test_file = demo_path / "test_demo.py"
    if not test_file.exists():
        print(f"ERROR: Test file not found at {test_file}")
        return False

    # Run pytest with verbose output
    result = subprocess.run(
        ["pytest", str(test_file), "-v", "--color=yes"],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    return result.returncode == 0

def capture_demo_output(demo_path):
    """Run the demo and capture its ASCII art output"""
    print(f"🎨 Capturing ASCII output from {demo_path}...")

    demo_file = demo_path / "demo.py"
    if not demo_file.exists():
        print(f"ERROR: Demo file not found at {demo_file}")
        return False

    # Run the demo and capture output
    result = subprocess.run(
        [sys.executable, str(demo_file)],
        capture_output=True,
        text=True,
        cwd=demo_path
    )

    # Save output to file
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path(f"outputs/{today}")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "terminal_output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.stdout)

    print(f"✓ Output saved to {output_file}")
    print("\n" + "="*60)
    print("DEMO OUTPUT:")
    print("="*60)
    print(result.stdout)
    print("="*60)

    if result.stderr:
        print("STDERR:", result.stderr)

    return result.returncode == 0

def main():
    """Main execution"""
    # Get pattern info
    pattern = get_current_pattern()
    pattern_name = pattern['name']

    demo_path = Path(f"demos/{pattern_name}")

    if not demo_path.exists():
        print(f"ERROR: Demo directory not found at {demo_path}")
        sys.exit(1)

    print(f"Testing demo: {pattern_name}")
    print(f"Description: {pattern['description']}")
    print()

    # Run tests
    tests_passed = run_tests(demo_path)

    if not tests_passed:
        print("❌ Tests failed")
        sys.exit(1)

    print("✅ Tests passed")
    print()

    # Capture demo output
    output_captured = capture_demo_output(demo_path)

    if not output_captured:
        print("❌ Failed to capture demo output")
        sys.exit(1)

    print("✅ Demo output captured successfully")

    # Update pattern status to completed
    queue_file = Path("queue/patterns.json")
    with open(queue_file, 'r') as f:
        data = json.load(f)

    for p in data['patterns']:
        if p['name'] == pattern_name:
            p['status'] = 'completed'
            break

    with open(queue_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Pattern {pattern_name} marked as completed")

if __name__ == "__main__":
    main()
