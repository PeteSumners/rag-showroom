# Running Examples

Detailed guide for running and understanding each pattern example.

## Basic Usage

Every pattern follows the same structure:

```bash
cd patterns/<pattern-name>
python example.py
```

## Pattern Examples

### 1. Semantic Chunking

```bash
cd patterns/01-semantic-chunking
python example.py
```

**What to look for:**
- Documents split at topic boundaries
- Related sentences grouped together
- Chunk statistics showing average sizes

**Experiment:**
```python
# In example.py, try different thresholds
chunker = SemanticChunker(similarity_threshold=0.1)  # More chunks
chunker = SemanticChunker(similarity_threshold=0.3)  # Fewer chunks
```

### 2. HyDE (Hypothetical Document Embeddings)

```bash
cd patterns/02-hyde
python example.py
```

**What to look for:**
- Generated hypothetical answer
- Comparison between naive and HyDE retrieval
- Better matches with hypothesis-based search

### 3. Re-ranking

```bash
cd patterns/03-reranking
python example.py
```

**What to look for:**
- Initial vector search results (Stage 1)
- Re-ranked results showing position changes (Stage 2)
- Most relevant doc moving from position 5 to position 1

### 4. Metadata Filtering

```bash
cd patterns/04-metadata-filtering
python example.py
```

**What to look for:**
- Unfiltered results showing deprecated docs
- Filtered results showing only v3 API docs
- How metadata constraints prevent wrong results

### 5. Query Decomposition

```bash
cd patterns/05-query-decomposition
python example.py
```

**What to look for:**
- Complex query broken into sub-questions
- Retrieval results for each sub-question
- Combined results providing comprehensive coverage

## Understanding Terminal Output

### Color Coding

All examples use consistent color schemes:

- **Cyan** (`>>>` cyan headers) - Input data (queries, documents)
- **Green** (`>>>` green headers) - Results and outputs
- **Yellow** (`>>>` yellow headers) - Statistics, insights, metadata
- **Red** (`>>>` red headers) - Baseline/comparison results

### Output Sections

Most examples include these sections:

1. **Input** - The query or document being processed
2. **Processing** - What the algorithm is doing
3. **Results** - The output (chunks, retrieved docs, etc.)
4. **Key Insight** - Summary of what makes this pattern effective

## Running Tests

Each pattern includes test files:

```bash
cd patterns/<pattern-name>
pytest test_example.py -v
```

!!! note "Test Requirements"
    Some tests may require additional dependencies. Run:
    ```bash
    pip install pytest
    ```

## Troubleshooting

### Colors Not Showing

**Windows:** Use Windows Terminal instead of Command Prompt

**Alternative:** Install colorama:
```bash
pip install colorama
```

### Module Not Found

Make sure you're in the correct directory:
```bash
# Should be in the pattern directory
pwd  # or cd on Windows

# Should show: .../patterns/<pattern-name>
```

### Example Doesn't Run

Check Python version:
```bash
python --version  # Should be 3.10+
```

Reinstall dependencies:
```bash
cd ../..  # Back to root
pip install -r requirements.txt
```

## Customizing Examples

### Modify Parameters

Each example has configurable parameters at the bottom of the file:

```python
# Find in main() function
def main():
    # Modify these values
    chunker = SemanticChunker(similarity_threshold=0.15)
    retriever = Retriever(documents, top_k=5)
    # etc.
```

### Use Your Own Data

Replace sample data in the `create_sample_*()` functions:

```python
def create_sample_documents():
    return [
        Document(
            id="custom1",
            title="Your Title",
            content="Your content here..."
        ),
        # Add more documents
    ]
```

## Next Steps

Once you've run the examples:

1. **[Read pattern documentation](../patterns/overview.md)** - Understand concepts deeply
2. **[Compare patterns](../guides/comparison.md)** - See when to use each
3. **[Adapt for your project](../guides/choosing-pattern.md)** - Apply to your use case

---

**Need help?** Open an [issue on GitHub](https://github.com/yourusername/rag-patterns-guide/issues)
