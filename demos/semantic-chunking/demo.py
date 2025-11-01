#!/usr/bin/env python3
"""
Semantic Chunking RAG Demo

Demonstrates intelligent document chunking at semantic boundaries rather than
arbitrary character counts. Uses sentence embeddings to detect topic shifts
and create semantically coherent chunks.
"""

import os
from typing import List, Tuple
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# For simplicity, using basic sentence splitting and mock embeddings
# In production, use proper embedding models (OpenAI, Anthropic, etc.)

console = Console()


@dataclass
class Chunk:
    """Represents a semantic chunk of text"""
    id: int
    text: str
    sentences: List[str]
    topic: str


class SemanticChunker:
    """
    Chunks documents at semantic boundaries.

    Key insight: Breaking documents at topic shifts preserves context
    better than arbitrary character limits.
    """

    def __init__(self, similarity_threshold: float = 0.7):
        """
        Args:
            similarity_threshold: Cosine similarity threshold for creating new chunks.
                                Lower values = more chunks, higher = fewer chunks.
        """
        self.similarity_threshold = similarity_threshold

    def chunk_document(self, text: str) -> List[Chunk]:
        """
        Chunk document at semantic boundaries.

        Engineering decision: We use sentence-level analysis rather than
        paragraph-level because topics can shift mid-paragraph in technical docs.
        """
        # Split into sentences (simplified - production should use spacy/nltk)
        sentences = self._split_sentences(text)

        # Group sentences into semantic chunks
        chunks = []
        current_chunk_sentences = [sentences[0]]
        chunk_id = 0

        for i in range(1, len(sentences)):
            # Calculate semantic similarity between sentences
            # In production: use actual embeddings (OpenAI, Anthropic, etc.)
            similarity = self._calculate_similarity(
                current_chunk_sentences[-1],
                sentences[i]
            )

            if similarity >= self.similarity_threshold:
                # Similar enough - add to current chunk
                current_chunk_sentences.append(sentences[i])
            else:
                # Topic shift detected - create new chunk
                chunk_text = ' '.join(current_chunk_sentences)
                chunks.append(Chunk(
                    id=chunk_id,
                    text=chunk_text,
                    sentences=current_chunk_sentences.copy(),
                    topic=self._extract_topic(current_chunk_sentences)
                ))

                # Start new chunk
                current_chunk_sentences = [sentences[i]]
                chunk_id += 1

        # Add final chunk
        if current_chunk_sentences:
            chunk_text = ' '.join(current_chunk_sentences)
            chunks.append(Chunk(
                id=chunk_id,
                text=chunk_text,
                sentences=current_chunk_sentences,
                topic=self._extract_topic(current_chunk_sentences)
            ))

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences (simplified)"""
        # Production: use proper sentence tokenizer
        sentences = text.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|').split('|')
        return [s.strip() for s in sentences if s.strip()]

    def _calculate_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate semantic similarity between sentences.

        Engineering decision: In this demo, we use keyword overlap as a proxy.
        Production systems should use proper embeddings (cosine similarity of
        sentence-transformers, OpenAI embeddings, etc.)
        """
        words1 = set(sent1.lower().split())
        words2 = set(sent2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        # Jaccard similarity as a simple proxy for semantic similarity
        return len(intersection) / len(union)

    def _extract_topic(self, sentences: List[str]) -> str:
        """Extract topic keywords from sentences (simplified)"""
        # Production: use proper topic modeling or LLM extraction
        all_words = ' '.join(sentences).lower().split()
        # Get most common non-stopwords (simplified)
        word_counts = {}
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were'}

        for word in all_words:
            word = word.strip('.,!?')
            if word not in stopwords and len(word) > 3:
                word_counts[word] = word_counts.get(word, 0) + 1

        if not word_counts:
            return "general"

        # Return top keyword
        return max(word_counts.items(), key=lambda x: x[1])[0]


def visualize_chunking(document: str, chunks: List[Chunk]):
    """Display the chunking results with colored ASCII art"""

    # Display original document
    console.print(Panel(
        document[:200] + "..." if len(document) > 200 else document,
        title="📥 Original Document",
        border_style="cyan"
    ))

    console.print()

    # Display chunking statistics
    stats_table = Table(title="📊 Chunking Statistics", border_style="yellow")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="green")

    stats_table.add_row("Total Chunks", str(len(chunks)))
    stats_table.add_row("Avg Sentences/Chunk", f"{sum(len(c.sentences) for c in chunks) / len(chunks):.1f}")
    stats_table.add_row("Avg Chars/Chunk", f"{sum(len(c.text) for c in chunks) / len(chunks):.0f}")

    console.print(stats_table)
    console.print()

    # Display each chunk
    for chunk in chunks:
        chunk_info = f"Topic: {chunk.topic.upper()} | Sentences: {len(chunk.sentences)} | Chars: {len(chunk.text)}"

        console.print(Panel(
            Text(chunk.text[:150] + "..." if len(chunk.text) > 150 else chunk.text),
            title=f"🔎 Chunk {chunk.id}: {chunk_info}",
            border_style="green"
        ))

    # Display key insight
    console.print()
    console.print(Panel(
        "✨ Semantic chunking preserves context by breaking at topic boundaries,\n"
        "leading to better retrieval relevance compared to arbitrary character limits.",
        title="💡 Key Insight",
        border_style="yellow"
    ))


def main():
    """Run the semantic chunking demo"""

    # Sample technical document about RAG systems
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

    # Display header
    console.print()
    console.print("╔═══════════════════════════════════════════════════════════════╗", style="bold blue")
    console.print("║  🔍 SEMANTIC CHUNKING RAG                                     ║", style="bold blue")
    console.print("╚═══════════════════════════════════════════════════════════════╝", style="bold blue")
    console.print()

    # Create chunker and process document
    chunker = SemanticChunker(similarity_threshold=0.3)

    console.print("[cyan]Processing document...[/cyan]")
    chunks = chunker.chunk_document(sample_document)

    console.print(f"[green]✓ Created {len(chunks)} semantic chunks[/green]")
    console.print()

    # Visualize results
    visualize_chunking(sample_document, chunks)

    console.print()
    console.print("[green]✅ Demo complete![/green]")


if __name__ == "__main__":
    main()
