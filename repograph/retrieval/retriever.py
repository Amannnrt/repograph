from repograph.indexing.embedding_formatter import (
    format_chunk_for_embedding,
)
from repograph.providers.embeddings.ollama_provider import (
    OllamaEmbeddingProvider,
)
from repograph.storage.vector_store import (
    VectorStore,
)


class Retriever:

    def __init__(self):

        self.embedding_provider = (
            OllamaEmbeddingProvider(
                model="nomic-embed-text"
            )
        )

        self.vector_store = VectorStore()

    def search(self,query: str,limit: int = 5,):

        query_embedding = (
            self.embedding_provider.embed([query])[0]
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            limit=limit,
        )

        return results
