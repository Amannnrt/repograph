import uuid

from tree_sitter import Language, Parser
from tree_sitter_python import language

from repograph.core.models import CodeChunk


PY_LANGUAGE = Language(language())
parser = Parser(PY_LANGUAGE)


def parse_code(code: str):
    """
    Parse Python source code into a tree-sitter AST.
    """
    tree = parser.parse(bytes(code, "utf-8"))
    return tree


def extract_functions(code: str, file_path: str) -> list[CodeChunk]:
    """
    Extract top-level Python functions as CodeChunk objects.
    """

    tree = parse_code(code)

    root = tree.root_node

    chunks = []

    for child in root.children:

        if child.type != "function_definition":
            continue

        start_byte = child.start_byte
        end_byte = child.end_byte

        function_code = code[start_byte:end_byte]

        function_name = "unknown"

        for node in child.children:
            if node.type == "identifier":
                function_name = code[node.start_byte:node.end_byte]
                break

        chunk = CodeChunk(
            chunk_id=str(uuid.uuid4()),
            file_path=file_path,
            language="python",
            chunk_type="function",
            name=function_name,
            content=function_code,
            start_line=child.start_point[0] + 1,
            end_line=child.end_point[0] + 1,
        )

        chunks.append(chunk)

    return chunks


if __name__ == "__main__":

    sample_code = """
import jwt

def validate_token(token):
    payload = jwt.decode(token, "secret", algorithms=["HS256"])
    return payload

def login_user(username, password):
    return True
"""

    chunks = extract_functions(
        code=sample_code,
        file_path="auth/service.py",
    )

    for chunk in chunks:
        print("=" * 50)
        print(f"Function: {chunk.name}")
        print(f"Lines: {chunk.start_line} - {chunk.end_line}")
        print(chunk.content)
        print()
