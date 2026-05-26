import uuid

from tree_sitter import Language, Node, Parser
from tree_sitter_python import language

from repograph.core.models import CodeChunk


PY_LANGUAGE = Language(language())
parser = Parser(PY_LANGUAGE)


def parse_code(code: str):
    """
    Parse Python source code into a tree-sitter AST.
    """
    return parser.parse(bytes(code, "utf-8"))


def extract_docstring(node: Node, code: str) -> str | None:
    """
    Extract docstring from function/class body if present.
    """

    for child in node.children:

        if child.type == "block":

            for block_child in child.children:

                if block_child.type == "expression_statement":

                    text = code[
                        block_child.start_byte:block_child.end_byte
                    ]

                    stripped = text.strip()

                    if (
                        stripped.startswith('"""')
                        or stripped.startswith("'''")
                    ):
                        return stripped

    return None


def create_chunk(
    node: Node,
    code: str,
    file_path: str,
    chunk_type: str,
) -> CodeChunk:
    """
    Create a CodeChunk from an AST node.
    """

    start_byte = node.start_byte
    end_byte = node.end_byte

    content = code[start_byte:end_byte]

    name = "unknown"

    for child in node.children:

        if child.type == "identifier":
            name = code[child.start_byte:child.end_byte]
            break

    return CodeChunk(
        chunk_id=str(uuid.uuid4()),
        file_path=file_path,
        language="python",
        chunk_type=chunk_type,
        name=name,
        content=content,
        start_line=node.start_point[0] + 1,
        end_line=node.end_point[0] + 1,
        docstring=extract_docstring(node, code),
    )


def walk_tree(
    node: Node,
    code: str,
    file_path: str,
    chunks: list[CodeChunk],
):
    """
    Recursively traverse AST and extract chunks.
    """

    if node.type == "function_definition":

        chunks.append(
            create_chunk(
                node=node,
                code=code,
                file_path=file_path,
                chunk_type="function",
            )
        )

    elif node.type == "async_function_definition":

        chunks.append(
            create_chunk(
                node=node,
                code=code,
                file_path=file_path,
                chunk_type="async_function",
            )
        )

    elif node.type == "class_definition":

        chunks.append(
            create_chunk(
                node=node,
                code=code,
                file_path=file_path,
                chunk_type="class",
            )
        )

    for child in node.children:
        walk_tree(
            node=child,
            code=code,
            file_path=file_path,
            chunks=chunks,
        )


def extract_chunks(
    code: str,
    file_path: str,
) -> list[CodeChunk]:
    """
    Extract semantic chunks from Python code.
    """

    tree = parse_code(code)

    root = tree.root_node

    chunks: list[CodeChunk] = []

    walk_tree(
        node=root,
        code=code,
        file_path=file_path,
        chunks=chunks,
    )

    return chunks
