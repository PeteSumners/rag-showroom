# Production Integration

Learn how to integrate RAG patterns into your production applications.

## Quick Start Examples

### Basic RAG with Anthropic Claude

```python
from anthropic import Anthropic
import chromadb

# Initialize clients
client = Anthropic(api_key="your-api-key")
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("docs")

# Add documents
collection.add(
    documents=["Python is a programming language", "JavaScript runs in browsers"],
    ids=["doc1", "doc2"]
)

# Query
def rag_query(question: str) -> str:
    # Retrieve
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n".join(results['documents'][0])

    # Generate
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }]
    )

    return message.content[0].text

# Use it
answer = rag_query("What is Python?")
print(answer)
```

### With Semantic Chunking

```python
from patterns.semantic_chunking import SemanticChunker

# Chunk documents
chunker = SemanticChunker(similarity_threshold=0.15)
chunks = chunker.chunk_document(long_document)

# Add to vector DB
for i, chunk in enumerate(chunks):
    collection.add(
        documents=[chunk.text],
        ids=[f"chunk_{i}"],
        metadatas=[{"source": "doc1", "chunk_id": chunk.id}]
    )
```

### With Metadata Filtering

```python
# Add with metadata
collection.add(
    documents=["Python 3.12 release notes"],
    ids=["doc_py312"],
    metadatas=[{
        "version": "3.12",
        "language": "python",
        "type": "release_notes",
        "date": "2023-10-02"
    }]
)

# Query with filters
results = collection.query(
    query_texts=["What's new?"],
    n_results=5,
    where={
        "version": "3.12",
        "language": "python"
    }
)
```

### With Re-ranking

```python
from sentence_transformers import CrossEncoder

# First stage: Vector search
candidates = collection.query(
    query_texts=[question],
    n_results=50  # Get more candidates
)

# Second stage: Re-rank
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
pairs = [[question, doc] for doc in candidates['documents'][0]]
scores = reranker.predict(pairs)

# Sort by re-ranking scores
reranked = sorted(
    zip(candidates['documents'][0], scores),
    key=lambda x: x[1],
    reverse=True
)[:5]  # Top 5 after re-ranking
```

### With HyDE

```python
def hyde_query(question: str) -> str:
    # Generate hypothetical answer
    hypothesis = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"Generate a concise answer to: {question}"
        }]
    ).content[0].text

    # Search with hypothesis (not original question!)
    results = collection.query(query_texts=[hypothesis], n_results=5)

    # Generate final answer
    context = "\n".join(results['documents'][0])
    return generate_answer(context, question)
```

### With Query Decomposition

```python
def decompose_and_retrieve(complex_question: str) -> list:
    # Decompose
    sub_questions = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        messages=[{
            "role": "user",
            "content": f"Break this into 2-4 sub-questions:\n{complex_question}"
        }]
    ).content[0].text.split('\n')

    # Retrieve for each
    all_docs = []
    for sub_q in sub_questions:
        results = collection.query(query_texts=[sub_q], n_results=2)
        all_docs.extend(results['documents'][0])

    # Deduplicate
    return list(set(all_docs))
```

## Production Stack Example

Complete production-ready implementation:

```python
from typing import List, Dict, Any
from anthropic import Anthropic
import chromadb
from sentence_transformers import CrossEncoder
from dataclasses import dataclass
import logging

@dataclass
class RAGConfig:
    model: str = "claude-3-5-sonnet-20241022"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_candidates: int = 50
    top_k_final: int = 5
    rerank: bool = True
    use_metadata: bool = True

class ProductionRAG:
    """Production-ready RAG system with multiple patterns"""

    def __init__(self, config: RAGConfig, api_key: str):
        self.config = config
        self.client = Anthropic(api_key=api_key)
        self.chroma = chromadb.Client()
        self.collection = None
        self.reranker = None
        self.logger = logging.getLogger(__name__)

        if config.rerank:
            self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    def initialize_collection(self, name: str):
        """Initialize vector database collection"""
        self.collection = self.chroma.get_or_create_collection(name)
        self.logger.info(f"Initialized collection: {name}")

    def add_documents(
        self,
        documents: List[str],
        metadatas: List[Dict[str, Any]] = None
    ):
        """Add documents with semantic chunking"""
        from patterns.semantic_chunking import SemanticChunker

        chunker = SemanticChunker(similarity_threshold=0.15)
        all_chunks = []
        all_metadatas = []

        for idx, doc in enumerate(documents):
            chunks = chunker.chunk_document(doc)
            for chunk in chunks:
                all_chunks.append(chunk.text)

                # Combine doc metadata with chunk info
                chunk_meta = {
                    "doc_id": idx,
                    "chunk_id": chunk.id,
                    "char_count": chunk.char_count
                }
                if metadatas and idx < len(metadatas):
                    chunk_meta.update(metadatas[idx])

                all_metadatas.append(chunk_meta)

        # Add to vector DB
        self.collection.add(
            documents=all_chunks,
            ids=[f"chunk_{i}" for i in range(len(all_chunks))],
            metadatas=all_metadatas
        )

        self.logger.info(f"Added {len(all_chunks)} chunks from {len(documents)} documents")

    def query(
        self,
        question: str,
        filters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Query with optional metadata filtering and re-ranking"""

        # Stage 1: Vector search
        query_kwargs = {
            "query_texts": [question],
            "n_results": self.config.top_k_candidates
        }

        if filters and self.config.use_metadata:
            query_kwargs["where"] = filters

        try:
            results = self.collection.query(**query_kwargs)
        except Exception as e:
            self.logger.error(f"Query failed: {e}")
            return {"error": str(e)}

        documents = results['documents'][0]
        metadatas = results['metadatas'][0]

        # Stage 2: Re-ranking (optional)
        if self.config.rerank and self.reranker:
            pairs = [[question, doc] for doc in documents]
            scores = self.reranker.predict(pairs)

            # Sort by re-ranking scores
            ranked = sorted(
                zip(documents, metadatas, scores),
                key=lambda x: x[2],
                reverse=True
            )[:self.config.top_k_final]

            documents = [d for d, _, _ in ranked]
            metadatas = [m for _, m, _ in ranked]

        # Stage 3: Generate answer
        context = "\n\n".join([
            f"[Doc {i+1}] {doc}"
            for i, doc in enumerate(documents[:self.config.top_k_final])
        ])

        answer = self._generate_answer(context, question)

        return {
            "answer": answer,
            "sources": documents[:self.config.top_k_final],
            "metadatas": metadatas[:self.config.top_k_final]
        }

    def _generate_answer(self, context: str, question: str) -> str:
        """Generate answer using Claude"""
        try:
            message = self.client.messages.create(
                model=self.config.model,
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"""Use the following context to answer the question.
If the answer isn't in the context, say so.

Context:
{context}

Question: {question}

Answer:"""
                }]
            )
            return message.content[0].text

        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            return f"Error generating answer: {str(e)}"

# Usage
config = RAGConfig(rerank=True, use_metadata=True)
rag = ProductionRAG(config, api_key="your-key")
rag.initialize_collection("my_docs")

# Add documents
rag.add_documents(
    documents=["Python is...", "JavaScript is..."],
    metadatas=[
        {"language": "python", "version": "3.12"},
        {"language": "javascript", "version": "es6"}
    ]
)

# Query
result = rag.query(
    "What's new in Python?",
    filters={"language": "python"}
)

print(result["answer"])
print(f"Sources: {len(result['sources'])}")
```

## Deployment Checklist

### Before Production

- [ ] **Test with real data** - Not just examples
- [ ] **Measure baseline performance** - Latency, quality, cost
- [ ] **Set up monitoring** - Errors, latency, costs
- [ ] **Configure logging** - Debug issues easily
- [ ] **Add error handling** - Graceful degradation
- [ ] **Set rate limits** - Protect API quotas
- [ ] **Cache common queries** - Reduce costs
- [ ] **Version control** - Track changes
- [ ] **Document configuration** - Team knowledge
- [ ] **Plan rollback** - Quick recovery

### Performance Optimization

```python
# Caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_query(question: str) -> str:
    return rag.query(question)

# Async for parallel queries
import asyncio

async def batch_query(questions: List[str]):
    tasks = [query_async(q) for q in questions]
    return await asyncio.gather(*tasks)

# Rate limiting
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)  # 100 calls per minute
def rate_limited_query(question: str):
    return rag.query(question)
```

### Monitoring

```python
import time
from prometheus_client import Counter, Histogram

# Metrics
query_counter = Counter('rag_queries_total', 'Total RAG queries')
query_duration = Histogram('rag_query_duration_seconds', 'Query duration')
error_counter = Counter('rag_errors_total', 'Total errors')

def monitored_query(question: str):
    query_counter.inc()

    with query_duration.time():
        try:
            result = rag.query(question)
            return result
        except Exception as e:
            error_counter.inc()
            raise
```

### Cost Management

```python
# Token counting
def estimate_cost(text: str, model: str = "claude-3-sonnet"):
    tokens = len(text) / 4  # Rough estimate

    costs = {
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},  # per 1K tokens
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125}
    }

    input_cost = (tokens / 1000) * costs[model]["input"]
    return input_cost

# Use cheaper models for candidates
def cost_optimized_query(question: str):
    # Use Haiku for initial processing
    hypothesis = generate_with_haiku(question)

    # Use Sonnet only for final answer
    return generate_with_sonnet(context, question)
```

## Common Issues & Solutions

### Issue: High Latency

**Solutions:**
- Reduce `top_k_candidates` (50 → 20)
- Disable re-ranking for non-critical queries
- Cache frequent queries
- Use faster embedding models

### Issue: Low Quality Results

**Solutions:**
- Enable re-ranking
- Add metadata filtering
- Improve chunking (semantic vs fixed)
- Use better embedding models
- Increase `top_k_final`

### Issue: High Costs

**Solutions:**
- Use cheaper models (Haiku instead of Sonnet)
- Cache results
- Reduce context size
- Batch queries
- Use local embedding models

### Issue: Wrong Document Versions

**Solutions:**
- Add metadata filtering
- Tag documents with versions
- Filter by date
- Separate collections per version

## Next Steps

1. **Start simple** - Basic vector search first
2. **Measure** - Baseline performance
3. **Add patterns** - One at a time
4. **Benchmark** - Measure improvement
5. **Deploy** - With monitoring
6. **Iterate** - Based on metrics

---

**Questions?** [Open an issue](https://github.com/PeteSumners/rag-showroom/issues) or check the [patterns](../patterns/overview.md)!
