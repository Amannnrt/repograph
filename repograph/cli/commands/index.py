#file : repograph/cli/commands/index.py

from pathlib import Path

import typer
from rich import print

from repograph.indexing.chunker import ASTChunker
from repograph.indexing.loader import RepositoryLoader


def index_command(
    repo_path: str = typer.Argument(
        ".",
        help="Path to the repository to index",
    )
):
    repo = Path(repo_path).resolve()

    if not repo.exists():
        print("[red]Repository path does not exist[/red]")
        raise typer.Exit(code=1)

    if not repo.is_dir():
        print("[red]Provided path is not a directory[/red]")
        raise typer.Exit(code=1)

    print(f"[green]Indexing repository:[/green] {repo}")

    # STEP 1 — Load repository files
    loader = RepositoryLoader()

    files = loader.load(str(repo))

    print(f"[cyan]Loaded {len(files)} source files[/cyan]")

    # STEP 2 — Chunk files using AST parsing
    chunker = ASTChunker()

    all_chunks = []

    for file in files:

        chunks = chunker.chunk(file)

        all_chunks.extend(chunks)

    print(f"[green]Extracted {len(all_chunks)} chunks[/green]")

    # STEP 3 — Preview chunks
    for chunk in all_chunks[:10]:

        print("=" * 50)

        print(f"[bold cyan]Function:[/bold cyan] {chunk.name}")

        print(
            f"[yellow]Lines:[/yellow] "
            f"{chunk.start_line}-{chunk.end_line}"
        )

        print(
            f"[magenta]File:[/magenta] "
            f"{chunk.file_path}"
        )
