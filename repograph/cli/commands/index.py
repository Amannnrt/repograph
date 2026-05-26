from pathlib import Path

import typer
from dotenv import load_dotenv
from rich import print

from repograph.git.history import (
    get_file_git_metadata,
)
from repograph.indexing.chunker import (
    ASTChunker,
)
from repograph.indexing.embedding_formatter import (
    format_chunk_for_embedding,
)
from repograph.indexing.loader import (
    RepositoryLoader,
)
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

        print(
            "[red]Repository path does not exist[/red]"
        )

        raise typer.Exit(code=1)

    if not repo.is_dir():

        print(
            "[red]Provided path is not a directory[/red]"
        )

        raise typer.Exit(code=1)

    print(
        f"[green]Indexing repository:[/green] "
        f"{repo}"
    )

    # Load repository files

    loader = RepositoryLoader()

    files = loader.load(str(repo))

    print(
        f"[cyan]Loaded {len(files)} source files[/cyan]"
    )

    # AST chunking

    chunker = ASTChunker()

    all_chunks = []

    for file in files:

        chunks = chunker.chunk(file)

        git_metadata = get_file_git_metadata(
            repo_path=str(repo),
            relative_file_path=file.path,
        )

        for chunk in chunks:

            chunk.git_metadata = git_metadata

        all_chunks.extend(chunks)

    print(
        f"[green]Extracted "
        f"{len(all_chunks)} chunks[/green]"
    )

    # Preview sample chunks

    for chunk in all_chunks[:5]:

        print("=" * 60)

        print(
            f"[bold cyan]"
            f"{chunk.chunk_type.title()}:"
            f"[/bold cyan] "
            f"{chunk.name}"
        )

        print(
            f"[yellow]Lines:[/yellow] "
            f"{chunk.start_line}-"
            f"{chunk.end_line}"
        )

        print(
            f"[magenta]File:[/magenta] "
            f"{chunk.file_path}"
        )

        print(
            f"[blue]Docstring:[/blue] "
            f"{chunk.docstring}"
        )

    # Embedding generation

    provider = OllamaEmbeddingProvider(
        model="nomic-embed-text"
    )

    safe_chunks = []

    for chunk in all_chunks:

        # Skip absurdly large chunks
        if len(chunk.content) > 50000:
            continue

        safe_chunks.append(chunk)

    texts = [
        format_chunk_for_embedding(chunk)
        for chunk in safe_chunks
    ]

    print(
        "[cyan]Generating embeddings...[/cyan]"
    )

    print(
        f"[cyan]Embedding "
        f"{len(texts)} chunks[/cyan]"
    )

    valid_pairs = []

    for idx, (chunk, text) in enumerate(
        zip(safe_chunks, texts)
    ):

        if idx % 50 == 0:

            print(
                f"[cyan]Embedded "
                f"{idx}/{len(texts)} chunks"
                f"[/cyan]"
            )

        try:

            embedding = (
                provider.embed([text])[0]
            )

            valid_pairs.append(
                (chunk, embedding)
            )

        except Exception as error:

            print(
                f"[red]Skipped chunk:[/red] "
                f"{chunk.file_path} :: "
                f"{chunk.name}"
            )

            print(
                f"[yellow]Reason:[/yellow] "
                f"{error}"
            )

            continue

    safe_chunks = [
        pair[0]
        for pair in valid_pairs
    ]

    embeddings = [
        pair[1]
        for pair in valid_pairs
    ]

    if not embeddings:

        print(
            "[red]No embeddings generated[/red]"
        )

        raise typer.Exit(code=1)

    print(
        f"[green]Generated "
        f"{len(embeddings)} embeddings"
        f"[/green]"
    )

    print(
        f"[yellow]Embedding dimension:"
        f"[/yellow] "
        f"{len(embeddings[0])}"
    )

    # Store in Qdrant

    vector_store = VectorStore()

    vector_store.create_collection(
        vector_size=len(embeddings[0])
    )

    vector_store.insert_chunks(
        chunks=safe_chunks,
        embeddings=embeddings,
    )

    print(
        "[green]Stored embeddings "
        "in Qdrant[/green]"
    )
