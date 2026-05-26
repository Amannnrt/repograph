import hashlib


def generate_chunk_id(file_path: str,chunk_type: str,name: str,) -> str:
    """
    Generate stable deterministic chunk IDs.

    Same chunk
    → same ID
    → Qdrant upsert replaces old vector
    """

    raw = f"{file_path}:{chunk_type}:{name}"

    return hashlib.md5(
        raw.encode("utf-8")
    ).hexdigest()
