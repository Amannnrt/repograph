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
from repograph.storage.vector_store import (
    VectorStore,
)

load_dotenv()


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

    print(
        f"[green]Indexing repository:[/green] "
        f"{repo}"
    )

    #loadinf files

    loader = RepositoryLoader()

    files = loader.load(str(repo))

    print(
        f"[cyan]Loaded {len(files)} source files[/cyan]"
    )

    #AST
    chunker = ASTChunker()

    all_chunks = []

    for file in files:

        chunks = chunker.chunk(file)

        all_chunks.extend(chunks)

    print(
        f"[green]Extracted {len(all_chunks)} chunks[/green]"
    )

    #Preview chunks

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
    #Generate embeddings

    provider = OllamaEmbeddingProvider(
        model="nomic-embed-text"
    )

    texts = [
        format_chunk_for_embedding(chunk)
        for chunk in all_chunks
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

    #Store embeddings in Qdrant

    vector_store = VectorStore()

    vector_store.create_collection(
        vector_size=len(embeddings[0])
    )

    vector_store.insert_chunks(
        chunks=all_chunks,
        embeddings=embeddings,
    )

    print(
        "[green]Stored embeddings in Qdrant[/green]"
    )
