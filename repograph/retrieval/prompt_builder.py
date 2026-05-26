def build_prompt(
    query: str,
    retrieved_chunks: list,
) -> str:

    context_parts = []

    for chunk in retrieved_chunks:

        payload = chunk.payload

        context_parts.append(
            f"""
FILE: {payload['file_path']}
TYPE: {payload['chunk_type']}
NAME: {payload['name']}

CODE:
{payload['content'][:1200]}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are RepoGraph, a developer intelligence system.

Answer the user's question using ONLY the
provided repository context.

Rules:
- Keep answers concise and technical
- Prefer 3-6 sentences maximum
- Do not hallucinate
- If information is missing, say so
- Mention relevant file names
- Focus on implementation details
- Avoid unnecessary explanation

USER QUESTION:
{query}

REPOSITORY CONTEXT:
{context}

Answer clearly and technically.
Cite relevant file names when possible.
"""

    return prompt
