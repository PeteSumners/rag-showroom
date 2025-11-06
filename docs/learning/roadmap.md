# Learning Roadmap

Your path to mastering RAG patterns, from absolute beginner to production expert.

## 🎯 Learning Paths

Choose your starting point:

=== "Complete Beginner"
    **You're new to RAG** → Start here

    [Week 1: Foundations](#week-1-foundations){ .md-button .md-button--primary }

=== "Familiar with RAG"
    **You've built basic RAG** → Skip to patterns

    [Week 2: Patterns](#week-2-core-patterns){ .md-button .md-button--primary }

=== "Ready for Production"
    **You need production setup** → Advanced topics

    [Week 4: Production](#week-4-production-deployment){ .md-button .md-button--primary }

## Complete Learning Path

### Week 1: Foundations

**Goal**: Understand RAG basics and run your first example

#### Day 1-2: RAG Fundamentals
- [ ] Read [Why This Matters](../showcase/why-it-matters.md)
- [ ] Understand the RAG architecture
- [ ] Learn key terms in the [Glossary](../resources/glossary.md)
- [ ] **Checkpoint**: Can you explain RAG in 30 seconds?

**Learning Resources**:
- 📄 [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- 📺 Video: "RAG Explained" (search YouTube)
- 📖 Read: First 3 glossary entries

#### Day 3-4: Setup & First Pattern
- [ ] [Install the guide](../getting-started/installation.md)
- [ ] Run your first pattern: [Semantic Chunking](../patterns/01-semantic-chunking.md)
- [ ] Understand the colored terminal output
- [ ] **Checkpoint**: Can you run `python example.py` successfully?

**Hands-on Exercise**:
```python
# Try different threshold values
chunker = SemanticChunker(similarity_threshold=0.1)  # Many small chunks
chunker = SemanticChunker(similarity_threshold=0.3)  # Fewer larger chunks
# What changes? Why?
```

#### Day 5-7: Pattern Selection Basics
- [ ] Read [Pattern Overview](../patterns/overview.md)
- [ ] Use the [Pattern Selector](../guides/choosing-pattern.md)
- [ ] Compare [all patterns](../guides/comparison.md)
- [ ] **Checkpoint**: Can you pick the right pattern for a use case?

**Practice**:
- Use case: "Customer support FAQ"
- Use case: "Multi-version API docs"
- Use case: "Research paper search"
- Which patterns for each?

**End of Week Assessment**:
- ✅ Can explain RAG to a colleague
- ✅ Ran at least one pattern example
- ✅ Can identify which pattern to use when

---

### Week 2: Core Patterns

**Goal**: Understand and implement all beginner patterns

#### Day 8-9: Semantic Chunking Deep Dive
- [ ] Read [full pattern docs](../patterns/01-semantic-chunking.md)
- [ ] Run example with your own text
- [ ] Implement in a mini-project
- [ ] **Checkpoint**: Can you chunk a 5-page document?

**Project**: Build a simple document chunker
```python
# Your own docs
my_document = "..." # Load your text
chunker = SemanticChunker(similarity_threshold=0.15)
chunks = chunker.chunk_document(my_document)
print(f"Created {len(chunks)} chunks")
```

#### Day 10-11: Re-ranking Mastery
- [ ] Read [Re-ranking pattern](../patterns/03-reranking.md)
- [ ] Understand two-stage retrieval
- [ ] Run the example
- [ ] **Checkpoint**: Explain why re-ranking improves precision

**Exercise**: Track how rankings change
```python
# Run the example and note:
# - Vector search top 5
# - Re-ranked top 5
# - What moved up? What moved down? Why?
```

#### Day 12-13: Metadata Filtering
- [ ] Read [Metadata Filtering](../patterns/04-metadata-filtering.md)
- [ ] Understand filter operators
- [ ] Run examples with different filters
- [ ] **Checkpoint**: Can you write complex filter queries?

**Practice Filters**:
```python
# Try these on your own data:
where={"version": "3.0", "language": "en"}
where={"date": {"$gte": "2024-01-01"}}
where={"$or": [{"type": "api"}, {"type": "sdk"}]}
```

#### Day 14: Week 2 Project
**Build**: A filtered search system
- Use semantic chunking for preprocessing
- Add metadata to your documents
- Implement filtered search
- Add re-ranking for precision

**Success Criteria**:
- Can search with version filter
- Results are relevant
- System handles 100+ documents

---

### Week 3: Intermediate Patterns

**Goal**: Master advanced patterns and combinations

#### Day 15-17: HyDE Pattern
- [ ] Read [HyDE pattern](../patterns/02-hyde.md)
- [ ] Understand hypothesis generation
- [ ] Run the example
- [ ] Implement with real LLM (optional)
- [ ] **Checkpoint**: Explain the vocabulary gap problem

**Advanced Exercise**:
```python
# Compare retrieval quality:
# 1. Direct query embedding
# 2. HyDE approach
# Which performs better for your use case?
```

#### Day 18-20: Query Decomposition
- [ ] Read [Query Decomposition](../patterns/05-query-decomposition.md)
- [ ] Understand sub-query generation
- [ ] Run examples
- [ ] Practice on complex queries
- [ ] **Checkpoint**: Can you decompose a 3-part query?

**Practice Queries**:
```
- "Compare Python vs JavaScript for web development"
- "What are the benefits and drawbacks of microservices?"
- "How do I set up, configure, and deploy feature X?"
```

#### Day 21: Pattern Combinations
- [ ] Read [Production Integration](../guides/production-integration.md)
- [ ] Study pattern stacks
- [ ] Understand complementary patterns
- [ ] **Checkpoint**: Can you design a stack for a use case?

**Design Exercise**:
- Use case: Enterprise documentation search
- Design your pattern stack
- Justify each choice
- Estimate costs using the [calculator](../tools/cost-calculator.md)

---

### Week 4: Production Deployment

**Goal**: Deploy production-ready RAG system

#### Day 22-23: Production Code
- [ ] Study [production example code](../guides/production-integration.md)
- [ ] Implement error handling
- [ ] Add logging and monitoring
- [ ] **Checkpoint**: Can you handle API failures gracefully?

**Checklist**:
```python
class ProductionRAG:
    # ✓ Error handling with retries
    # ✓ Logging for debugging
    # ✓ Rate limiting
    # ✓ Caching common queries
    # ✓ Cost tracking
    # ✓ Performance monitoring
```

#### Day 24-25: Optimization
- [ ] Profile your system
- [ ] Add caching
- [ ] Optimize retrieval
- [ ] Reduce costs
- [ ] **Checkpoint**: Can you explain your optimization choices?

**Metrics to Track**:
- Latency (P50, P95, P99)
- Cost per query
- Cache hit rate
- Error rate

#### Day 26-27: Monitoring & Iteration
- [ ] Set up metrics collection
- [ ] Create dashboards
- [ ] Define SLAs
- [ ] **Checkpoint**: Can you spot issues from metrics?

**Monitoring Setup**:
```python
# Key metrics:
- query_count
- query_duration_seconds
- error_rate
- pattern_usage
- cost_per_query
```

#### Day 28: Capstone Project
**Build**: Complete production RAG system

**Requirements**:
- Uses 2-3 patterns
- Error handling
- Monitoring
- Cost tracking
- Documentation

**Deliverables**:
- Working code
- README with setup instructions
- Performance metrics
- Cost analysis

---

## By Role

### For ML Engineers

**Focus on**:
- Pattern algorithms and trade-offs
- Embedding model selection
- Re-ranking model choice
- Performance optimization

**Key Patterns**: All, with emphasis on HyDE and Re-ranking

**Timeline**: 3-4 weeks

### For Software Engineers

**Focus on**:
- Production integration
- Error handling
- Monitoring and observability
- Cost optimization

**Key Patterns**: Semantic Chunking, Metadata Filtering, Re-ranking

**Timeline**: 2-3 weeks

### For Product Managers

**Focus on**:
- Pattern selection for use cases
- Cost vs quality trade-offs
- User impact metrics
- ROI analysis

**Key Resources**:
- [Pattern Comparison](../guides/comparison.md)
- [Why It Matters](../showcase/why-it-matters.md)
- [Cost Calculator](../tools/cost-calculator.md)

**Timeline**: 1-2 weeks

### For Data Scientists

**Focus on**:
- Evaluation metrics
- Benchmarking approaches
- Pattern effectiveness analysis
- Embedding quality

**Key Patterns**: All, with emphasis on evaluation methodology

**Timeline**: 3-4 weeks

## Learning Objectives

### After Week 1
- ✅ Understand RAG fundamentals
- ✅ Can run example code
- ✅ Can select appropriate patterns

### After Week 2
- ✅ Implemented 3 beginner patterns
- ✅ Built a mini-project
- ✅ Can explain trade-offs

### After Week 3
- ✅ Mastered intermediate patterns
- ✅ Can combine patterns effectively
- ✅ Designed a production stack

### After Week 4
- ✅ Deployed production system
- ✅ Implemented monitoring
- ✅ Optimized for cost and performance
- ✅ Can maintain and iterate

## Assessment Checklist

Use this to track your progress:

### Knowledge Check
- [ ] Can explain RAG in simple terms
- [ ] Know when to use each pattern
- [ ] Understand trade-offs (latency, cost, quality)
- [ ] Can read and interpret metrics
- [ ] Familiar with production considerations

### Practical Skills
- [ ] Ran all 5 pattern examples
- [ ] Modified examples with own data
- [ ] Built at least one mini-project
- [ ] Implemented error handling
- [ ] Set up monitoring

### Production Ready
- [ ] Deployed a working system
- [ ] Handled edge cases
- [ ] Optimized performance
- [ ] Documented your work
- [ ] Can explain your choices

## Next Steps After Completion

### Continue Learning
- Contribute new patterns
- Write blog posts about your experience
- Help others in discussions
- Build advanced projects

### Build Your Portfolio
- Share your capstone project
- Write case studies
- Present at meetups
- Contribute to this guide

### Production Experience
- Deploy at work
- Measure real impact
- Iterate based on metrics
- Share lessons learned

---

**Ready to start?** Begin with [Week 1: Foundations](#week-1-foundations) or jump to your level!

**Questions?** Check the [FAQ](#) or [open a discussion](https://github.com/PeteSumners/rag-showroom/discussions).
