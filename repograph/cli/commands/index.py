import os
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich import print

from repograph.indexing.chunker import ASTChunker
from repograph.indexing.embedding_formatter import (
    format_chunk_for_embedding,
)
from repograph.indexing.loader import RepositoryLoader
from repograph.providers.embeddings.ollama_provider import (
    OllamaEmbeddingProvider,
)

load_dotenv()


def index_command(
    repo_path: str = typer.Argument(
        ".",
        help="Path to the repository to index",
    )
):

    repo = Path(repo_path).resolve()

    # Validate repo path
    if not repo.exists():
        print("[red]Repository path does not exist[/red]")
        raise typer.Exit(code=1)

    if not repo.is_dir():
        print("[red]Provided path is not a directory[/red]")
        raise typer.Exit(code=1)

    print(
        f"[green]Indexing repository:[/green] "
        f"{repo}"
    )

    #load repo files
    loader = RepositoryLoader()

    files = loader.load(str(repo))

    print(
        f"[cyan]Loaded {len(files)} source files[/cyan]"
    )

    #AST chunking
    chunker = ASTChunker()

    all_chunks = []

    for file in files:

        chunks = chunker.chunk(file)

        all_chunks.extend(chunks)

    print(
        f"[green]Extracted {len(all_chunks)} chunks[/green]"
    )

    #preview chunks
    for chunk in all_chunks[:5]:

        print("=" * 60)

        print(
            f"[bold cyan]{chunk.chunk_type.title()}:[/bold cyan] "
            f"{chunk.name}"
        )

        print(
            f"[yellow]Lines:[/yellow] "
            f"{chunk.start_line}-{chunk.end_line}"
        )

        print(
            f"[magenta]File:[/magenta] "
            f"{chunk.file_path}"
        )

        print(
            f"[blue]Docstring:[/blue] "
            f"{chunk.docstring}"
        )

    #generate embeddings
    provider = OllamaEmbeddingProvider(
        model="nomic-embed-text"
    )

    texts = [
        format_chunk_for_embedding(chunk)
        for chunk in all_chunks[:3]
    ]

    print("[cyan]Generating embeddings...[/cyan]")

    embeddings = provider.embed(texts)

    print(
        f"[green]Generated {len(embeddings)} embeddings[/green]"
    )

    print(
        f"[yellow]Embedding dimension:[/yellow] "
        f"{len(embeddings[0])}"
    )
