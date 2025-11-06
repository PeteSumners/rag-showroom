#!/usr/bin/env python3
"""
HyDE (Hypothetical Document Embeddings) - ULTRA COLORFUL VERSION!

Watch as we generate fake answers to bridge the vocabulary gap! MAXIMUM VISUAL FLAIR!
"""

import time
from typing import List, Tuple
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
class SearchResult:
    """A search result with score"""
    doc_id: str
    content: str
    score: float


def create_rainbow_text(text: str) -> Text:
    """Rainbow gradient magic!"""
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    rainbow = Text()
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        rainbow.append(char, style=f"bold {color}")
    return rainbow


def show_header():
    """Epic animated header!"""
    console.print()
    console.print(create_rainbow_text("=" * 75))

    title = Text()
    title.append("  HyDE ", style="bold white on blue")
    title.append("- Hypothetical Document Embeddings ", style="bold white on magenta")
    title.append("MAGIC!  ", style="bold white on green")
    console.print(title)

    console.print(create_rainbow_text("=" * 75))
    console.print()


def show_problem():
    """Show the vocabulary gap problem!"""
    console.print("[bold red]>>> THE VOCABULARY GAP PROBLEM[/bold red]")
    console.print()

    problem = Panel(
        "[bold yellow]USERS ASK QUESTIONS:[/bold yellow]\n"
        "[cyan]\"How do I authenticate?\"[/cyan]\n"
        "[cyan]\"What is semantic chunking?\"[/cyan]\n\n"
        "[bold red]DOCS CONTAIN ANSWERS:[/bold red]\n"
        "[green]\"Authentication is performed by...\"[/green]\n"
        "[green]\"Semantic chunking splits documents...\"[/green]\n\n"
        "[bold white on red] LANGUAGE MISMATCH = POOR RETRIEVAL! [/bold white on red]\n\n"
        "[dim]Questions vs Statements = Different embeddings = Bad matches[/dim]",
        title="[bold red]*** PROBLEM ***[/bold red]",
        border_style="red",
        box=box.HEAVY
    )
    console.print(problem)
    console.print()


def show_solution():
    """Show the HyDE solution!"""
    console.print("[bold green]>>> THE HYDE SOLUTION[/bold green]")
    console.print()

    solution = Panel(
        "[bold cyan]STEP 1:[/bold cyan] Generate a [yellow]fake answer[/yellow] to the question\n"
        "[bold cyan]STEP 2:[/bold cyan] Embed the [yellow]hypothesis[/yellow] (not the question!)\n"
        "[bold cyan]STEP 3:[/bold cyan] Search using [green]hypothesis embedding[/green]\n"
        "[bold cyan]STEP 4:[/bold cyan] Find [green]actual docs[/green] that match!\n\n"
        "[bold white on blue] DOCUMENTS MATCH DOCUMENTS! [/bold white on blue]\n\n"
        "[bold green]Result:[/bold green] [magenta]+20-30% precision improvement![/magenta]\n"
        "[dim](Even if the fake answer is wrong, the vocabulary matches!)[/dim]",
        title="[bold green]*** SOLUTION ***[/bold green]",
        border_style="green",
        box=box.DOUBLE
    )
    console.print(solution)
    console.print()


def show_query(query: str):
    """Display user query dramatically!"""
    console.print("[bold cyan]>>> USER QUERY[/bold cyan]")
    console.print()

    query_panel = Panel(
        f"[bold white]{query}[/bold white]",
        title="[cyan]Question from User[/cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 4)
    )
    console.print(query_panel)
    console.print()


def generate_hypothesis_animated(query: str) -> str:
    """Generate hypothesis with animation!"""
    console.print("[bold yellow]>>> GENERATING HYPOTHESIS[/bold yellow]")
    console.print()

    with console.status("[bold yellow]LLM is thinking...", spinner="dots"):
        time.sleep(1)

    console.print("[green][OK][/green] Hypothesis generated!")
    console.print()

    hypothesis = (
        "Semantic chunking is a document preprocessing technique that splits "
        "text at meaningful topic boundaries rather than arbitrary character limits. "
        "It uses embeddings to identify where topics shift, preserving context and "
        "improving retrieval quality by 15-28% compared to fixed-size chunking."
    )

    # Show hypothesis generation process
    console.print("[bold magenta]>>> HYPOTHESIS (Fake Answer)[/bold magenta]")
    console.print()

    hyp_panel = Panel(
        f"[yellow]{hypothesis}[/yellow]\n\n"
        "[dim]Note: This is a MADE-UP answer! It might even be wrong!\n"
        "But it uses the same vocabulary as real documentation.[/dim]",
        title="[magenta]Generated Hypothesis[/magenta]",
        border_style="magenta",
        box=box.DOUBLE,
        padding=(1, 2)
    )
    console.print(hyp_panel)
    console.print()

    return hypothesis


def show_comparison_search(query: str, hypothesis: str):
    """Show naive vs HyDE search side by side!"""
    console.print("[bold cyan]>>> RETRIEVAL COMPARISON[/bold cyan]")
    console.print()

    # Naive results
    naive_results = [
        SearchResult("doc_5", "FAQ: Common questions about chunking strategies", 0.72),
        SearchResult("doc_12", "Chunking vs splitting: What's the difference?", 0.68),
        SearchResult("doc_8", "Guide to text preprocessing techniques", 0.65),
    ]

    # HyDE results
    hyde_results = [
        SearchResult("doc_1", "Semantic Chunking: Split documents at topic boundaries for better RAG", 0.89),
        SearchResult("doc_3", "How semantic chunking improves retrieval quality in production", 0.84),
        SearchResult("doc_7", "Implementation guide: semantic chunking algorithms explained", 0.81),
    ]

    # Create comparison table
    table = Table(
        title="[bold white]Search Results Showdown![/bold white]",
        box=box.HEAVY_EDGE,
        border_style="bright_cyan"
    )

    table.add_column("Rank", justify="center", style="cyan bold", width=6)
    table.add_column("Naive Search\n(Question Embedding)", style="yellow", width=35)
    table.add_column("Score", justify="center", style="yellow", width=7)
    table.add_column("HyDE Search\n(Hypothesis Embedding)", style="green", width=35)
    table.add_column("Score", justify="center", style="green bold", width=7)

    for i, (naive, hyde) in enumerate(zip(naive_results, hyde_results), 1):
        table.add_row(
            f"{i}",
            f"[yellow]{naive.content[:50]}...[/yellow]",
            f"[yellow]{naive.score:.2f}[/yellow]",
            f"[green]{hyde.content[:50]}...[/green]",
            f"[bold green]{hyde.score:.2f}[/bold green]"
        )

    console.print(table)
    console.print()

    # Highlight the difference
    highlight = Panel(
        "[bold red]Naive:[/bold red] Found [yellow]FAQ and meta pages[/yellow] (not the actual docs!)\n"
        "[bold green]HyDE:[/bold green] Found [green]ACTUAL DOCUMENTATION[/green] (exactly what we need!)\n\n"
        "[bold white]Score Improvement:[/bold white] [cyan]0.72[/cyan] -> [bold green]0.89[/bold green] "
        "[magenta](+24% better!)[/magenta]",
        title="[bold magenta]*** IMPACT ***[/bold magenta]",
        border_style="magenta",
        box=box.DOUBLE
    )
    console.print(highlight)
    console.print()


def show_workflow_tree():
    """Visualize the HyDE workflow!"""
    console.print("[bold cyan]>>> HYDE WORKFLOW[/bold cyan]")
    console.print()

    tree = Tree(
        "[bold white on blue] HyDE Pipeline [/bold white on blue]",
        guide_style="bright_blue"
    )

    # User query
    step1 = tree.add("[bold cyan][1] User Query[/bold cyan]")
    step1.add("[dim]\"What is semantic chunking?\"[/dim]")

    # Generate hypothesis
    step2 = tree.add("[bold yellow][2] Generate Hypothesis (LLM)[/bold yellow]")
    step2.add("[dim]\"Semantic chunking is a technique that...\"[/dim]")
    step2.add("[magenta]Status: Made-up answer (might be wrong!)[/magenta]")

    # Embed hypothesis
    step3 = tree.add("[bold magenta][3] Embed Hypothesis[/bold magenta]")
    step3.add("[dim]Convert hypothesis to vector[/dim]")
    step3.add("[yellow]Embedding: [0.23, 0.45, 0.78, ...][/yellow]")

    # Vector search
    step4 = tree.add("[bold green][4] Vector Search[/bold green]")
    step4.add("[dim]Search docs using hypothesis embedding[/dim]")
    step4.add("[green]Found: 5 highly relevant documents[/green]")

    # Return results
    step5 = tree.add("[bold blue][5] Return Top Results[/bold blue]")
    step5.add("[bold green]Actual documentation pages![/bold green]")
    step5.add("[magenta]Precision: 89% (vs 72% naive)[/magenta]")

    console.print(tree)
    console.print()


def show_metrics():
    """Show performance metrics!"""
    console.print("[bold cyan]>>> PERFORMANCE METRICS[/bold cyan]")
    console.print()

    metrics = Table(
        box=box.ROUNDED,
        border_style="green",
        header_style="bold white on dark_green"
    )

    metrics.add_column("Metric", style="cyan bold", width=25)
    metrics.add_column("Naive Search", justify="center", style="yellow", width=18)
    metrics.add_column("HyDE", justify="center", style="green bold", width=18)
    metrics.add_column("Improvement", justify="center", style="magenta bold", width=15)

    metrics.add_row("Precision@5", "72%", "89%", "[bold green]+24%[/bold green]")
    metrics.add_row("User Satisfaction", "3.2 stars", "4.5 stars", "[bold green]+41%[/bold green]")
    metrics.add_row("Latency", "120ms", "420ms", "[yellow]+300ms[/yellow]")
    metrics.add_row("Cost/Query", "$0.0001", "$0.0005", "[yellow]+$0.0004[/yellow]")

    console.print(metrics)
    console.print()

    tradeoff = Panel(
        "[bold yellow]TRADE-OFF:[/bold yellow]\n\n"
        "[green]+[/green] Better precision (+20-30%)\n"
        "[green]+[/green] Better vocabulary matching\n"
        "[green]+[/green] Finds actual docs (not meta-content)\n\n"
        "[yellow]-[/yellow] Extra latency (+300-500ms)\n"
        "[yellow]-[/yellow] Extra LLM cost (~$20-60/100K queries)\n\n"
        "[bold white]Worth it?[/bold white] [bold green]YES[/bold green] for high-value queries!",
        title="[yellow]Trade-off Analysis[/yellow]",
        border_style="yellow",
        box=box.ROUNDED
    )
    console.print(tradeoff)
    console.print()


def show_key_insight():
    """Show the key insight!"""
    console.print("[bold cyan]>>> KEY INSIGHT[/bold cyan]")
    console.print()

    insight_title = Text()
    insight_title.append("*** ", style="bold yellow")
    insight_title.append("THE MAGIC TRICK", style="bold white on magenta")
    insight_title.append(" ***", style="bold yellow")

    insight = Panel(
        "[bold cyan]Documents are similar to other documents[/bold cyan]\n\n"
        "By generating a [yellow]fake answer[/yellow], we search in\n"
        "[green]\"document space\"[/green] instead of [red]\"question space\"[/red]\n\n"
        "[bold white]Even if the answer is WRONG:[/bold white]\n"
        "  [green]+[/green] Uses document vocabulary\n"
        "  [green]+[/green] Matches document structure\n"
        "  [green]+[/green] Finds real documentation\n\n"
        "[bold white on blue] VOCABULARY GAP: BRIDGED! [/bold white on blue]",
        title=insight_title,
        border_style="bold magenta",
        box=box.DOUBLE
    )
    console.print(insight)
    console.print()


def show_footer():
    """Rainbow footer!"""
    console.print(create_rainbow_text("=" * 75))

    footer = Text()
    footer.append("  *** HyDE Demo Complete! *** ", style="bold green")
    footer.append("Hypothesis power activated! ", style="italic magenta")
    console.print(footer)

    console.print(create_rainbow_text("=" * 75))
    console.print()


def main():
    """Run the ULTRA COLORFUL HyDE demo!"""

    query = "What is semantic chunking?"

    show_header()
    time.sleep(0.3)

    show_problem()
    time.sleep(0.3)

    show_solution()
    time.sleep(0.3)

    show_query(query)
    time.sleep(0.3)

    hypothesis = generate_hypothesis_animated(query)
    time.sleep(0.3)

    show_comparison_search(query, hypothesis)
    time.sleep(0.3)

    show_workflow_tree()
    time.sleep(0.3)

    show_metrics()
    time.sleep(0.3)

    show_key_insight()
    time.sleep(0.3)

    show_footer()


if __name__ == "__main__":
    main()
