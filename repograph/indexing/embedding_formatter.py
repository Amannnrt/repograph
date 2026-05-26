from repograph.core.models import CodeChunk 

def format_chunk_for_embedding(chunk: CodeChunk,) -> str:
    return f"""
    Chunk Type: {chunk.chunk_type}
    Name: {chunk.name}
    Docstring: {chunk.docstring}
    code: {chunk.content}
    """
