import ollama

from repograph.providers.embeddings.base import (
    EmbeddingProvider,
)


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

        for text in texts:

            response = ollama.embeddings(
                model=self.model,
                prompt=text,
            )

            embeddings.append(
                response["embedding"]
            )

        return embeddings
