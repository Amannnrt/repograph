from tree_sitter import Language, Parser
from tree_sitter_python import language

from repograph.core.models import CodeChunk
from repograph.utils.hash import generate_chunk_id


PY_LANGUAGE = Language(language())

parser = Parser(PY_LANGUAGE)


def parse_code(code: str):
    tree = parser.parse(
        bytes(code, "utf-8")
    )
    return tree


def get_node_text(code: str, node):
    return code[
        node.start_byte:node.end_byte
    ]


def extract_docstring(code: str, node):

    if len(node.children) == 0:
        return None

    block = node.children[-1]

    if block.type != "block":
        return None

    if len(block.children) == 0:
        return None

    first_stmt = block.children[0]

    if first_stmt.type != "expression_statement":
        return None

    string_node = first_stmt.children[0]

    if string_node.type != "string":
        return None

    return get_node_text(
        code,
        string_node,
    )


def extract_imports(root, code):

    imports = []

    for child in root.children:

        if child.type == "import_statement":

            text = get_node_text(
                code,
                child,
            )

            imports.append(text)

        elif child.type == "import_from_statement":

            text = get_node_text(
                code,
                child,
            )

            imports.append(text)

    return imports


def create_chunk(
    *,
    code: str,
    node,
    file_path: str,
    chunk_type: str,
    language: str,
    parent_class: str | None = None,
    imports_used: list[str] | None = None,
):
    imports_used = imports_used or []
    name = "unknown"

    for child in node.children:

        if child.type == "identifier":

            name = get_node_text(
                code,
                child,
            )

            break

    start_line = (
        node.start_point[0] + 1
    )

    end_line = (
        node.end_point[0] + 1
    )

    node_code = get_node_text(
        code,
        node,
    )

    docstring = extract_docstring(
        code,
        node,
    )

    is_async = (
        node.type
        == "async_function_definition"
    )

    full_name = (
        f"{parent_class}.{name}"
        if parent_class
        else name
    )

    return CodeChunk(
        chunk_id=generate_chunk_id(
            file_path=file_path,
            chunk_type=chunk_type,
            name=full_name,
        ),
        file_path=file_path,
        language=language,
        chunk_type=chunk_type,
        name=full_name,
        content=node_code,
        start_line=start_line,
        end_line=end_line,
        docstring=docstring,
        imports_used=imports_used,
        parent_class=parent_class,
        is_async=is_async,
    )


def walk_tree(
    *,
    code: str,
    node,
    file_path: str,
    language: str,
    imports_used: list[str],
    chunks: list[CodeChunk],
    parent_class: str | None = None,
):

    current_parent = parent_class

    if node.type == "class_definition":

        class_chunk = create_chunk(
            code=code,
            node=node,
            file_path=file_path,
            chunk_type="class",
            language=language,
            imports_used=imports_used,
        )

        chunks.append(class_chunk)

        current_parent = class_chunk.name

    elif node.type in [
        "function_definition",
        "async_function_definition",
    ]:

        function_chunk = create_chunk(
            code=code,
            node=node,
            file_path=file_path,
            chunk_type="function",
            language=language,
            parent_class=parent_class,
            imports_used=imports_used,
        )

        chunks.append(function_chunk)

    for child in node.children:

        walk_tree(
            code=code,
            node=child,
            file_path=file_path,
            language=language,
            imports_used=imports_used,
            chunks=chunks,
            parent_class=current_parent,
        )


        
def extract_chunks(
    *,
    code: str,
    file_path: str,
):

    tree = parse_code(code)

    root = tree.root_node

    imports_used = extract_imports(
        root,
        code,
    )

    chunks = []

    walk_tree(
        code=code,
        node=root,
        file_path=file_path,
        language="python",
        imports_used=imports_used,
        chunks=chunks,
    )

    return chunks
