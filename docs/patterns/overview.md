# Pattern Overview

A visual guide to all available RAG patterns, organized by difficulty level.

## Pattern Catalog

### Beginner Patterns

Perfect for getting started with RAG systems.

| Pattern | Use Case | Key Benefit |
|---------|----------|-------------|
| [Semantic Chunking](01-semantic-chunking.md) | Split documents intelligently | Preserves context, improves relevance |
| [Re-ranking](03-reranking.md) | Improve retrieval precision | Better relevance with minimal complexity |
| [Metadata Filtering](04-metadata-filtering.md) | Enforce hard constraints | Prevents wrong-version/language results |

### Intermediate Patterns

Build on fundamentals for more sophisticated retrieval.

| Pattern | Use Case | Key Benefit |
|---------|----------|-------------|
| [HyDE](02-hyde.md) | Question-answering systems | Bridges vocabulary gap between Q&A |
| [Query Decomposition](05-query-decomposition.md) | Complex multi-part queries | Comprehensive coverage of all aspects |

## Quick Reference

### By Use Case

**Need better context preservation?**
→ [Semantic Chunking](01-semantic-chunking.md)

**Users ask questions, docs are statements?**
→ [HyDE](02-hyde.md)

**Top results aren't the best matches?**
→ [Re-ranking](03-reranking.md)

**Getting outdated or wrong-language results?**
→ [Metadata Filtering](04-metadata-filtering.md)

**Users ask complex comparison questions?**
→ [Query Decomposition](05-query-decomposition.md)

### By Latency Budget

**< 100ms** - Use simple patterns only:
- Metadata Filtering (fastest)
- Basic vector search

**100-300ms** - Add these patterns:
- Semantic Chunking (preprocessing)
- Re-ranking (adds ~150-200ms)

**300ms+** - All patterns available:
- HyDE (adds ~300-500ms)
- Query Decomposition (adds ~500-800ms)

### By Retrieval Quality Needs

**High precision critical** (medical, legal, financial):
1. Metadata Filtering - Enforce constraints
2. Re-ranking - Select best matches
3. Query Decomposition - Comprehensive coverage

**Balance speed and quality** (general knowledge):
1. Semantic Chunking - Better context
2. Metadata Filtering - Basic constraints
3. Optional: Re-ranking if needed

**Exploration/research** (comprehensive answers):
1. Query Decomposition - Multi-faceted retrieval
2. HyDE - Better matching
3. Re-ranking - Final selection

## Pattern Combinations

Many patterns work well together:

### Stack 1: High Precision

```
Query → Metadata Filtering → Vector Search → Re-ranking → Results
```

**Use for:** Medical, legal, financial applications
**Latency:** ~200-300ms
**Precision:** ⭐⭐⭐⭐⭐

### Stack 2: Question Answering

```
Query → HyDE (generate hypothesis) → Vector Search → Re-ranking → Results
```

**Use for:** FAQ, documentation search, customer support
**Latency:** ~400-600ms
**Quality:** ⭐⭐⭐⭐⭐

### Stack 3: Complex Queries

```
Query → Decompose → Parallel Retrieval → Combine → Re-rank → Results
```

**Use for:** Research, analysis, comparison questions
**Latency:** ~600-1000ms
**Coverage:** ⭐⭐⭐⭐⭐

### Stack 4: Production Baseline

```
Semantic Chunking (preprocessing) → Metadata Filter → Vector Search
```

**Use for:** Most production systems
**Latency:** ~50-100ms
**Balance:** ⭐⭐⭐⭐

## Pattern Selection Guide

Not sure which pattern to use? Answer these questions:

1. **What's your latency budget?**
   - < 100ms: Basic only
   - 100-300ms: Add re-ranking
   - 300ms+: All patterns available

2. **What type of queries do you receive?**
   - Simple factual: Basic vector search
   - Questions: HyDE
   - Complex: Query Decomposition

3. **Do you have metadata?**
   - Yes: Use Metadata Filtering
   - No: Focus on semantic patterns

4. **How critical is precision?**
   - Critical: Re-ranking + Filtering
   - Important: Re-ranking
   - Moderate: Basic patterns

Use our interactive [Pattern Selector](../guides/choosing-pattern.md) for a recommendation!

## Coming Soon

Future patterns we're planning to add:

- **Parent-Child Retrieval** - Hierarchical context
- **Ensemble Retrieval** - BM25 + vector hybrid
- **Recursive Retrieval** - Multi-hop reasoning
- **Agentic RAG** - LLM-driven decisions
- **Self-Query** - Natural language filters

Want to contribute a pattern? See our [Contributing Guide](../about/contributing.md)!

---

**Ready to start?** Pick a pattern above or continue to [Installation →](../getting-started/installation.md)
