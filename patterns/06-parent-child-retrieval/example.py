"""
Parent-Child Retrieval Pattern Demo

This demo shows how to use hierarchical chunking with colorful, engaging output!
"""

import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.tree import Tree
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich import box

console = Console()

# Mock document and chunks
PARENT_DOC = """
Python's asyncio module provides infrastructure for writing single-threaded concurrent
code using coroutines, multiplexing I/O access over sockets and other resources, running
network clients and servers, and other related primitives.

The asyncio event loop is the core of every asyncio application. Event loops run
asynchronous tasks and callbacks, perform network IO operations, and run subprocesses.

Performance characteristics: asyncio excels at I/O-bound operations where you're waiting
for external resources. For CPU-bound tasks, threading or multiprocessing is better.
"""

CHILD_CHUNKS = [
    {
        "id": "chunk_1",
        "content": "Python's asyncio module provides infrastructure for writing single-threaded concurrent code...",
        "parent_id": "doc_001",
        "topic": "Overview"
    },
    {
        "id": "chunk_2",
        "content": "The asyncio event loop is the core of every asyncio application...",
        "parent_id": "doc_001",
        "topic": "Event Loop"
    },
    {
        "id": "chunk_3",
        "content": "Performance characteristics: asyncio excels at I/O-bound operations...",
        "parent_id": "doc_001",
        "topic": "Performance"
    }
]




def show_header():
    """Professional header with coherent colors!"""
    console.print()
    console.print("=" * 70, style="bold cyan")

    title = Text()
    title.append("  PARENT-CHILD RETRIEVAL ", style="bold white on blue")
    title.append("- Hierarchical Chunking  ", style="bold white on cyan")
    console.print(title)

    console.print("=" * 70, style="bold blue")
    console.print()


def show_concept():
    """Explain the concept with coherent colors!"""
    concept_panel = Panel(
        "[bold red]THE PROBLEM:[/bold red]\n"
        "[red]Small chunks[/red] = Precise but lack context\n"
        "[red]Large chunks[/red] = Context but imprecise\n\n"
        "[bold green]THE SOLUTION:[/bold green]\n"
        "[cyan]Parent-Child retrieval[/cyan] uses both = [bold green]Precision + Context![/bold green]\n\n"
        "[bold cyan]HOW IT WORKS:[/bold cyan]\n"
        "  [cyan]1.[/cyan] Store small child chunks + large parent docs\n"
        "  [cyan]2.[/cyan] Search using [green]child chunks[/green] (precise)\n"
        "  [cyan]3.[/cyan] Return [blue]parent documents[/blue] (full context)\n"
        "  [cyan]4.[/cyan] Profit! [bold green](+35% context completeness!)[/bold green]",
        title="[bold white on blue] CONCEPT [/bold white on blue]",
        border_style="blue",
        box=box.DOUBLE
    )
    console.print(concept_panel)
    console.print()


def show_processing_with_progress():
    """Show processing with animated progress bars"""
    console.print("[bold cyan]>>> PROCESSING DOCUMENT[/bold cyan]")
    console.print()

    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green", finished_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:

        task1 = progress.add_task("[yellow]Creating parent document...", total=100)
        for i in range(100):
            time.sleep(0.01)
            progress.update(task1, advance=1)

        task2 = progress.add_task("[cyan]Splitting into child chunks...", total=100)
        for i in range(100):
            time.sleep(0.01)
            progress.update(task2, advance=1)

        task3 = progress.add_task("[magenta]Indexing chunks...", total=100)
        for i in range(100):
            time.sleep(0.01)
            progress.update(task3, advance=1)

    console.print()
    console.print("[bold green][OK] SUCCESS:[/bold green] Created 1 parent + 3 child chunks!", style="bold")
    console.print()


def show_hierarchy_tree():
    """Display parent-child hierarchy as a tree"""
    console.print("[bold cyan]>>> DOCUMENT HIERARCHY[/bold cyan]")
    console.print()

    tree = Tree(
        "[bold white on blue] Parent Document: doc_001 [/bold white on blue]",
        guide_style="cyan"
    )

    # Add child chunks with alternating cyan/green for coherence
    child1 = tree.add("[bold cyan][*] Child Chunk 1: Overview[/bold cyan]")
    child1.add("[dim]'Python's asyncio module provides...'[/dim]")
    child1.add("[white]Embedding: [0.23, 0.45, 0.78, ...][/white]")

    child2 = tree.add("[bold green][*] Child Chunk 2: Event Loop[/bold green]")
    child2.add("[dim]'The asyncio event loop is the core...'[/dim]")
    child2.add("[white]Embedding: [0.67, 0.12, 0.91, ...][/white]")

    child3 = tree.add("[bold cyan][*] Child Chunk 3: Performance[/bold cyan]")
    child3.add("[dim]'Performance characteristics: asyncio excels...'[/dim]")
    child3.add("[white]Embedding: [0.34, 0.89, 0.56, ...][/white]")

    console.print(tree)
    console.print()


def show_retrieval():
    """Show retrieval process with colors"""
    console.print("[bold cyan]>>> USER QUERY[/bold cyan]")
    query_panel = Panel(
        "[bold white]What are the performance characteristics of asyncio?[/bold white]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(query_panel)
    console.print()

    # Search animation
    console.print("[bold yellow]>>> SEARCHING...[/bold yellow]")
    with console.status("[bold green]Embedding query...", spinner="dots"):
        time.sleep(0.5)
    console.print("[green][OK][/green] Query embedded")

    with console.status("[bold green]Searching child chunks...", spinner="dots"):
        time.sleep(0.5)
    console.print("[green][OK][/green] Found matching child chunk")

    with console.status("[bold green]Retrieving parent document...", spinner="dots"):
        time.sleep(0.5)
    console.print("[green][OK][/green] Retrieved parent context")
    console.print()


def show_results():
    """Show results with colorful table"""
    console.print("[bold cyan]>>> RETRIEVAL RESULTS[/bold cyan]")
    console.print()

    # Create results table
    table = Table(
        title="[bold blue]Search Results[/bold blue]",
        box=box.DOUBLE_EDGE,
        header_style="bold white on dark_blue",
        border_style="cyan"
    )

    table.add_column("Step", style="cyan bold", justify="center")
    table.add_column("What Matched", style="white")
    table.add_column("What Was Returned", style="white")
    table.add_column("Score", style="green bold", justify="right")

    table.add_row(
        "[bold]1[/bold]",
        "[cyan]Child Chunk 3\n'Performance characteristics...'[/cyan]",
        "[bold green]ENTIRE Parent Doc\n(includes all context!)[/bold green]",
        "[bold green]0.94[/bold green]"
    )

    console.print(table)
    console.print()


def show_comparison():
    """Show before/after comparison"""
    console.print("[bold cyan]>>> IMPACT COMPARISON[/bold cyan]")
    console.print()

    comparison_table = Table(
        box=box.ROUNDED,
        border_style="cyan",
        show_header=True,
        header_style="bold white on dark_blue"
    )

    comparison_table.add_column("Approach", style="white")
    comparison_table.add_column("Precision", justify="center")
    comparison_table.add_column("Context", justify="center")
    comparison_table.add_column("Result", style="bold")

    comparison_table.add_row(
        "[yellow]Small chunks only[/yellow]",
        "[green]*****[/green]",
        "[red]**[/red]",
        "[red][X] Missing context[/red]"
    )

    comparison_table.add_row(
        "[yellow]Large chunks only[/yellow]",
        "[yellow]***[/yellow]",
        "[green]*****[/green]",
        "[yellow][!] Imprecise matches[/yellow]"
    )

    comparison_table.add_row(
        "[bold green]Parent-Child (BEST!)[/bold green]",
        "[green]*****[/green]",
        "[green]*****[/green]",
        "[bold green][OK] Perfect![/bold green]"
    )

    console.print(comparison_table)
    console.print()


def show_key_insight():
    """Show key insight with coherent colors!"""
    insight_text = Text()
    insight_text.append("*** ", style="bold cyan")
    insight_text.append("KEY INSIGHT", style="bold white on cyan")
    insight_text.append(" ***", style="bold cyan")

    insight_panel = Panel(
        "[bold cyan]Search with precision[/bold cyan] (child chunks)\n"
        "[bold white]+[/bold white]\n"
        "[bold green]Return with context[/bold green] (parent docs)\n"
        "[bold white]=[/bold white]\n"
        "[bold white on blue]  BEST OF BOTH WORLDS!  [/bold white on blue]\n\n"
        "[bold white]Result:[/bold white] [bold green]+35% context completeness, no precision loss![/bold green]\n\n"
        "[dim]Production tip: Store parent docs alongside child embeddings[/dim]",
        title=insight_text,
        border_style="cyan",
        box=box.DOUBLE
    )
    console.print(insight_panel)
    console.print()


def show_footer():
    """Clean professional footer!"""
    console.print()
    console.print("=" * 70, style="bold blue")

    footer_text = Text()
    footer_text.append("  Demo Complete! ", style="bold green")
    footer_text.append("Hierarchical chunking delivers precision + context!", style="cyan")
    console.print(footer_text)

    console.print("=" * 70, style="bold cyan")
    console.print()


def main():
    """Run the colorful demo!"""
    show_header()
    time.sleep(0.5)

    show_concept()
    time.sleep(0.5)

    show_processing_with_progress()
    time.sleep(0.5)

    show_hierarchy_tree()
    time.sleep(0.5)

    show_retrieval()
    time.sleep(0.5)

    show_results()
    time.sleep(0.5)

    show_comparison()
    time.sleep(0.5)

    show_key_insight()
    time.sleep(0.5)

    show_footer()


if __name__ == "__main__":
    main()
