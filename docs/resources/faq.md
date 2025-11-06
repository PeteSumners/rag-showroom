# Frequently Asked Questions

Common questions about RAG patterns and this guide.

## Getting Started

### Do I need API keys to try the examples?

**No!** All the basic examples use mock implementations that work without API keys. You can:
- Run all 5 pattern examples locally
- See the colored terminal output
- Understand how patterns work

**For production**: You'll need API keys (OpenAI, Anthropic, etc.) but not for learning!

### What programming experience do I need?

**Minimum**: Basic Python (if you can read functions and classes, you're good)

**Helpful**:
- Understanding of functions and loops
- Basic API concepts
- Command line usage

**Not required**:
- ML/AI background
- Vector database experience
- LLM expertise

### How long does it take to learn?

**Quick start**: 5 minutes to run first example
**Basic proficiency**: 1-2 weeks (beginner patterns)
**Production ready**: 4 weeks (full roadmap)
**Master level**: 2-3 months (building real systems)

### Can I use this for my job/startup?

**Yes!** MIT License means:
- ✅ Use in personal projects
- ✅ Use in commercial products
- ✅ Modify as needed
- ✅ No attribution required (but appreciated!)

---

## Technical Questions

### Which pattern should I start with?

**For learning**: Start with [Semantic Chunking](../patterns/01-semantic-chunking.md) - it's fundamental

**For quick ROI**: Start with [Metadata Filtering](../patterns/04-metadata-filtering.md) - 4 hours, massive impact

**For production**: Use the [Pattern Selector](../guides/choosing-pattern.md)

### Can I use multiple patterns together?

**Yes!** Most patterns complement each other:

**Great combinations**:
- Semantic Chunking + Metadata Filtering + Re-ranking
- HyDE + Re-ranking
- Metadata Filtering + anything

**Avoid**:
- HyDE + Query Decomposition (redundant - both expand queries)

See [Pattern Combinations](../guides/comparison.md#pattern-combinations)

### How much does it cost in production?

**Depends on**:
- Query volume
- Patterns used
- LLM model choice

**Typical ranges** (100K queries/month):
- Basic: $200-300
- Standard: $300-500
- Advanced: $500-1000

**Use the [Cost Calculator](../tools/cost-calculator.md)** for your specific case!

### What vector databases work with these patterns?

**All of them!** Patterns are database-agnostic:

- ✅ ChromaDB (local, easy to start)
- ✅ Pinecone (managed, scalable)
- ✅ Weaviate (open-source, feature-rich)
- ✅ Qdrant (fast, efficient)
- ✅ Milvus (large-scale)
- ✅ Any other vector DB

The examples use ChromaDB but concepts transfer directly.

### Do I need GPU for these patterns?

**No!** None of the patterns require GPU:

- Semantic Chunking: CPU preprocessing
- Metadata Filtering: No ML needed
- Re-ranking: Small models run on CPU
- HyDE: API calls to hosted LLMs
- Query Decomposition: API calls

**For production embeddings**: GPUs help but aren't required. You can use API-based embeddings (OpenAI, Cohere, etc.)

---

## Pattern-Specific Questions

### When should I use HyDE vs Query Decomposition?

**Use HyDE when:**
- Users ask questions, docs are statements
- Single queries, not multi-part
- Need better vocabulary matching
- Example: "What is X?"

**Use Query Decomposition when:**
- Users ask complex comparisons
- Multi-part questions
- Need comprehensive coverage
- Example: "Compare X vs Y"

**Don't use both** - they're redundant!

### Why is Semantic Chunking better than fixed-size?

**Fixed-size chunking** (every 500 chars):
```
...the key benefit is improved accu[CHUNK ENDS]
[NEW CHUNK STARTS]racy through better context preservation...
```
😞 Breaks mid-sentence, loses context

**Semantic chunking** (at topic boundaries):
```
...the key benefit is improved accuracy through better context preservation.
[NEW CHUNK STARTS]
Another important aspect is performance...
```
😊 Complete thoughts, better context

**Result**: +15-20% precision improvement

### What's the difference between re-ranking and re-ordering?

**They're the same!** Re-ranking = re-ordering = two-stage retrieval:

1. **Stage 1**: Fast vector search (50-100 candidates)
2. **Stage 2**: Precise model re-ranks them
3. **Result**: Best results bubble to top

### Can I re-rank without vector search?

**Not really.** Re-ranking is expensive (slow + costly), so:

- **Vector search**: Fast, gets candidates ($0.0001/query)
- **Re-ranking**: Slow, finds best ones ($0.0001/query)
- **Together**: Fast + accurate ✅

**Just re-ranking**: Too slow for 1000s of docs ❌

---

## Implementation Questions

### How do I add this to my existing RAG system?

**Step-by-step**:

1. **Measure baseline** (before adding patterns)
2. **Start with metadata filtering** (if you have metadata)
3. **Add re-ranking** (biggest quality boost)
4. **Measure improvement** (quantify ROI)
5. **Add more patterns** (if needed)

See [Production Integration](../guides/production-integration.md)

### How do I test if patterns are working?

**Create a test set**:
```python
test_queries = [
    ("What is Python?", expected_doc_ids),
    ("How do I authenticate?", expected_doc_ids),
    # ... 20-50 queries
]

# Measure precision
correct = 0
for query, expected in test_queries:
    results = rag_query(query)
    if results[0] in expected:
        correct += 1

precision = correct / len(test_queries)
```

**Track over time**: Baseline → After Pattern 1 → After Pattern 2

### What if patterns make things worse?

**Common causes**:

1. **Wrong threshold** - Try different values
2. **Wrong pattern** - Not right for your use case
3. **Bad data** - Garbage in, garbage out
4. **Need tuning** - Default settings not optimal

**Solution**: Measure, tune, iterate. Start with defaults, adjust based on data.

### How do I explain this to my boss?

**Focus on business impact**:

> "I want to implement re-ranking. It takes 12 hours and costs $10/month for 100K queries. Similar companies saw +25-40% precision improvements, which means fewer support tickets and happier users. I measured our baseline at 62% precision. After implementing, we should see 80-85% precision. Can I spend Friday afternoon on this?"

**Highlight ROI**:
- Time investment vs expected return
- Real metrics from case studies
- Measurable outcomes

### Can I contribute new patterns?

**Yes, please!** We welcome contributions:

1. **Check issues** - See if pattern already planned
2. **Create discussion** - Propose the pattern
3. **Follow template** - Match existing structure
4. **Submit PR** - With docs + code + tests

See [Contributing Guide](../about/contributing.md)

---

## Troubleshooting

### "Module not found" errors

**Solution**:
```bash
# Make sure you're in the right directory
cd patterns/01-semantic-chunking

# Install dependencies
pip install -r ../../requirements.txt

# Try again
python example.py
```

### Terminal colors not showing (Windows)

**Solution 1**: Use Windows Terminal (recommended)
**Solution 2**: Install colorama
```bash
pip install colorama
```

### Example runs but output looks wrong

**Check**:
- Are you in the pattern directory?
- Did dependencies install correctly?
- Is Python 3.10+?

```bash
python --version  # Should be 3.10+
pwd  # Should be in patterns/XX-pattern-name/
```

### "Too many API requests" error

**You're hitting rate limits!**

**Solution**:
```python
# Add rate limiting
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=50, period=60)  # 50 per minute
def rate_limited_query(q):
    return rag_query(q)
```

### Costs higher than expected

**Common causes**:
1. **No caching** - Repeated queries hitting API
2. **Wrong model** - Using GPT-4 instead of GPT-3.5
3. **Too many candidates** - Retrieving 100 when 20 enough
4. **Query decomposition** - Multiplies cost 3x

**Solutions**:
- Add caching (30-50% savings)
- Use cheaper models for simple queries
- Reduce candidate count
- Use query decomposition only for complex queries

---

## Best Practices

### Should I implement all patterns?

**No!** Start simple:

1. **Week 1**: Metadata Filtering (if you have metadata)
2. **Week 2**: Re-ranking (biggest quality boost)
3. **Week 3**: Semantic Chunking (foundation)
4. **Week 4+**: HyDE or Query Decomposition (if needed)

**Measure after each** - Only add more if needed!

### How often should I re-index?

**Depends on content freshness**:

- **Static content** (docs): Monthly or when updated
- **Semi-static** (blog): Weekly
- **Dynamic** (news): Daily
- **Real-time** (chat): Continuous

**For semantic chunking**: Re-chunk when documents change

### What metrics should I track?

**Quality metrics**:
- Precision@5 (top 5 results relevant?)
- User satisfaction (star ratings)
- Answer completeness (covers question?)

**Technical metrics**:
- Latency (P50, P95, P99)
- Cost per query
- Error rate

**Business metrics**:
- Support ticket reduction
- User retention
- Time-to-answer

### How do I stay up to date?

- **Watch this repo** - Get notified of updates
- **Follow RAG research** - Papers, blog posts
- **Join communities** - Discord, Reddit, forums
- **Experiment** - Try new patterns on your data

---

## Still Have Questions?

- Check the [Glossary](glossary.md) for term definitions
- Read [Pattern Comparison](../guides/comparison.md) for detailed analysis
- Use [Cost Calculator](../tools/cost-calculator.md) for estimates
- See [Why It Matters](../showcase/why-it-matters.md) for impact stories

**Still stuck?** [Open an issue](https://github.com/PeteSumners/rag-showroom/issues) or [start a discussion](https://github.com/PeteSumners/rag-showroom/discussions)!
