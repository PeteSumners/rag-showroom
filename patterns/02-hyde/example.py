#!/usr/bin/env python3
"""
HyDE (Hypothetical Document Embeddings) Example

Demonstrates query expansion by generating hypothetical answers and using them
for retrieval instead of the original query.
"""

from typing import List, Tuple
from dataclasses import dataclass
import random

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@dataclass
class Document:
    """A document in the knowledge base"""
    id: str
    content: str
    title: str


class MockLLM:
    """
    Mock LLM for generating hypothetical answers.

    In production, use actual LLM APIs (Anthropic, OpenAI, etc.)
    """

    def generate_hypothesis(self, query: str) -> str:
        """
        Generate a hypothetical answer to the query.

        Engineering decision: The hypothesis doesn't need to be correct!
        We just want it to be in the same format (declarative statement)
        as our knowledge base documents.
        """
        # Simplified hypothesis generation based on query patterns
        if "what is" in query.lower() or "define" in query.lower():
            # Extract subject
            subject = query.lower().replace("what is", "").replace("?", "").strip()
            return f"{subject.title()} is a technique that combines multiple approaches to improve system performance and accuracy."

        elif "how" in query.lower():
            return "This process works by analyzing input data, applying transformations, and generating outputs based on learned patterns."

        else:
            return "This technique involves processing data through multiple stages to achieve better results than traditional approaches."


class MockEmbedding:
    """
    Mock embedding model using simple keyword overlap.

    In production, use actual embedding models (OpenAI, sentence-transformers, etc.)
    """

    def embed(self, text: str) -> List[float]:
        """
        Create a simple embedding based on keywords.

        Engineering decision: Using word presence as embedding dimensions.
        Real embeddings are dense vectors from neural networks.
        """
        # Simple keyword-based "embedding"
        keywords = ["rag", "retrieval", "generation", "embedding", "vector",
                   "semantic", "search", "llm", "context", "query",
                   "document", "knowledge", "answer", "database"]

        embedding = []
        text_lower = text.lower()
        for keyword in keywords:
            # Count keyword presence (normalized)
            count = text_lower.count(keyword)
            embedding.append(min(count / 3.0, 1.0))  # Normalize to [0, 1]

        return embedding

    def similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """Calculate cosine similarity between embeddings"""
        if len(emb1) != len(emb2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(emb1, emb2))
        norm1 = sum(a * a for a in emb1) ** 0.5
        norm2 = sum(b * b for b in emb2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)


class HyDERetriever:
    """
    HyDE retriever that uses hypothetical document embeddings.

    Key insight: Generate what the answer might look like, then search for
    documents that match that hypothetical answer.
    """

    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.llm = MockLLM()
        self.embedding = MockEmbedding()

        # Pre-compute document embeddings
        self.doc_embeddings = {
            doc.id: self.embedding.embed(doc.content)
            for doc in documents
        }

    def retrieve_naive(self, query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
        """
        Naive retrieval: embed query directly.

        This is the baseline approach - often suboptimal when queries are
        questions but documents are declarative statements.
        """
        query_embedding = self.embedding.embed(query)

        # Calculate similarities
        results = []
        for doc in self.documents:
            doc_embedding = self.doc_embeddings[doc.id]
            similarity = self.embedding.similarity(query_embedding, doc_embedding)
            results.append((doc, similarity))

        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def retrieve_hyde(self, query: str, top_k: int = 3) -> Tuple[str, List[Tuple[Document, float]]]:
        """
        HyDE retrieval: generate hypothesis, embed it, then search.

        Engineering decision: The hypothesis bridges the vocabulary gap between
        question-format queries and declarative documents.
        """
        # Step 1: Generate hypothetical answer
        hypothesis = self.llm.generate_hypothesis(query)

        # Step 2: Embed the hypothesis (not the query!)
        hypothesis_embedding = self.embedding.embed(hypothesis)

        # Step 3: Retrieve using hypothesis embedding
        results = []
        for doc in self.documents:
            doc_embedding = self.doc_embeddings[doc.id]
            similarity = self.embedding.similarity(hypothesis_embedding, doc_embedding)
            results.append((doc, similarity))

        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)
        return hypothesis, results[:top_k]


def create_sample_knowledge_base() -> List[Document]:
    """Create a sample knowledge base about RAG systems"""
    return [
        Document(
            id="doc1",
            title="RAG Fundamentals",
            content="RAG (Retrieval-Augmented Generation) combines retrieval systems with "
                   "generation models to produce accurate answers. The system retrieves relevant "
                   "context from a knowledge base and uses it to generate informed responses."
        ),
        Document(
            id="doc2",
            title="Vector Embeddings",
            content="Vector embeddings are numerical representations of text in high-dimensional "
                   "space. They capture semantic meaning and enable similarity search through "
                   "distance metrics like cosine similarity."
        ),
        Document(
            id="doc3",
            title="Semantic Search",
            content="Semantic search uses embeddings to find documents by meaning rather than "
                   "keywords. It matches the intent and context of queries with relevant documents "
                   "in the vector database."
        ),
        Document(
            id="doc4",
            title="LLM Integration",
            content="Large Language Models generate natural language responses based on retrieved "
                   "context. They synthesize information from multiple sources to provide coherent "
                   "and contextually appropriate answers."
        ),
        Document(
            id="doc5",
            title="Query Processing",
            content="Query processing transforms user questions into suitable formats for retrieval. "
                   "This may involve expansion, reformulation, or embedding to improve search accuracy."
        ),
    ]


def visualize_comparison(query: str, hypothesis: str, naive_results: List[Tuple[Document, float]],
                        hyde_results: List[Tuple[Document, float]]):
    """Display comparison between naive and HyDE retrieval"""

    console.print()
    console.print("[bold cyan]>>> USER QUERY[/bold cyan]")
    console.print(Panel(query, border_style="cyan", padding=(0, 2)))

    console.print()
    console.print("[bold yellow]>>> GENERATED HYPOTHESIS[/bold yellow]")
    console.print(Panel(
        f"[italic]{hypothesis}[/italic]",
        border_style="yellow",
        padding=(0, 2)
    ))

    # Naive results
    console.print()
    console.print("[bold red]>>> NAIVE RETRIEVAL (Direct Query Embedding)[/bold red]")
    table_naive = Table(border_style="red", show_header=True, header_style="bold red")
    table_naive.add_column("Rank", width=6)
    table_naive.add_column("Document", width=40)
    table_naive.add_column("Score", width=10)

    for i, (doc, score) in enumerate(naive_results, 1):
        table_naive.add_row(
            str(i),
            doc.title,
            f"{score:.3f}"
        )

    console.print(table_naive)

    # HyDE results
    console.print()
    console.print("[bold green]>>> HYDE RETRIEVAL (Hypothesis Embedding)[/bold green]")
    table_hyde = Table(border_style="green", show_header=True, header_style="bold green")
    table_hyde.add_column("Rank", width=6)
    table_hyde.add_column("Document", width=40)
    table_hyde.add_column("Score", width=10)

    for i, (doc, score) in enumerate(hyde_results, 1):
        table_hyde.add_row(
            str(i),
            doc.title,
            f"{score:.3f}"
        )

    console.print(table_hyde)

    # Key insight
    console.print()
    console.print("[bold yellow]>>> KEY INSIGHT[/bold yellow]")
    console.print(Panel(
        "[bold]HyDE retrieves using a hypothetical answer format,[/bold]\n"
        "which better matches declarative documents than question-format queries.",
        border_style="yellow",
        padding=(1, 2)
    ))


def main():
    """Run HyDE demo"""

    # Header
    console.print()
    console.print("=" * 65, style="bold blue")
    console.print("  HYDE (HYPOTHETICAL DOCUMENT EMBEDDINGS)", style="bold blue")
    console.print("=" * 65, style="bold blue")
    console.print()

    # Create knowledge base
    knowledge_base = create_sample_knowledge_base()
    retriever = HyDERetriever(knowledge_base)

    # Test query
    query = "What is RAG and how does it work?"

    console.print("[cyan]Processing query with both methods...[/cyan]")

    # Naive retrieval
    naive_results = retriever.retrieve_naive(query, top_k=3)

    # HyDE retrieval
    hypothesis, hyde_results = retriever.retrieve_hyde(query, top_k=3)

    console.print("[green]SUCCESS: Retrieved results from both approaches[/green]")

    # Display comparison
    visualize_comparison(query, hypothesis, naive_results, hyde_results)

    console.print()
    console.print("[green]Demo complete![/green]")
    console.print()
    console.print("[dim]Try modifying the query to see different hypotheses:[/dim]")
    console.print("[dim]  - 'How do embeddings work?'[/dim]")
    console.print("[dim]  - 'Define semantic search'[/dim]")


if __name__ == "__main__":
    main()
