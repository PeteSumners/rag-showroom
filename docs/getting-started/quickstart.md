# Quick Start

Get running with your first RAG pattern in under 5 minutes!

## Your First Pattern

Let's start with **Semantic Chunking** - a foundational pattern that demonstrates how to split documents at semantic boundaries.

### 1. Navigate to the Pattern

```bash
cd patterns/01-semantic-chunking
```

### 2. Run the Example

```bash
python example.py
```

### 3. See the Results

You'll see beautiful colored terminal output:

```
=================================================================
  SEMANTIC CHUNKING EXAMPLE
=================================================================

Processing document...
SUCCESS: Created 12 semantic chunks

>>> INPUT DOCUMENT
+-------------------------------------------------------------------+
|  Retrieval-Augmented Generation (RAG) combines retrieval and      |
|  generation for better LLM outputs...                             |
+-------------------------------------------------------------------+

>>> CHUNKING STATISTICS
+-----------------------------+
| Metric               | Value|
|----------------------+------|
| Total Chunks         | 12   |
| Avg Sentences/Chunk  | 1.1  |
| Avg Characters/Chunk | 79   |
+-----------------------------+

>>> SEMANTIC CHUNKS
Chunk 0 | 1 sentences | 94 chars
+-------------------------------------------------------------------+
|  Retrieval-Augmented Generation (RAG) combines retrieval...       |
+-------------------------------------------------------------------+
```

## Try More Patterns

### Pattern 2: HyDE (Query Expansion)

```bash
cd ../02-hyde
python example.py
```

See how hypothetical document generation improves retrieval!

### Pattern 3: Re-ranking

```bash
cd ../03-reranking
python example.py
```

Watch as re-ranking moves the most relevant document from position 5 to position 1!

### Pattern 4: Metadata Filtering

```bash
cd ../04-metadata-filtering
python example.py
```

See how metadata filters prevent retrieving deprecated documentation.

### Pattern 5: Query Decomposition

```bash
cd ../05-query-decomposition
python example.py
```

Watch a complex query get broken into focused sub-questions!

## Understanding the Output

Each example uses color-coding:

- **Cyan** - Input (queries, documents)
- **Green** - Results (retrieved documents, chunks)
- **Yellow** - Statistics and insights
- **Red** - Baseline/comparison results

## Running Tests

Most patterns include test files:

```bash
cd patterns/01-semantic-chunking
pytest test_example.py -v
```

## Modifying Examples

Want to experiment? Try changing parameters:

```python
# In example.py, try different threshold values:
chunker = SemanticChunker(similarity_threshold=0.2)  # More chunks
chunker = SemanticChunker(similarity_threshold=0.5)  # Fewer chunks
```

Then run the example again to see the difference!

## What's Next?

Now that you've seen the patterns in action:

1. **[Read the pattern documentation](../patterns/overview.md)** - Understand when to use each pattern
2. **[Compare patterns](../guides/comparison.md)** - See trade-offs and use cases
3. **[Choose your pattern](../guides/choosing-pattern.md)** - Find the right pattern for your needs

## Need Help?

- Check the [Running Examples](running-examples.md) guide for detailed instructions
- See [Troubleshooting](installation.md#troubleshooting) for common issues
- Open an issue on [GitHub](https://github.com/yourusername/rag-patterns-guide/issues)

---

**Happy learning!** Continue to [Pattern Overview →](../patterns/overview.md)
