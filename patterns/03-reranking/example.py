#!/usr/bin/env python3
"""
Re-ranking Example

Demonstrates two-stage retrieval: fast vector search for candidates,
then precise re-ranking for the best results.
"""

from typing import List, Tuple
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


@dataclass
class Document:
    """A document in the knowledge base"""
    id: str
    title: str
    content: str


class SimpleEmbedding:
    """Simple keyword-based embedding for demonstration"""

    def embed(self, text: str) -> List[float]:
        """Create simple embedding based on keyword presence"""
        keywords = ["rag", "retrieval", "semantic", "vector", "embedding",
                   "search", "llm", "context", "query", "rerank"]

        embedding = []
        text_lower = text.lower()
        for keyword in keywords:
            count = text_lower.count(keyword)
            embedding.append(min(count / 2.0, 1.0))

        return embedding

    def similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """Cosine similarity"""
        dot_product = sum(a * b for a, b in zip(emb1, emb2))
        norm1 = sum(a * a for a in emb1) ** 0.5
        norm2 = sum(b * b for b in emb2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)


class SimpleReRanker:
    """
    Simple re-ranking model using keyword relevance.

    In production, use cross-encoder models like:
    - cross-encoder/ms-marco-MiniLM-L-6-v2
    - or LLM-based scoring
    """

    def score(self, query: str, document: str) -> float:
        """
        Score query-document relevance.

        Engineering decision: Re-ranker considers more signals than vector
        similarity - exact matches, keyword density, document structure, etc.
        """
        query_lower = query.lower()
        doc_lower = document.lower()

        score = 0.0

        # Exact phrase match (strong signal)
        query_words = query_lower.split()
        for i in range(len(query_words)):
            for j in range(i + 1, len(query_words) + 1):
                phrase = " ".join(query_words[i:j])
                if phrase in doc_lower:
                    score += 2.0 * (j - i)  # Longer phrases = higher score

        # Individual keyword match
        for word in query_words:
            if len(word) > 3:  # Skip short words
                count = doc_lower.count(word)
                score += count * 0.5

        # Keyword density (penalize very long docs that mention keywords once)
        if len(doc_lower) > 0:
            density = score / (len(doc_lower) / 100)
            score = score * (1 + density * 0.1)

        return score


class ReRankingRetriever:
    """
    Two-stage retrieval: vector search + re-ranking.

    Key insight: Cast a wide net with fast vector search, then use a
    precise model to pick the best results.
    """

    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.embedding = SimpleEmbedding()
        self.reranker = SimpleReRanker()

        # Pre-compute document embeddings
        self.doc_embeddings = {
            doc.id: self.embedding.embed(doc.content)
            for doc in documents
        }

    def retrieve_vector_only(self, query: str, top_k: int = 5) -> List[Tuple[Document, float]]:
        """
        Baseline: vector search only.

        Fast but less precise - relies solely on embedding similarity.
        """
        query_embedding = self.embedding.embed(query)

        results = []
        for doc in self.documents:
            doc_embedding = self.doc_embeddings[doc.id]
            similarity = self.embedding.similarity(query_embedding, doc_embedding)
            results.append((doc, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def retrieve_with_reranking(self, query: str, top_k: int = 5,
                               candidate_multiplier: int = 3) -> Tuple[List[Tuple[Document, float]], List[Tuple[Document, float]]]:
        """
        Two-stage retrieval: vector search + re-ranking.

        Engineering decision: Retrieve more candidates than needed (3-10x),
        then use re-ranker to select the most relevant ones.
        """
        # Stage 1: Vector search for candidates
        candidate_count = top_k * candidate_multiplier
        query_embedding = self.embedding.embed(query)

        vector_results = []
        for doc in self.documents:
            doc_embedding = self.doc_embeddings[doc.id]
            similarity = self.embedding.similarity(query_embedding, doc_embedding)
            vector_results.append((doc, similarity))

        vector_results.sort(key=lambda x: x[1], reverse=True)
        candidates = vector_results[:candidate_count]

        # Stage 2: Re-rank candidates
        reranked_results = []
        for doc, vector_score in candidates:
            rerank_score = self.reranker.score(query, doc.content)
            reranked_results.append((doc, rerank_score))

        reranked_results.sort(key=lambda x: x[1], reverse=True)
        final_results = reranked_results[:top_k]

        return candidates, final_results


def create_sample_documents() -> List[Document]:
    """Create sample knowledge base about RAG systems"""
    return [
        Document(
            id="doc1",
            title="RAG Overview",
            content="Retrieval-Augmented Generation combines retrieval with language models. "
                   "It searches a knowledge base and uses retrieved context for generation."
        ),
        Document(
            id="doc2",
            title="Semantic Search Fundamentals",
            content="Semantic search uses vector embeddings to find relevant documents. "
                   "Unlike keyword search, it understands meaning and context."
        ),
        Document(
            id="doc3",
            title="Advanced RAG: Re-ranking",
            content="Re-ranking improves retrieval accuracy by re-scoring vector search results. "
                   "It uses cross-encoders or LLMs to identify the most relevant documents."
        ),
        Document(
            id="doc4",
            title="Vector Databases",
            content="Vector databases store and query embeddings efficiently. "
                   "They enable fast similarity search across millions of documents."
        ),
        Document(
            id="doc5",
            title="Embedding Models",
            content="Embedding models convert text into dense vectors that capture semantic meaning. "
                   "Popular options include OpenAI embeddings and sentence-transformers."
        ),
        Document(
            id="doc6",
            title="Query Optimization",
            content="Query optimization techniques improve retrieval quality. "
                   "Methods include query expansion, reformulation, and decomposition."
        ),
        Document(
            id="doc7",
            title="RAG Evaluation",
            content="Evaluating RAG systems requires measuring both retrieval and generation quality. "
                   "Metrics include precision, recall, and end-to-end answer accuracy."
        ),
        Document(
            id="doc8",
            title="Context Window Management",
            content="Managing context windows is crucial for RAG performance. "
                   "Too much context wastes tokens, too little reduces answer quality."
        ),
    ]


def visualize_comparison(query: str, vector_results: List[Tuple[Document, float]],
                        candidates: List[Tuple[Document, float]],
                        reranked_results: List[Tuple[Document, float]]):
    """Display comparison between vector-only and re-ranked retrieval"""

    console.print()
    console.print("[bold cyan]>>> USER QUERY[/bold cyan]")
    console.print(Panel(query, border_style="cyan", padding=(0, 2)))

    # Vector-only results
    console.print()
    console.print("[bold red]>>> VECTOR SEARCH ONLY (Baseline)[/bold red]")
    table_vector = Table(border_style="red", show_header=True, header_style="bold red")
    table_vector.add_column("Rank", width=6)
    table_vector.add_column("Document", width=35)
    table_vector.add_column("Vector Score", width=12)

    for i, (doc, score) in enumerate(vector_results, 1):
        table_vector.add_row(str(i), doc.title, f"{score:.4f}")

    console.print(table_vector)

    # Candidates from Stage 1
    console.print()
    console.print("[bold yellow]>>> STAGE 1: Vector Candidates[/bold yellow]")
    console.print(f"[dim]Retrieved {len(candidates)} candidates for re-ranking...[/dim]")

    # Re-ranked results
    console.print()
    console.print("[bold green]>>> STAGE 2: Re-ranked Results[/bold green]")
    table_rerank = Table(border_style="green", show_header=True, header_style="bold green")
    table_rerank.add_column("Rank", width=6)
    table_rerank.add_column("Document", width=35)
    table_rerank.add_column("Rerank Score", width=12)

    for i, (doc, score) in enumerate(reranked_results, 1):
        table_rerank.add_row(str(i), doc.title, f"{score:.4f}")

    console.print(table_rerank)

    # Key insight
    console.print()
    console.print("[bold yellow]>>> KEY INSIGHT[/bold yellow]")
    console.print(Panel(
        "[bold]Re-ranking catches what vector search misses[/bold]\n"
        "by using a more precise model to score query-document relevance.",
        border_style="yellow",
        padding=(1, 2)
    ))


def main():
    """Run re-ranking demo"""

    # Header
    console.print()
    console.print("=" * 65, style="bold blue")
    console.print("  RE-RANKING: TWO-STAGE RETRIEVAL", style="bold blue")
    console.print("=" * 65, style="bold blue")
    console.print()

    # Create knowledge base
    documents = create_sample_documents()
    retriever = ReRankingRetriever(documents)

    # Test query
    query = "How does re-ranking improve RAG accuracy?"

    console.print("[cyan]Processing query with both methods...[/cyan]")

    # Vector-only retrieval
    vector_results = retriever.retrieve_vector_only(query, top_k=5)

    # Two-stage retrieval with re-ranking
    candidates, reranked_results = retriever.retrieve_with_reranking(query, top_k=5, candidate_multiplier=3)

    console.print("[green]SUCCESS: Retrieved and re-ranked results[/green]")

    # Display comparison
    visualize_comparison(query, vector_results, candidates, reranked_results)

    console.print()
    console.print("[green]Demo complete![/green]")
    console.print()
    console.print("[dim]Try different queries:[/dim]")
    console.print("[dim]  - 'What are vector databases?'[/dim]")
    console.print("[dim]  - 'How to evaluate RAG systems?'[/dim]")


if __name__ == "__main__":
    main()
