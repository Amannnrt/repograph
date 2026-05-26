import typer
from rich import print

from repograph.retrieval.retriever import (
    Retriever,
)


def ask_command(
    query: str = typer.Argument(
        ...,
        help="Question to ask about the repository",
    )
):

    print(
        f"[cyan]Query:[/cyan] {query}"
    )

    retriever = Retriever()

    results = retriever.search(query)

    print(
        f"[green]Found {len(results)} relevant chunks[/green]"
    )

    for idx, result in enumerate(results, start=1):

        payload = result.payload

        print("=" * 60)

        print(
            f"[bold yellow]{idx}. "
            f"{payload['name']}[/bold yellow]"
        )

        print(
            f"[magenta]Type:[/magenta] "
            f"{payload['chunk_type']}"
        )

        print(
            f"[cyan]File:[/cyan] "
            f"{payload['file_path']}"
        )

        print(
            f"[green]Lines:[/green] "
            f"{payload['start_line']}"
            f"-{payload['end_line']}"
        )

        print(
            f"[blue]Docstring:[/blue] "
            f"{payload['docstring']}"
        )

        print(
            f"[white]\n{payload['content'][:500]}"
        )

        print()
