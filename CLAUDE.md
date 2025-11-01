# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an automated RAG (Retrieval-Augmented Generation) pattern showcase system that builds, tests, and posts daily demonstrations of production-quality RAG implementations to LinkedIn. Each demo uses multicolored ASCII art for terminal visualization.

**Current State:** Repository is in initial setup phase. Only README.md exists; implementation needs to be built from scratch.

## Architecture

The system follows a pipeline architecture with distinct stages:

1. **Pattern Selection** (`scripts/generate_demo.py`) - Reads from `queue/patterns.json`, selects next pattern, generates Claude Code prompt
2. **Demo Building** (`scripts/build_demo.sh`) - Invokes Claude Code in headless mode to implement the RAG pattern
3. **Testing** (`scripts/test_demo.py`) - Runs pytest tests, captures colored ASCII output
4. **Screenshot Capture** (`scripts/capture_screenshots.js`) - Uses Playwright to screenshot terminal output
5. **Technical Writing** (`scripts/write_breakdown.py`) - Uses Claude API to generate technical breakdown
6. **LinkedIn Posting** (`scripts/post_linkedin.py`) - Posts via LinkedIn API

GitHub Actions orchestrates the entire pipeline daily at 9 AM UTC via `.github/workflows/daily-showcase.yml`.

## Directory Structure

```
demos/                      # Individual RAG pattern implementations
  ├── {pattern-name}/      # Each pattern is self-contained
  │   ├── demo.py          # Main implementation
  │   ├── test_demo.py     # Tests with ASCII output capture
  │   └── requirements.txt # Pattern-specific dependencies
queue/
  └── patterns.json        # Queue of patterns to implement
scripts/                   # Pipeline automation scripts
outputs/
  └── YYYY-MM-DD/         # Daily outputs (demos, screenshots, posts)
```

## Key Technical Requirements

### ASCII Art Output
All demo implementations MUST use the `rich` library for colored terminal output:
- Queries: cyan panels
- Results: green panels
- LLM output: yellow panels
- Errors: red panels

Example pattern (from README.md:257-275):
```python
from rich.console import Console
from rich.panel import Panel

console = Console()
console.print(Panel("User query", title="📥 Input", border_style="cyan"))
console.print(Panel("Retrieved docs", title="🔎 Results", border_style="green"))
console.print(Panel("Generated answer", title="🧠 Output", border_style="yellow"))
```

### Demo Implementation Standards
Each demo in `demos/{pattern-name}/` should:
- Be minimal and focused on teaching ONE concept
- Include real working code (not stubs)
- Use production-ready RAG patterns (LangChain/LlamaIndex)
- Be fully tested with pytest
- Output workflow visualization via ASCII art
- Include inline comments explaining engineering decisions

### Pattern Queue Format
`queue/patterns.json` structure (from README.md:109-126):
```json
{
  "patterns": [
    {
      "name": "semantic-chunking",
      "description": "Smart document chunking with overlap and semantic boundaries",
      "difficulty": "beginner|intermediate|advanced",
      "key_concepts": ["embeddings", "cosine similarity", "chunking strategies"]
    }
  ]
}
```

## GitHub Actions Workflow

The `.github/workflows/daily-showcase.yml` must:
- Run on schedule (`cron: '0 9 * * *'`) and manual dispatch
- Use secrets: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_URN`
- Execute pipeline stages sequentially
- Commit generated demos back to repository
- Handle failures gracefully (skip posting if tests fail)

## LinkedIn Post Format

Posts follow this structure (from README.md:226-251):
```
[ASCII art screenshot]

🔍 RAG Pattern #{number}: {Pattern Name}

{Hook/insight paragraph}

Key insight: {One-liner}

🛠️ What it does:
• {Bullet point 1}
• {Bullet point 2}
• {Bullet point 3}

📊 Test results:
• {Metric 1}
• {Metric 2}
• {Metric 3}

Code + full breakdown: [GitHub link]

#AI #MachineLearning #RAG #LLM #AIEngineering
```

## Development Commands

Since implementation doesn't exist yet, here are the intended commands once built:

```bash
# Test full pipeline locally for a specific pattern
./scripts/build_demo.sh {pattern-name}
python scripts/test_demo.py demos/{pattern-name}
node scripts/capture_screenshots.js demos/{pattern-name}
python scripts/write_breakdown.py demos/{pattern-name}

# Run tests for a single demo
cd demos/{pattern-name}
pytest test_demo.py -v

# Manually trigger workflow (once GitHub Actions is set up)
# Use GitHub UI: Actions → Daily RAG Showcase → Run workflow
```

## RAG Patterns Priority List

Suggested implementation order (from README.md:211-223):
1. Semantic Chunking (beginner) - foundational
2. HyDE (intermediate) - demonstrates query expansion
3. Parent-Child Retrieval (intermediate) - context window optimization
4. Query Decomposition (intermediate) - complex query handling
5. Re-ranking (advanced) - two-stage retrieval
6. Metadata Filtering (beginner) - structured search
7. Ensemble Retrieval (intermediate) - hybrid search
8. Recursive Retrieval (advanced) - multi-hop reasoning
9. Agentic RAG (advanced) - LLM-driven retrieval
10. Self-Query (intermediate) - natural language to filters

## Implementation Notes

- Each demo should be runnable standalone (self-contained dependencies)
- Use virtual environments per demo to avoid dependency conflicts
- Screenshots should capture full terminal output with colors preserved
- Tests should verify both correctness AND ASCII art output formatting
- Breakdowns should explain "why" (engineering decisions) not just "what" (code walkthrough)
- LinkedIn posts must include actual metrics from test runs (not made up)
