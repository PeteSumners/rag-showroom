# Welcome to RAG Patterns Guide

<div style="text-align: center; margin: 2rem 0;">
  <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; background: linear-gradient(120deg, #1e88e5, #7c4dff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
    Master Production RAG Patterns
  </h2>
  <p style="font-size: 1.3rem; color: #666; max-width: 700px; margin: 0 auto 2rem;">
    Learn Retrieval-Augmented Generation through <strong>working code</strong>,
    <strong>real metrics</strong>, and <strong>visual demonstrations</strong>
  </p>
</div>

<div class="grid cards" style="margin: 2rem 0;" markdown>

-   :material-rocket-launch:{ .lg .middle } __Start Learning in 5 Minutes__

    ---

    Working code examples you can run immediately. No API keys required for local testing.

    [:octicons-arrow-right-24: Quick Start](getting-started/quickstart.md)

-   :material-chart-line:{ .lg .middle } __Real Production Metrics__

    ---

    Actual performance numbers: +15% to +55% precision improvements, cost breakdowns per 1M queries.

    [:octicons-arrow-right-24: See Comparisons](guides/comparison.md)

-   :material-brain:{ .lg .middle } __Smart Pattern Selection__

    ---

    Interactive decision tree helps you choose the right pattern for your use case.

    [:octicons-arrow-right-24: Find Your Pattern](guides/choosing-pattern.md)

-   :material-code-braces:{ .lg .middle } __Production-Ready Code__

    ---

    Copy-paste implementations with error handling, monitoring, and optimization.

    [:octicons-arrow-right-24: Integration Guide](guides/production-integration.md)

</div>

## Why This Guide Exists

**The Problem**: RAG tutorials show toy examples. Production systems need battle-tested patterns.

**The Solution**: This guide teaches the actual techniques used by companies building real RAG systems, with working code and honest trade-off analysis.

!!! success "What Makes This Different"
    ✅ **Working code** - Not pseudocode. Run `python example.py` and see it work.
    ✅ **Real metrics** - Actual performance numbers from production systems.
    ✅ **Visual learning** - Colored terminal output shows patterns in action.
    ✅ **Honest trade-offs** - When NOT to use each pattern, cost analysis, latency impacts.
    ✅ **Production focus** - Error handling, monitoring, optimization strategies.

## What You'll Learn

This guide covers essential RAG patterns, from foundational concepts to advanced techniques. Each pattern includes:

- 📝 **Conceptual explanation** - Why and when to use it
- 💡 **Working code examples** - Simple, runnable implementations
- 🎨 **Visual demonstrations** - Colored terminal output showing the pattern in action
- 🧪 **Test cases** - Real queries and expected behavior

## Available Patterns

### Beginner Level

<div class="grid cards" markdown>

-   :material-scissors-cutting:{ .lg .middle } __Semantic Chunking__

    ---

    Split documents at semantic boundaries instead of arbitrary character limits

    [:octicons-arrow-right-24: Learn more](patterns/01-semantic-chunking.md)

-   :material-sort-ascending:{ .lg .middle } __Re-ranking__

    ---

    Two-stage retrieval: fast vector search + precise re-ranking

    [:octicons-arrow-right-24: Learn more](patterns/03-reranking.md)

-   :material-filter:{ .lg .middle } __Metadata Filtering__

    ---

    Pre-filter with structured data before vector search

    [:octicons-arrow-right-24: Learn more](patterns/04-metadata-filtering.md)

</div>

### Intermediate Level

<div class="grid cards" markdown>

-   :material-lightbulb-on:{ .lg .middle } __HyDE__

    ---

    Query expansion through hypothetical answer generation

    [:octicons-arrow-right-24: Learn more](patterns/02-hyde.md)

-   :material-call-split:{ .lg .middle } __Query Decomposition__

    ---

    Break complex queries into focused sub-questions

    [:octicons-arrow-right-24: Learn more](patterns/05-query-decomposition.md)

</div>

## Quick Start

Get started in minutes:

```bash
# Clone the repository
git clone https://github.com/yourusername/rag-patterns-guide.git
cd rag-patterns-guide

# Install dependencies
pip install -r requirements.txt

# Run an example
cd patterns/01-semantic-chunking
python example.py
```

See the [Installation Guide](getting-started/installation.md) for detailed setup instructions.

## Visual Learning

All examples use colored ASCII output to visualize the RAG workflow:

```
=================================================================
  SEMANTIC CHUNKING EXAMPLE
=================================================================

>>> INPUT DOCUMENT
+---------------------------------------------------------------+
|  Retrieval-Augmented Generation (RAG) combines retrieval      |
|  and generation for better LLM outputs...                     |
+---------------------------------------------------------------+

>>> SEMANTIC CHUNKS
Chunk 0 | 1 sentences | 94 chars
Chunk 2 | 2 sentences | 146 chars  ← Topic grouping!
```

## Pattern Selection Guide

Not sure which pattern to use? Check out our [Pattern Comparison Guide](guides/comparison.md) or use our [Pattern Selector Tool](guides/choosing-pattern.md).

## Contributing

Want to add a pattern or improve an explanation? We welcome contributions! See our [Contributing Guide](about/contributing.md) for details.

## License

This project is licensed under the MIT License. See [License](about/license.md) for details.

---

**Ready to dive in?** Start with [Installation →](getting-started/installation.md)
