# Welcome to RAG Patterns Guide

> **A comprehensive visual guide to production RAG patterns**

Learn Retrieval-Augmented Generation (RAG) patterns through clear conceptual explanations, working code examples, and beautiful terminal visualizations. Each pattern demonstrates a real-world technique used in production AI systems.

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
