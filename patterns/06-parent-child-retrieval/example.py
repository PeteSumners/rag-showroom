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


def create_rainbow_text(text: str) -> Text:
    """Create rainbow gradient text"""
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    rainbow = Text()
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        rainbow.append(char, style=f"bold {color}")
    return rainbow


def show_header():
    """Display colorful header"""
    console.print()

    # Rainbow title
    title = create_rainbow_text("=" * 65)
    console.print(title)

    header_text = Text("  PARENT-CHILD RETRIEVAL", style="bold white on blue")
    console.print(header_text)

    subtitle = Text("  Hierarchical Chunking for Better Context", style="italic cyan")
    console.print(subtitle)

    console.print(create_rainbow_text("=" * 65))
    console.print()


def show_concept():
    """Explain the concept with visual flair"""
    concept_panel = Panel(
        "[bold yellow]THE IDEA:[/bold yellow]\n\n"
        "[green]Small chunks[/green] = Good for precise retrieval\n"
        "[blue]Large chunks[/blue] = Good for context\n\n"
        "[bold magenta]SOLUTION:[/bold magenta] Store both!\n"
        "  [cyan]1.[/cyan] Search using [green]small child chunks[/green] (precise)\n"
        "  [cyan]2.[/cyan] Return [blue]large parent docs[/blue] (context)\n"
        "  [cyan]3.[/cyan] Get [bold yellow]best of both worlds![/bold yellow]",
        title="[bold magenta]>>> Concept <<<[/bold magenta]",
        border_style="bright_magenta",
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
        "[bold blue on white] Parent Document: doc_001 [/bold blue on white]",
        guide_style="bright_blue"
    )

    # Add child chunks with different colors
    child1 = tree.add("[bold green][*] Child Chunk 1: Overview[/bold green]")
    child1.add("[dim]'Python\\'s asyncio module provides...'[/dim]")
    child1.add("[yellow]Embedding: [0.23, 0.45, 0.78, ...][/yellow]")

    child2 = tree.add("[bold cyan][*] Child Chunk 2: Event Loop[/bold cyan]")
    child2.add("[dim]'The asyncio event loop is the core...'[/dim]")
    child2.add("[yellow]Embedding: [0.67, 0.12, 0.91, ...][/yellow]")

    child3 = tree.add("[bold magenta][*] Child Chunk 3: Performance[/bold magenta]")
    child3.add("[dim]'Performance characteristics: asyncio excels...'[/dim]")
    child3.add("[yellow]Embedding: [0.34, 0.89, 0.56, ...][/yellow]")

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
        title="[bold magenta]Search Results[/bold magenta]",
        box=box.DOUBLE_EDGE,
        header_style="bold white on blue",
        border_style="bright_cyan"
    )

    table.add_column("Step", style="cyan", justify="center")
    table.add_column("What Matched", style="yellow")
    table.add_column("What Was Returned", style="green")
    table.add_column("Score", style="magenta", justify="right")

    table.add_row(
        "[bold]1[/bold]",
        "[yellow]Child Chunk 3\n'Performance characteristics...'[/yellow]",
        "[green]ENTIRE Parent Doc\n(includes all context!)[/green]",
        "[bold magenta]0.94[/bold magenta]"
    )

    console.print(table)
    console.print()


def show_comparison():
    """Show before/after comparison"""
    console.print("[bold cyan]>>> IMPACT COMPARISON[/bold cyan]")
    console.print()

    comparison_table = Table(
        box=box.HEAVY_EDGE,
        border_style="yellow",
        show_header=True,
        header_style="bold white on dark_blue"
    )

    comparison_table.add_column("Approach", style="cyan")
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
        "[blue]Large chunks only[/blue]",
        "[yellow]***[/yellow]",
        "[green]*****[/green]",
        "[yellow][!] Imprecise matches[/yellow]"
    )

    comparison_table.add_row(
        "[bold magenta]Parent-Child (BEST!)[/bold magenta]",
        "[green]*****[/green]",
        "[green]*****[/green]",
        "[bold green][OK] Perfect![/bold green]"
    )

    console.print(comparison_table)
    console.print()


def show_key_insight():
    """Show key insight with maximum visual impact"""
    insight_text = Text()
    insight_text.append("*** ", style="bold yellow")
    insight_text.append("KEY INSIGHT", style="bold white on magenta")
    insight_text.append(" ***", style="bold yellow")

    insight_panel = Panel(
        "[bold cyan]Search with precision[/bold cyan] (child chunks)\n"
        "[bold yellow]+[/bold yellow]\n"
        "[bold green]Return with context[/bold green] (parent docs)\n"
        "[bold magenta]=[/bold magenta]\n"
        "[bold white on blue]  BEST OF BOTH WORLDS!  [/bold white on blue]\n\n"
        "[dim]Result: +35% context completeness, no precision loss![/dim]",
        title=insight_text,
        border_style="bold magenta",
        box=box.DOUBLE
    )
    console.print(insight_panel)
    console.print()


def show_footer():
    """Show colorful footer"""
    footer = create_rainbow_text("=" * 65)
    console.print(footer)

    footer_text = Text()
    footer_text.append("  *** Pattern Complete! *** ", style="bold green")
    footer_text.append("Check the docs for production implementation ", style="italic cyan")
    console.print(footer_text)

    console.print(create_rainbow_text("=" * 65))
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
