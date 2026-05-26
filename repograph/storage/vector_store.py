from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from repograph.core.models import CodeChunk


class VectorStore:

    def __init__(
        self,
        path: str = ".repograph/qdrant",
        collection_name: str = "code_chunks",
    ):

        self.collection_name = collection_name

        self.client = QdrantClient(
            path=path,
        )

    def create_collection(self,vector_size: int,):

        collections = self.client.get_collections()

        existing = [
            c.name
            for c in collections.collections
        ]

        if self.collection_name in existing:
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def insert_chunks(self,chunks: list[CodeChunk],embeddings: list[list[float]],):
        points = []

        for idx, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            payload = {
                "chunk_id": chunk.chunk_id,
                "file_path": chunk.file_path,
                "language": chunk.language,
                "chunk_type": chunk.chunk_type,
                "name": chunk.name,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "docstring": chunk.docstring,
                "content": chunk.content,
                "commit_hash": (
                    chunk.git_metadata.commit_hash
                    if chunk.git_metadata
                    else None
                                ),

                "author": (
                    chunk.git_metadata.author
                    if chunk.git_metadata
                    else None
                            ),

                "commit_message": (
                    chunk.git_metadata.commit_message
                    if chunk.git_metadata
                    else None
                            ),

                "commit_timestamp": (
                    chunk.git_metadata.commit_timestamp
                    if chunk.git_metadata
                    else None
                        ),

                "change_frequency": (
                    chunk.git_metadata.change_frequency
                    if chunk.git_metadata
                    else 0
                    ),
            }

            points.append(
                PointStruct(
                    id=chunk.chunk_id,
                    vector=embedding,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )
    def search(self,query_embedding: list[float],limit: int = 5,):

        results = self.client.query_points(
        collection_name=self.collection_name,
        query=query_embedding,
        limit=limit,
        )

        return results.points
