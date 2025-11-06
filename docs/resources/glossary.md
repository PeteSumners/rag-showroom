# Glossary

A comprehensive glossary of RAG and related terms used throughout this guide.

## Core Concepts

### RAG (Retrieval-Augmented Generation)
A technique that combines information retrieval with language model generation. The system retrieves relevant documents from a knowledge base and uses them as context for generating answers.

**Example**: When you ask "What is Python?", a RAG system retrieves Python documentation and uses it to generate an accurate answer.

### Vector Embedding
A numerical representation of text in high-dimensional space (typically 384-1536 dimensions). Similar texts have similar embeddings.

**Example**: "dog" and "puppy" have similar embeddings, while "dog" and "car" have very different embeddings.

### Semantic Search
Search based on meaning rather than exact keyword matching. Uses embeddings to find semantically similar content.

**Example**: Searching "quick canine" might return documents about "fast dogs" even though the words don't match exactly.

### Cosine Similarity
A metric for measuring how similar two vectors are, ranging from -1 (opposite) to 1 (identical). Used to compare embedding similarity.

**Formula**: `similarity = dot(A, B) / (norm(A) * norm(B))`

### Knowledge Base
A collection of documents that the RAG system can retrieve from. Also called a corpus or vector database.

**Example**: Your company's documentation, support articles, or research papers.

## Retrieval Patterns

### Chunking
Breaking long documents into smaller pieces for more precise retrieval.

**Why**: LLMs have context limits (4K-32K tokens), and smaller chunks retrieve more precisely.

### Semantic Chunking
Splitting documents at natural boundaries (topic shifts) rather than arbitrary character counts.

**Example**: Breaking a document after "In summary..." rather than mid-sentence.

### HyDE (Hypothetical Document Embeddings)
Generating a hypothetical answer to a query, then using that answer's embedding for retrieval.

**Why**: Bridges the vocabulary gap between questions and declarative documents.

### Re-ranking
A two-stage retrieval approach: (1) fast vector search retrieves candidates, (2) precise model ranks them.

**Example**: Vector search gets top 50 results, cross-encoder re-ranks to find best 5.

### Metadata Filtering
Pre-filtering documents by structured attributes (date, category, language) before vector search.

**Example**: Only search Python API v3 docs, ignore v1/v2.

### Query Decomposition
Breaking complex queries into simpler sub-questions for independent retrieval.

**Example**: "Compare X vs Y" → "What is X?" + "What is Y?" + "X vs Y differences"

## Technical Terms

### Embedding Model
A neural network that converts text into vector embeddings.

**Examples**:
- OpenAI `text-embedding-ada-002`
- Sentence Transformers `all-MiniLM-L6-v2`
- Anthropic embeddings

### Cross-Encoder
A model that jointly encodes a query and document together to score relevance. More accurate than comparing separate embeddings but slower.

**Use case**: Re-ranking in two-stage retrieval.

### Bi-Encoder
A model that separately encodes queries and documents. Faster than cross-encoders but less accurate.

**Use case**: Initial vector search.

### Vector Database
A database optimized for storing and searching vector embeddings.

**Examples**: Pinecone, Weaviate, ChromaDB, Qdrant, Milvus

### Dense Retrieval
Retrieval using dense vector embeddings (every dimension has a value).

**Contrast**: Sparse retrieval like BM25 (most dimensions are zero).

### Sparse Retrieval
Retrieval using sparse representations like TF-IDF or BM25.

**Example**: BM25 scores based on term frequency and rarity.

### Hybrid Search
Combining dense (vector) and sparse (BM25) retrieval.

**Why**: Gets benefits of both semantic and keyword matching.

## Metrics

### Precision
Percentage of retrieved documents that are relevant.

**Formula**: `relevant_retrieved / total_retrieved`

**Example**: If 4 out of 5 retrieved docs are relevant, precision = 0.8

### Recall
Percentage of relevant documents that were retrieved.

**Formula**: `relevant_retrieved / total_relevant`

**Example**: If 4 out of 6 relevant docs were retrieved, recall = 0.67

### Precision@K
Precision for the top K results (e.g., Precision@5 for top 5 results).

**Why**: Users typically only look at top results.

### Recall@K
Recall considering only top K results.

### Mean Reciprocal Rank (MRR)
Average of reciprocal ranks of first relevant result across queries.

**Formula**: `MRR = average(1/rank_of_first_relevant)`

**Example**: If first relevant doc is rank 3, contribution = 1/3 = 0.33

### NDCG (Normalized Discounted Cumulative Gain)
Metric that considers both relevance and ranking position.

**Why**: Rewards having highly relevant docs at top positions.

## LLM Terms

### Context Window
Maximum amount of text an LLM can process at once.

**Examples**:
- GPT-3.5: 4K tokens
- GPT-4: 8K-32K tokens
- Claude 2: 100K tokens

### Token
Unit of text for LLMs (roughly 4 characters in English).

**Example**: "Hello world" ≈ 2 tokens

### Prompt
The input text given to an LLM.

**RAG Context**: Usually includes retrieved documents plus the user's query.

### Temperature
Controls randomness in LLM generation (0 = deterministic, 1 = creative).

**RAG Usage**: Usually set low (0-0.3) for factual answers.

### Hallucination
When an LLM generates false information not supported by the input.

**RAG Benefit**: Grounding in retrieved documents reduces hallucinations.

## Advanced Concepts

### Top-K Retrieval
Retrieving the K most similar documents.

**Example**: top_k=5 returns 5 best matches.

### Similarity Threshold
Minimum similarity score required for retrieval.

**Example**: Only return documents with cosine similarity > 0.7

### Chunk Overlap
When chunking, how much text to repeat between adjacent chunks.

**Example**: 500 char chunks with 50 char overlap preserves context across boundaries.

### Parent-Child Retrieval
Storing small chunks for retrieval but using larger parent chunks for context.

**Why**: Precise retrieval + sufficient context for LLM.

### Self-Query
LLM extracts structured filters from natural language queries.

**Example**: "Recent Python docs" → `{language: "python", date: {$gte: "2024-01-01"}}`

### Agentic RAG
LLM decides when and what to retrieve based on the task.

**Example**: "The model determines it needs pricing info, retrieves it, then answers."

### Recursive Retrieval
Multi-hop retrieval where initial results inform subsequent retrievals.

**Example**: Retrieve about "neural networks", then retrieve about specific architectures mentioned.

## Performance Terms

### Latency
Time from query submission to result return.

**Example**: "Average latency: 250ms"

### Throughput
Queries processed per second.

**Example**: "Handles 100 QPS (queries per second)"

### P95 Latency
Latency at 95th percentile (95% of queries are faster).

**Why**: Captures tail latency that affects user experience.

### Cold Start
First query being slower than subsequent queries due to initialization.

**Example**: First embedding takes 500ms, subsequent take 50ms.

## Common Abbreviations

- **RAG** - Retrieval-Augmented Generation
- **LLM** - Large Language Model
- **NLP** - Natural Language Processing
- **QPS** - Queries Per Second
- **TF-IDF** - Term Frequency-Inverse Document Frequency
- **BM25** - Best Matching 25 (ranking function)
- **FAISS** - Facebook AI Similarity Search
- **HyDE** - Hypothetical Document Embeddings
- **MRR** - Mean Reciprocal Rank
- **NDCG** - Normalized Discounted Cumulative Gain

## Further Reading

- [RAG Papers](https://github.com/yangzhipeng1108/RAG-Papers) - Research papers on RAG
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction) - RAG framework documentation
- [Pinecone Learning Center](https://www.pinecone.io/learn/) - Vector search concepts

---

**Don't see a term?** [Open an issue](https://github.com/PeteSumners/rag-showroom/issues) to request it!
