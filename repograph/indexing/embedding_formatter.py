from repograph.core.models import (
    CodeChunk,
)

MAX_CHARS = 4000


def truncate_text(
    text: str,
    max_chars: int,
) -> str:

    if len(text) <= max_chars:
        return text

    return text[:max_chars]


def format_chunk_for_embedding(
    chunk: CodeChunk,
) -> str:

    content = truncate_text(
        chunk.content,
        MAX_CHARS,
    )

    docstring = truncate_text(
        str(chunk.docstring),
        1000,
    )

    return f"""
Chunk Type: {chunk.chunk_type}

Name:
{chunk.name}

Docstring:
{docstring}

Code:
{content}
"""
