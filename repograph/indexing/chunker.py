from repograph.core.models import CodeChunk, RepositoryFile
from repograph.parsing.treesitter.python_parser import extract_chunks


class ASTChunker:

    def chunk(self, file: RepositoryFile) -> list[CodeChunk]:

        if file.language == "python":
            return extract_chunks(
                code=file.content,
                file_path=file.path,
            )

        return []

    
