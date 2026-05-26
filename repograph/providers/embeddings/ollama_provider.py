import ollama
from rich import print

from repograph.providers.embeddings.base import (
    EmbeddingProvider,
)


MAX_EMBED_INPUT_CHARS = 3000


def safe_text(
    text: str,
) -> str:

    text = text or ""

    if len(text) > MAX_EMBED_INPUT_CHARS:
        return text[:MAX_EMBED_INPUT_CHARS]

    return text


class OllamaEmbeddingProvider(
    EmbeddingProvider
):

    def __init__(
        self,
        model: str = "nomic-embed-text",
    ):
        self.model = model

    def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        embeddings = []

        for idx, text in enumerate(texts):

            safe_prompt = safe_text(text)

            try:

                response = ollama.embed(
                    model=self.model,
                    input=safe_prompt,
                )

                embeddings.append(
                    response["embeddings"][0]
                )

            except Exception as error:

                print(
                    f"[red]Embedding failed "
                    f"for chunk {idx}[/red]"
                )

                print(
                    f"[yellow]Input size:[/yellow] "
                    f"{len(safe_prompt)} chars"
                )

                print(
                    f"[red]{error}[/red]"
                )

                continue

        return embeddings
