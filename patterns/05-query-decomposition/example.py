#!/usr/bin/env python3
"""
Query Decomposition Example

Demonstrates breaking complex queries into focused sub-questions for
better retrieval coverage.
"""

from typing import List, Tuple, Set
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

console = Console()


@dataclass
class Document:
    """A document in the knowledge base"""
    id: str
    title: str
    content: str


class MockLLM:
    """Mock LLM for query decomposition"""

    def decompose_query(self, query: str) -> List[str]:
        """
        Decompose complex query into sub-questions.

        Engineering decision: Identify distinct aspects that need separate
        retrieval. In production, use actual LLM for intelligent decomposition.
        """
        query_lower = query.lower()

        # Pattern: "compare X vs Y"
        if "compare" in query_lower or " vs " in query_lower:
            if "asyncio" in query_lower and "threading" in query_lower:
                return [
                    "What is asyncio and how does it work?",
                    "What is threading and how does it work?",
                    "What are the key differences between asyncio and threading?"
                ]

        # Pattern: "benefits and drawbacks"
        if ("benefit" in query_lower or "advantage" in query_lower) and \
           ("drawback" in query_lower or "disadvantage" in query_lower):
            subject = "RAG systems"  # Extract subject
            return [
                f"What are the benefits of {subject}?",
                f"What are the drawbacks of {subject}?",
                f"When should you use {subject}?"
            ]

        # Pattern: "how to... and..."
        if "how" in query_lower and " and " in query_lower:
            return [
                "How do I set up the feature?",
                "How do I use the feature?",
                "What are common issues?"
            ]

        # Default: split on "and"
        if " and " in query_lower:
            parts = query.split(" and ")
            return [part.strip() + "?" if not part.endswith("?") else part.strip()
                   for part in parts]

        # Single question - no decomposition needed
        return [query]


class SimpleEmbedding:
    """Simple keyword-based embedding"""

    def embed(self, text: str) -> List[float]:
        keywords = ["asyncio", "threading", "performance", "concurrency",
                   "parallel", "event", "loop", "cpu", "io", "blocking"]

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


class QueryDecompositionRetriever:
    """
    Retriever with query decomposition.

    Key insight: Multiple focused searches provide better coverage than
    one broad search for complex queries.
    """

    def __init__(self, documents: List[Document]):
        self.documents = documents
        self.llm = MockLLM()
        self.embedding = SimpleEmbedding()

        # Pre-compute embeddings
        self.doc_embeddings = {
            doc.id: self.embedding.embed(doc.content)
            for doc in documents
        }

    def retrieve_single(self, query: str, top_k: int = 3) -> List[Tuple[Document, float]]:
        """
        Baseline: single query retrieval.

        For complex queries, this often returns vague or incomplete results.
        """
        query_embedding = self.embedding.embed(query)

        results = []
        for doc in self.documents:
            doc_embedding = self.doc_embeddings[doc.id]
            similarity = self.embedding.similarity(query_embedding, doc_embedding)
            results.append((doc, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def retrieve_decomposed(self, query: str, top_k_per_question: int = 2) -> Tuple[List[str], dict, List[Document]]:
        """
        Query decomposition retrieval.

        Engineering decision: Break complex queries into sub-questions,
        retrieve for each, then combine results. This ensures comprehensive
        coverage of all query aspects.
        """
        # Step 1: Decompose query
        sub_questions = self.llm.decompose_query(query)

        # Step 2: Retrieve for each sub-question
        sub_results = {}
        all_docs = []

        for sub_q in sub_questions:
            query_embedding = self.embedding.embed(sub_q)

            results = []
            for doc in self.documents:
                doc_embedding = self.doc_embeddings[doc.id]
                similarity = self.embedding.similarity(query_embedding, doc_embedding)
                results.append((doc, similarity))

            results.sort(key=lambda x: x[1], reverse=True)
            top_results = results[:top_k_per_question]

            sub_results[sub_q] = top_results
            all_docs.extend([doc for doc, _ in top_results])

        # Step 3: Deduplicate
        seen_ids = set()
        unique_docs = []
        for doc in all_docs:
            if doc.id not in seen_ids:
                seen_ids.add(doc.id)
                unique_docs.append(doc)

        return sub_questions, sub_results, unique_docs


def create_sample_documents() -> List[Document]:
    """Create sample knowledge base about concurrency"""
    return [
        Document(
            id="doc1",
            title="Asyncio Fundamentals",
            content="Asyncio is Python's built-in library for asynchronous programming. "
                   "It uses an event loop to handle concurrent operations without threads. "
                   "Ideal for IO-bound tasks like network requests."
        ),
        Document(
            id="doc2",
            title="Threading in Python",
            content="Threading allows concurrent execution using OS threads. "
                   "Python threads are limited by the GIL for CPU-bound tasks. "
                   "Good for IO-bound operations that release the GIL."
        ),
        Document(
            id="doc3",
            title="Asyncio Performance",
            content="Asyncio performance excels with many concurrent IO operations. "
                   "Lower memory overhead than threads. Event loop scheduling is very efficient. "
                   "Can handle thousands of concurrent connections."
        ),
        Document(
            id="doc4",
            title="Threading Performance",
            content="Threading performance depends on task type. CPU-bound tasks limited by GIL. "
                   "IO-bound tasks perform well. Each thread has memory overhead. "
                   "OS handles thread scheduling."
        ),
        Document(
            id="doc5",
            title="Concurrency Comparison",
            content="Asyncio vs threading: asyncio better for IO-heavy workloads. "
                   "Threading simpler for blocking operations. Asyncio requires async/await syntax. "
                   "Threading uses familiar synchronous code."
        ),
        Document(
            id="doc6",
            title="Event Loop Mechanics",
            content="The event loop is central to asyncio. It schedules and runs coroutines. "
                   "Non-blocking IO operations yield control back to loop. "
                   "Single-threaded but highly concurrent."
        ),
        Document(
            id="doc7",
            title="GIL and Threading",
            content="The Global Interpreter Lock (GIL) affects threading. "
                   "Only one thread executes Python bytecode at a time. "
                   "Limits CPU-bound threading performance. IO operations release GIL."
        ),
    ]


def visualize_results(query: str, single_results: List[Tuple[Document, float]],
                     sub_questions: List[str], sub_results: dict,
                     combined_docs: List[Document]):
    """Display comparison between single and decomposed retrieval"""

    console.print()
    console.print("[bold cyan]>>> COMPLEX QUERY[/bold cyan]")
    console.print(Panel(query, border_style="cyan", padding=(0, 2)))

    # Single query results
    console.print()
    console.print("[bold red]>>> SINGLE QUERY RETRIEVAL (Baseline)[/bold red]")
    table_single = Table(border_style="red", show_header=True, header_style="bold red")
    table_single.add_column("Rank", width=6)
    table_single.add_column("Document", width=35)
    table_single.add_column("Score", width=10)

    for i, (doc, score) in enumerate(single_results, 1):
        table_single.add_row(str(i), doc.title, f"{score:.4f}")

    console.print(table_single)

    # Decomposition
    console.print()
    console.print("[bold yellow]>>> QUERY DECOMPOSITION[/bold yellow]")
    console.print(f"[dim]Broke query into {len(sub_questions)} focused sub-questions:[/dim]")
    console.print()

    tree = Tree("[bold]Sub-Questions", style="yellow")
    for i, sub_q in enumerate(sub_questions, 1):
        tree.add(f"[cyan]{i}. {sub_q}[/cyan]")

    console.print(tree)

    # Results for each sub-question
    console.print()
    console.print("[bold green]>>> RETRIEVAL FOR EACH SUB-QUESTION[/bold green]")

    for i, (sub_q, results) in enumerate(sub_results.items(), 1):
        console.print()
        console.print(f"[bold white]Sub-Question {i}:[/bold white] [cyan]{sub_q}[/cyan]")

        table = Table(border_style="green", show_header=False, box=None)
        table.add_column("", width=3)
        table.add_column("Document", width=35)
        table.add_column("Score", width=10)

        for j, (doc, score) in enumerate(results, 1):
            table.add_row(f"{j}.", doc.title, f"{score:.4f}")

        console.print(table)

    # Combined results
    console.print()
    console.print("[bold green]>>> COMBINED RESULTS (Deduplicated)[/bold green]")
    console.print(f"[dim]Total unique documents: {len(combined_docs)}[/dim]")
    console.print()

    for i, doc in enumerate(combined_docs, 1):
        console.print(f"  [green]{i}. {doc.title}[/green]")

    # Key insight
    console.print()
    console.print("[bold yellow]>>> KEY INSIGHT[/bold yellow]")
    console.print(Panel(
        "[bold]Query decomposition provides comprehensive coverage[/bold]\n"
        "by retrieving focused results for each aspect of a complex question.",
        border_style="yellow",
        padding=(1, 2)
    ))


def main():
    """Run query decomposition demo"""

    # Header
    console.print()
    console.print("=" * 65, style="bold blue")
    console.print("  QUERY DECOMPOSITION", style="bold blue")
    console.print("=" * 65, style="bold blue")
    console.print()

    # Create knowledge base
    documents = create_sample_documents()
    retriever = QueryDecompositionRetriever(documents)

    # Complex query
    query = "Compare asyncio vs threading in terms of performance"

    console.print("[cyan]Processing complex query...[/cyan]")

    # Single query retrieval (baseline)
    single_results = retriever.retrieve_single(query, top_k=3)

    # Decomposed retrieval
    sub_questions, sub_results, combined_docs = retriever.retrieve_decomposed(
        query, top_k_per_question=2
    )

    console.print("[green]SUCCESS: Decomposed and retrieved results[/green]")

    # Display comparison
    visualize_results(query, single_results, sub_questions, sub_results, combined_docs)

    console.print()
    console.print("[green]Demo complete![/green]")
    console.print()
    console.print("[dim]Try other complex queries:[/dim]")
    console.print("[dim]  - 'What are the benefits and drawbacks of RAG?'[/dim]")
    console.print("[dim]  - 'How do I set up and use feature X?'[/dim]")


if __name__ == "__main__":
    main()
