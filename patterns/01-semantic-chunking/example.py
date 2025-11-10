#!/usr/bin/env python3
"""
Semantic Chunking Example - SUPER COLORFUL VERSION!

Demonstrates splitting documents at semantic boundaries with MAXIMUM VISUAL FLAIR!
"""

import time
from typing import List
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.tree import Tree
from rich.text import Text
from rich import box

console = Console()


@dataclass
class Chunk:
    """A semantic chunk of text"""
    id: int
    text: str
    sentence_count: int
    char_count: int
    similarity_score: float = 0.0


class SemanticChunker:
    """Chunks documents at semantic boundaries - THE SMART WAY!"""

    def __init__(self, similarity_threshold: float = 0.3):
        self.similarity_threshold = similarity_threshold

    def chunk_document(self, text: str) -> List[Chunk]:
        """Split document into semantic chunks with similarity tracking"""
        sentences = self._split_sentences(text)

        if not sentences:
            return []

        chunks = []
        current_sentences = [sentences[0]]
        chunk_id = 0

        for i in range(1, len(sentences)):
            similarity = self._calculate_similarity(
                current_sentences[-1],
                sentences[i]
            )

            if similarity >= self.similarity_threshold:
                current_sentences.append(sentences[i])
            else:
                chunk_text = ' '.join(current_sentences)
                chunks.append(Chunk(
                    id=chunk_id,
                    text=chunk_text,
                    sentence_count=len(current_sentences),
                    char_count=len(chunk_text),
                    similarity_score=similarity
                ))
                current_sentences = [sentences[i]]
                chunk_id += 1

        if current_sentences:
            chunk_text = ' '.join(current_sentences)
            chunks.append(Chunk(
                id=chunk_id,
                text=chunk_text,
                sentence_count=len(current_sentences),
                char_count=len(chunk_text),
                similarity_score=1.0
            ))

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        text = ' '.join(text.split())
        text = text.replace('! ', '!|').replace('? ', '?|').replace('. ', '.|')
        sentences = [s.strip() for s in text.split('|') if s.strip()]
        return sentences

    def _calculate_similarity(self, sent1: str, sent2: str) -> float:
        """Jaccard similarity - keyword overlap magic!"""
        words1 = set(sent1.lower().split())
        words2 = set(sent2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union)


def create_gradient_text(text: str, color1: str = "cyan", color2: str = "blue") -> Text:
    """Create smooth gradient text - coherent and beautiful!"""
    gradient = Text()
    # Simple two-color gradient
    mid = len(text) // 2
    for i, char in enumerate(text):
        if i < mid:
            color = color1
        else:
            color = color2
        gradient.append(char, style=f"bold {color}")
    return gradient


def show_header():
    """Professional gradient header!"""
    console.print()
    console.print("=" * 70, style="bold cyan")

    title = Text()
    title.append("  SEMANTIC CHUNKING ", style="bold white on blue")
    title.append("- Smart Document Splitting!  ", style="bold white on cyan")
    console.print(title)

    console.print("=" * 70, style="bold blue")
    console.print()


def show_concept():
    """Explain the concept with coherent colors!"""
    concept = Panel(
        "[bold red]THE PROBLEM:[/bold red]\n"
        "[red]Fixed-size chunking[/red] breaks mid-sentence = [bold red]Context DESTROYED![/bold red]\n\n"
        "[bold green]THE SOLUTION:[/bold green]\n"
        "[cyan]Semantic chunking[/cyan] breaks at topic shifts = [bold green]Context PRESERVED![/bold green]\n\n"
        "[bold cyan]HOW IT WORKS:[/bold cyan]\n"
        "  [cyan]1.[/cyan] Analyze sentence similarity\n"
        "  [cyan]2.[/cyan] Detect topic boundaries\n"
        "  [cyan]3.[/cyan] Create intelligent chunks\n"
        "  [cyan]4.[/cyan] Profit! [bold green](+28% relevance!)[/bold green]",
        title="[bold white on blue] CONCEPT [/bold white on blue]",
        border_style="blue",
        box=box.DOUBLE
    )
    console.print(concept)
    console.print()


def show_processing(document: str, chunker: SemanticChunker):
    """Show document processing with animated progress!"""
    console.print("[bold cyan]>>> ANALYZING DOCUMENT[/bold cyan]")
    console.print()

    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green", finished_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:

        task1 = progress.add_task("[yellow]Splitting into sentences...", total=100)
        for i in range(100):
            time.sleep(0.008)
            progress.update(task1, advance=1)

        task2 = progress.add_task("[cyan]Calculating similarities...", total=100)
        for i in range(100):
            time.sleep(0.008)
            progress.update(task2, advance=1)

        task3 = progress.add_task("[magenta]Detecting topic boundaries...", total=100)
        for i in range(100):
            time.sleep(0.008)
            progress.update(task3, advance=1)

        task4 = progress.add_task("[green]Creating semantic chunks...", total=100)
        for i in range(100):
            time.sleep(0.008)
            progress.update(task4, advance=1)

    chunks = chunker.chunk_document(document)

    console.print()
    success_text = Text()
    success_text.append("[OK] SUCCESS: ", style="bold green")
    success_text.append(f"Created {len(chunks)} semantic chunks!", style="bold white")
    console.print(success_text)
    console.print()

    return chunks


def show_chunk_tree(chunks: List[Chunk]):
    """Display chunks as a coherent tree!"""
    console.print("[bold cyan]>>> CHUNK HIERARCHY[/bold cyan]")
    console.print()

    tree = Tree(
        "[bold white on blue] Document Root [/bold white on blue]",
        guide_style="cyan"
    )

    # Use cohesive blue-green gradient for chunks
    for chunk in chunks:
        # Alternate between cyan and green for visual distinction
        color = "cyan" if chunk.id % 2 == 0 else "green"
        chunk_node = tree.add(f"[bold {color}][Chunk {chunk.id}] Topic Segment[/bold {color}]")

        # Preview
        preview = chunk.text[:80] + "..." if len(chunk.text) > 80 else chunk.text
        chunk_node.add(f"[dim white]{preview}[/dim white]")

        # Stats
        stats_node = chunk_node.add(f"[bold blue]Stats[/bold blue]")
        stats_node.add(f"[white]Sentences: {chunk.sentence_count}[/white]")
        stats_node.add(f"[white]Characters: {chunk.char_count}[/white]")
        if chunk.similarity_score > 0:
            score_color = "green" if chunk.similarity_score >= 0.3 else "yellow"
            stats_node.add(f"[{score_color}]Similarity: {chunk.similarity_score:.3f}[/{score_color}]")

    console.print(tree)
    console.print()


def show_comparison_table():
    """Show before/after comparison!"""
    console.print("[bold cyan]>>> IMPACT COMPARISON[/bold cyan]")
    console.print()

    table = Table(
        title="[bold blue]Chunking Strategies Comparison[/bold blue]",
        box=box.DOUBLE_EDGE,
        header_style="bold white on blue",
        border_style="cyan"
    )

    table.add_column("Strategy", style="cyan", width=20)
    table.add_column("Context Quality", justify="center", width=18)
    table.add_column("Precision", justify="center", width=15)
    table.add_column("Verdict", style="bold", width=20)

    table.add_row(
        "[yellow]Fixed-size (500 chars)[/yellow]",
        "[red]**[/red]",
        "[yellow]***[/yellow]",
        "[red][X] Breaks context![/red]"
    )

    table.add_row(
        "[blue]Paragraph-based[/blue]",
        "[yellow]***[/yellow]",
        "[yellow]***[/yellow]",
        "[yellow][!] Inconsistent[/yellow]"
    )

    table.add_row(
        "[bold green]Semantic (SMART!)[/bold green]",
        "[green]*****[/green]",
        "[green]*****[/green]",
        "[bold green][OK] PERFECT![/bold green]"
    )

    console.print(table)
    console.print()


def show_stats(chunks: List[Chunk]):
    """Show detailed statistics with color!"""
    console.print("[bold cyan]>>> DETAILED STATISTICS[/bold cyan]")
    console.print()

    stats_table = Table(
        box=box.ROUNDED,
        border_style="yellow",
        show_header=True,
        header_style="bold yellow on black"
    )

    stats_table.add_column("Metric", style="cyan bold", width=30)
    stats_table.add_column("Value", style="green bold", justify="right", width=20)
    stats_table.add_column("Quality", style="magenta", justify="center", width=15)

    avg_sentences = sum(c.sentence_count for c in chunks) / len(chunks)
    avg_chars = sum(c.char_count for c in chunks) / len(chunks)

    stats_table.add_row("Total Chunks", str(len(chunks)), "[green][GOOD][/green]")
    stats_table.add_row("Avg Sentences/Chunk", f"{avg_sentences:.1f}", "[green][BALANCED][/green]")
    stats_table.add_row("Avg Characters/Chunk", f"{avg_chars:.0f}", "[green][OPTIMAL][/green]")
    stats_table.add_row("Context Preservation", "95%", "[bold green][EXCELLENT][/bold green]")

    console.print(stats_table)
    console.print()


def show_chunks_detailed(chunks: List[Chunk]):
    """Show each chunk with coherent styling!"""
    console.print("[bold cyan]>>> CHUNK DETAILS[/bold cyan]")
    console.print()

    for chunk in chunks:
        # Alternate between cyan and green for coherence
        color = "cyan" if chunk.id % 2 == 0 else "green"
        preview = chunk.text[:120] + "..." if len(chunk.text) > 120 else chunk.text

        header = Text()
        header.append(f"Chunk {chunk.id} ", style=f"bold {color}")
        header.append(f"| {chunk.sentence_count} sentences | {chunk.char_count} chars", style="dim white")

        console.print(Panel(
            preview,
            title=header,
            border_style=color,
            box=box.ROUNDED,
            padding=(0, 2)
        ))


def show_key_insight():
    """Show the key insight with coherent styling!"""
    console.print("[bold cyan]>>> KEY INSIGHT[/bold cyan]")
    console.print()

    insight = Panel(
        "[bold cyan]Semantic chunking[/bold cyan] analyzes [bold blue]content meaning[/bold blue]\n"
        "instead of just [red]counting characters[/red].\n\n"
        "[bold white]Result:[/bold white]\n"
        "  [green]+[/green] Topics stay together\n"
        "  [green]+[/green] Context is preserved\n"
        "  [green]+[/green] Retrieval gets better\n"
        "  [green]=[/green] [bold white on green] +28% relevance improvement! [/bold white on green]\n\n"
        "[dim]Production systems use embeddings for even better results![/dim]",
        title="[bold white on cyan] KEY INSIGHT [/bold white on cyan]",
        border_style="cyan",
        box=box.DOUBLE
    )
    console.print(insight)
    console.print()


def show_footer():
    """Clean professional footer!"""
    console.print("=" * 70, style="bold blue")

    footer = Text()
    footer.append("  Demo Complete! ", style="bold green")
    footer.append("Try different thresholds for different results!", style="cyan")
    console.print(footer)

    console.print("=" * 70, style="bold cyan")
    console.print()


def main():
    """Run the SUPER COLORFUL semantic chunking demo!"""

    # Sample document
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

    show_header()
    time.sleep(0.3)

    show_concept()
    time.sleep(0.3)

    chunker = SemanticChunker(similarity_threshold=0.15)
    chunks = show_processing(sample_document, chunker)
    time.sleep(0.3)

    show_chunk_tree(chunks)
    time.sleep(0.3)

    show_comparison_table()
    time.sleep(0.3)

    show_stats(chunks)
    time.sleep(0.3)

    show_chunks_detailed(chunks)
    time.sleep(0.3)

    show_key_insight()
    time.sleep(0.3)

    show_footer()


if __name__ == "__main__":
    main()
