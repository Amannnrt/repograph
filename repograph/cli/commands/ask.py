import typer
from rich import print

from repograph.providers.llm.ollama_provider import (
    OllamaLLMProvider,
)
from repograph.retrieval.prompt_builder import (
    build_prompt,
)
from repograph.retrieval.retriever import (
    Retriever,
)


def ask_command(
    query: str = typer.Argument(
        ...,
        help="Question to ask about repository",
    )
):

    print(
        f"[cyan]Query:[/cyan] {query}"
    )


    retriever = Retriever()

    results = retriever.search(query,limit=2)

    print(
        f"[green]Retrieved {len(results)} chunks[/green]"
    )


    prompt = build_prompt(
        query=query,
        retrieved_chunks=results,
    )


    llm = OllamaLLMProvider()

    print(
        "[yellow]Generating answer...[/yellow]"
    )

    answer = llm.generate(prompt)

    print("\n")
    print("=" * 60)

    print(
        "[bold green]Answer:[/bold green]\n"
    )

    print(answer)
