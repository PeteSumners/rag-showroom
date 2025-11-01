# 🎨 RAG Showroom - Daily AI Engineering Showcases

> **Zero AI slop. Just clean code, colored ASCII art, and real RAG implementations.**

This repo autonomously builds, tests, and showcases production-quality RAG patterns every day. Each demo is small, focused, and teaches one concept exceptionally well. Everything uses multicolored ASCII art for terminal output because we're not animals.

## 🎯 What This Does

Every day at 9 AM UTC, GitHub Actions:

1. **Picks a RAG pattern** from the queue (semantic chunking, hybrid search, re-ranking, query decomposition, etc.)
2. **Builds a minimal working demo** using Claude Code in headless mode
3. **Tests it thoroughly** with real queries and edge cases
4. **Captures beautiful terminal output** with colored ASCII art showing the workflow
5. **Writes a technical breakdown** explaining the engineering decisions
6. **Posts to LinkedIn** with screenshots and code snippets

## 🎨 The ASCII Art Philosophy

Every demo outputs its workflow as colored ASCII art in the terminal:

```
╔═══════════════════════════════════════════════════════════════╗
║  🔍 QUERY DECOMPOSITION RAG                                   ║
╚═══════════════════════════════════════════════════════════════╝

📥 User Query:
   "What are the performance implications of using asyncio vs threading?"

🧩 Decomposed into:
   ├─ Q1: "asyncio performance characteristics"
   ├─ Q2: "threading performance characteristics"  
   └─ Q3: "asyncio vs threading benchmarks"

🔎 Vector Search Results:
   Q1 ─→ 📄 Doc_032 (score: 0.94) ─→ ✓ Retrieved
   Q2 ─→ 📄 Doc_117 (score: 0.91) ─→ ✓ Retrieved
   Q3 ─→ 📄 Doc_089 (score: 0.89) ─→ ✓ Retrieved

🧠 LLM Synthesis:
   ├─ Tokens in:  2,847
   ├─ Tokens out: 412
   └─ Latency:    1.3s

✅ Response Generated
```

Uses ANSI color codes: queries in cyan, results in green, errors in red, metadata in yellow.

## 📁 Project Structure

```
rag-showroom/
├── .github/workflows/
│   └── daily-showcase.yml          # Main automation workflow
├── demos/
│   ├── semantic-chunking/          # Each pattern gets a folder
│   ├── hyde-search/
│   ├── parent-child-retrieval/
│   └── ...
├── queue/
│   └── patterns.json                # Queue of patterns to build
├── scripts/
│   ├── generate_demo.py             # Claude API: picks pattern & writes prompt
│   ├── build_demo.sh                # Claude Code: builds the demo
│   ├── test_demo.py                 # Runs tests, captures ASCII output
│   ├── capture_screenshots.js       # Playwright: terminal screenshots
│   ├── write_breakdown.py           # Claude API: technical write-up
│   └── post_linkedin.py             # Posts to LinkedIn API
├── outputs/
│   └── YYYY-MM-DD/                  # Daily output folders
│       ├── demo/                    # The built demo
│       ├── screenshots/             # Terminal screenshots
│       └── post.md                  # LinkedIn post content
└── README.md
```

## 🛠️ Tech Stack

- **Build:** Claude Code (headless mode) for demo implementation
- **Test:** pytest + custom ASCII reporters
- **Visual:** Rich library for colored terminal output + Playwright for screenshots
- **Post:** LinkedIn API (official) or Selenium fallback
- **RAG:** LangChain/LlamaIndex for patterns, OpenAI/Anthropic for embeddings/LLM

## 🚀 Setup

### Quick Start (Automated Online Setup)

Run the complete online setup in one command:

```bash
./setup-online.sh
```

This will:
- ✅ Create GitHub repository
- ✅ Get LinkedIn API credentials (with helper tool)
- ✅ Configure all secrets
- ✅ Trigger test run
- ✅ Set up daily automation

**See [ONLINE_SETUP.md](ONLINE_SETUP.md) for detailed walkthrough.**

### Manual Setup

If you prefer step-by-step control:

#### 1. Create Repository
```bash
./setup-github.sh
```

#### 2. Get LinkedIn Credentials
```bash
python scripts/linkedin_oauth.py
```
Or follow [LINKEDIN_SETUP.md](LINKEDIN_SETUP.md) for manual process.

#### 3. Configure GitHub Secrets
```bash
./setup-secrets.sh
```

Required secrets:
- `ANTHROPIC_API_KEY` - For Claude API
- `LINKEDIN_ACCESS_TOKEN` - For posting
- `LINKEDIN_URN` - Your LinkedIn user URN

#### 4. Deploy

Just push to main. GitHub Actions handles the rest!

### 3. Customize the Pattern Queue

Edit `queue/patterns.json` to add your RAG patterns:

```json
{
  "patterns": [
    {
      "name": "semantic-chunking",
      "description": "Smart document chunking with overlap and semantic boundaries",
      "difficulty": "beginner",
      "key_concepts": ["embeddings", "cosine similarity", "chunking strategies"]
    },
    {
      "name": "hyde-search",
      "description": "Hypothetical Document Embeddings for better retrieval",
      "difficulty": "intermediate",
      "key_concepts": ["query expansion", "embedding space", "synthetic documents"]
    }
  ]
}
```

### 4. Run Locally (Optional)

```bash
# Test the full pipeline locally
./scripts/build_demo.sh semantic-chunking
python scripts/test_demo.py demos/semantic-chunking
node scripts/capture_screenshots.js demos/semantic-chunking
python scripts/write_breakdown.py demos/semantic-chunking
```

### 5. Deploy

Just push to main. GitHub Actions handles the rest.

## 📋 Workflow Details

The `.github/workflows/daily-showcase.yml` file orchestrates everything:

```yaml
name: Daily RAG Showcase

on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM UTC daily
  workflow_dispatch:      # Manual trigger

jobs:
  build-and-post:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      # Pick next pattern from queue
      - name: Select RAG pattern
        run: python scripts/generate_demo.py
        
      # Build with Claude Code (headless)
      - name: Build demo
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: ./scripts/build_demo.sh
        
      # Test and capture ASCII output
      - name: Test demo
        run: python scripts/test_demo.py
        
      # Screenshot the terminal output
      - name: Capture screenshots
        run: node scripts/capture_screenshots.js
        
      # Write technical breakdown
      - name: Generate breakdown
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python scripts/write_breakdown.py
        
      # Post to LinkedIn
      - name: Post to LinkedIn
        env:
          LINKEDIN_ACCESS_TOKEN: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
          LINKEDIN_URN: ${{ secrets.LINKEDIN_URN }}
        run: python scripts/post_linkedin.py
        
      # Commit the new demo
      - name: Commit demo
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add demos/ outputs/
          git commit -m "feat: add $(date +%Y-%m-%d) RAG showcase"
          git push
```

## 🎯 What Makes This NOT Slop

1. **Every demo actually runs** - tested code with real outputs
2. **Teaching-focused** - each pattern is minimal, clear, well-commented
3. **Production patterns** - these are techniques used in real RAG systems
4. **Visual personality** - ASCII art makes it memorable and shareable
5. **Technical depth** - explains the "why" not just the "what"
6. **Consistent quality** - automated testing ensures nothing broken ships

## 🔥 Example Patterns to Showcase

- **Semantic Chunking**: Chunk documents at semantic boundaries, not arbitrary sizes
- **HyDE**: Generate hypothetical answers, embed them, use for retrieval
- **Parent-Child Retrieval**: Store small chunks, retrieve with parent context
- **Query Decomposition**: Break complex queries into sub-queries
- **Re-ranking**: Two-stage retrieval with cross-encoder re-ranking
- **Metadata Filtering**: Pre-filter with metadata before vector search
- **Ensemble Retrieval**: Combine BM25 + vector search
- **Recursive Retrieval**: Multi-hop retrieval for complex questions
- **Agentic RAG**: Let LLM decide when to retrieve more context
- **Self-Query**: LLM extracts structured filters from natural language

## 💡 LinkedIn Post Format

Each post follows this structure:

```
[ASCII art diagram as image]

🔍 RAG Pattern #23: Query Decomposition

Complex questions need complex retrieval. Instead of one fuzzy vector search,
this pattern breaks queries into focused sub-questions.

Key insight: Multiple precise retrievals beat one vague retrieval.

🛠️ What it does:
• Decomposes "Compare X vs Y" into separate lookups
• Retrieves independently with higher relevance
• Synthesizes results with full context

📊 Test results:
• Relevance score: +32% vs naive RAG
• Latency: 1.4s for 3-way decomposition
• Token efficiency: 40% reduction in irrelevant context

Code + full breakdown: [GitHub link]

#AI #MachineLearning #RAG #LLM #AIEngineering
```

## 🎨 ASCII Art Guidelines

All terminal output should use the `rich` library for colors:

```python
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# Query input
console.print(Panel("User query here", title="📥 Input", border_style="cyan"))

# Retrieval results
console.print(Panel("Retrieved docs", title="🔎 Results", border_style="green"))

# LLM generation
console.print(Panel("Generated answer", title="🧠 Output", border_style="yellow"))

# Errors
console.print(Panel("Error details", title="❌ Error", border_style="red"))
```

## 🤝 Contributing

Want to add a RAG pattern? Submit a PR with:
1. The pattern added to `queue/patterns.json`
2. Implementation requirements/constraints
3. Example test cases

## 📝 License

MIT - build cool shit, give credit

---

**Not here to spam LinkedIn. Here to showcase real engineering.**
