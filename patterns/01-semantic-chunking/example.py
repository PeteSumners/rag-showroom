#!/usr/bin/env python3
"""
Semantic Chunking Example

Demonstrates splitting documents at semantic boundaries instead of arbitrary
character limits. Uses simple keyword overlap as a proxy for semantic similarity.
"""

from typing import List
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@dataclass
class Chunk:
    """A semantic chunk of text"""
    id: int
    text: str
    sentence_count: int
    char_count: int


class SemanticChunker:
    """
    Chunks documents at semantic boundaries.

    Key insight: Breaking documents at topic shifts preserves context
    better than arbitrary character limits.
    """

    def __init__(self, similarity_threshold: float = 0.3):
        """
        Args:
            similarity_threshold: Similarity threshold for creating new chunks.
                Lower values = more granular chunks
                Higher values = fewer, larger chunks
        """
        self.similarity_threshold = similarity_threshold

    def chunk_document(self, text: str) -> List[Chunk]:
        """
        Split document into semantic chunks.

        Engineering decision: We analyze sentence-by-sentence rather than
        paragraph-by-paragraph because topics can shift mid-paragraph in
        technical content.
        """
        sentences = self._split_sentences(text)

        if not sentences:
            return []

        # Start first chunk
        chunks = []
        current_sentences = [sentences[0]]
        chunk_id = 0

        # Process remaining sentences
        for i in range(1, len(sentences)):
            similarity = self._calculate_similarity(
                current_sentences[-1],
                sentences[i]
            )

            if similarity >= self.similarity_threshold:
                # Similar enough - add to current chunk
                current_sentences.append(sentences[i])
            else:
                # Topic shift detected - finalize current chunk and start new one
                chunk_text = ' '.join(current_sentences)
                chunks.append(Chunk(
                    id=chunk_id,
                    text=chunk_text,
                    sentence_count=len(current_sentences),
                    char_count=len(chunk_text)
                ))

                # Start new chunk
                current_sentences = [sentences[i]]
                chunk_id += 1

        # Add final chunk
        if current_sentences:
            chunk_text = ' '.join(current_sentences)
            chunks.append(Chunk(
                id=chunk_id,
                text=chunk_text,
                sentence_count=len(current_sentences),
                char_count=len(chunk_text)
            ))

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.

        Note: This is a simplified implementation. Production systems should
        use proper sentence tokenizers like spaCy or NLTK.
        """
        # Clean up whitespace first
        text = ' '.join(text.split())

        # Basic sentence splitting
        text = text.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|')
        sentences = [s.strip() for s in text.split('|') if s.strip()]
        return sentences

    def _calculate_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate semantic similarity between sentences.

        Engineering decision: Using Jaccard similarity (keyword overlap) as a
        simple proxy for semantic similarity. Production systems should use
        proper embeddings (sentence-transformers, OpenAI, etc.) with cosine
        similarity.

        Why this works: Sentences about the same topic tend to share vocabulary.
        Example:
            "RAG combines retrieval and generation." vs
            "RAG systems use vector search." -> High overlap
            "RAG combines retrieval and generation." vs
            "Python is a programming language." -> Low overlap
        """
        words1 = set(sent1.lower().split())
        words2 = set(sent2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        # Jaccard similarity = |intersection| / |union|
        return len(intersection) / len(union)


def visualize_results(document: str, chunks: List[Chunk]):
    """Display chunking results with colored ASCII output"""

    # Original document preview
    console.print()
    console.print("[bold cyan]>>> INPUT DOCUMENT[/bold cyan]")
    console.print(Panel(
        document[:200] + "..." if len(document) > 200 else document,
        border_style="cyan",
        padding=(1, 2)
    ))

    # Statistics
    console.print()
    console.print("[bold yellow]>>> CHUNKING STATISTICS[/bold yellow]")
    stats_table = Table(border_style="yellow", show_header=True, header_style="bold yellow")
    stats_table.add_column("Metric", style="cyan", width=25)
    stats_table.add_column("Value", style="green bold", width=15)

    avg_sentences = sum(c.sentence_count for c in chunks) / len(chunks)
    avg_chars = sum(c.char_count for c in chunks) / len(chunks)

    stats_table.add_row("Total Chunks", str(len(chunks)))
    stats_table.add_row("Avg Sentences/Chunk", f"{avg_sentences:.1f}")
    stats_table.add_row("Avg Characters/Chunk", f"{avg_chars:.0f}")

    console.print(stats_table)

    # Display each chunk
    console.print()
    console.print("[bold green]>>> SEMANTIC CHUNKS[/bold green]")
    console.print()

    for chunk in chunks:
        preview = chunk.text[:150] + "..." if len(chunk.text) > 150 else chunk.text

        console.print(f"[bold white]Chunk {chunk.id}[/bold white] [dim]| {chunk.sentence_count} sentences | {chunk.char_count} chars[/dim]")
        console.print(Panel(
            preview,
            border_style="green",
            padding=(0, 2)
        ))

    # Key insight
    console.print()
    console.print("[bold yellow]>>> KEY INSIGHT[/bold yellow]")
    console.print(Panel(
        "[bold]Semantic chunking preserves context by breaking at topic boundaries,[/bold]\n"
        "leading to better retrieval relevance vs arbitrary character limits.",
        border_style="yellow",
        padding=(1, 2)
    ))


def main():
    """Run semantic chunking demo"""

    # Sample document about RAG systems (3 distinct topics)
    sample_document = """
    Retrieval-Augmented Generation (RAG) combines retrieval and generation for better LLM outputs.
    The system first retrieves relevant documents from a knowledge base using vector search.
    Vector embeddings represent semantic meaning in high-dimensional space.
    Cosine similarity measures how closely two embeddings match in this space.

    Chunking strategies significantly impact retrieval quality.
    Fixed-size chunking splits documents at arbitrary character counts, often breaking mid-sentence.
    This can fragment important context and reduce retrieval accuracy.
    Semantic chunking uses natural language boundaries like sentences or topics.

    The embedding model choice affects system performance.
    OpenAI's text-embedding-ada-002 provides good general-purpose embeddings.
    Domain-specific models can improve accuracy for specialized content.
    Embedding dimensions typically range from 384 to 1536.
    Higher dimensions capture more nuance but increase compute and storage costs.
    """

    # Header
    console.print()
    console.print("=" * 65, style="bold blue")
    console.print("  SEMANTIC CHUNKING EXAMPLE", style="bold blue")
    console.print("=" * 65, style="bold blue")
    console.print()

    # Create chunker and process
    # Lower threshold = more sensitive to topic changes = more chunks
    chunker = SemanticChunker(similarity_threshold=0.15)

    console.print("[cyan]Processing document...[/cyan]")
    chunks = chunker.chunk_document(sample_document)
    console.print(f"[green]SUCCESS: Created {len(chunks)} semantic chunks[/green]")
    console.print()

    # Display results
    visualize_results(sample_document, chunks)

    console.print()
    console.print("[green]Demo complete![/green]")
    console.print()
    console.print("[dim]Try running with different threshold values:[/dim]")
    console.print("[dim]  chunker = SemanticChunker(similarity_threshold=0.2)  # More chunks[/dim]")
    console.print("[dim]  chunker = SemanticChunker(similarity_threshold=0.5)  # Fewer chunks[/dim]")


if __name__ == "__main__":
    main()
