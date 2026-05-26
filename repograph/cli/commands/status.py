from rich import print
from qdrant_client import QdrantClient


def status_command():

    db_path = ".repograph/qdrant"
    collection_name = "code_chunks"

    try:

        client = QdrantClient(
            path=db_path,
        )

        collections = (
            client.get_collections()
        )

        existing = [
            c.name
            for c in collections.collections
        ]

        if collection_name not in existing:

            print(
                "[red]No index found[/red]"
            )

            return

        info = client.get_collection(
            collection_name=collection_name,
        )

        points_count = (
            info.points_count
        )

        vector_size = (
            info.config.params.vectors.size
        )

        distance = (
            info.config.params.vectors.distance
        )

        print(
            "\n[bold green]RepoGraph Status[/bold green]\n"
        )

        print(
            f"[cyan]Collection:[/cyan] "
            f"{collection_name}"
        )

        print(
            f"[green]Chunks Indexed:[/green] "
            f"{points_count}"
        )

        print(
            f"[yellow]Vector Size:[/yellow] "
            f"{vector_size}"
        )

        print(
            f"[magenta]Distance:[/magenta] "
            f"{distance}"
        )

        print(
            f"[blue]Vector DB:[/blue] "
            f"{db_path}"
        )

        print("")

    except Exception as error:

        print(
            f"[red]Status error:[/red] "
            f"{error}"
        )
