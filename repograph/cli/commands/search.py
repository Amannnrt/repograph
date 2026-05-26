import typer
from rich import print

from repograph.retrieval.retriever import Retriever


def search_command(
    query: str = typer.Argument(
        ...,
        help="Semantic code search query",
    )
):

    print(
        f"[cyan]Search Query:[/cyan] {query}"
    )

    retriever = Retriever()

    results = retriever.search(
        query=query,
        limit=5,
    )

    print(
        f"[green]Found {len(results)} matching chunks[/green]\n"
    )

    for i, result in enumerate(results, start=1):

        payload = result.payload

        print("=" * 60)

        print(
            f"[bold yellow]{i}. {payload['name']}[/bold yellow]"
        )

        print(
            f"[cyan]Type:[/cyan] "
            f"{payload['chunk_type']}"
        )

        print(
            f"[magenta]File:[/magenta] "
            f"{payload['file_path']}"
        )

        print(
            f"[green]Lines:[/green] "
            f"{payload['start_line']}"
            f"-"
            f"{payload['end_line']}"
        )

        print(
            f"[blue]Docstring:[/blue] "
            f"{payload.get('docstring')}"
        )

        print(
            f"[red]Score:[/red] "
            f"{round(result.score, 4)}"
        )

        print("\n[bold]Code:[/bold]\n")

        print(
            payload["content"][:1500]
        )

        print("\n")
