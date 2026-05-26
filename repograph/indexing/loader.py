"""
purpose:
recursively scan repositories,
ignore junk folders,
detect supported source files,
return structured RepositoryFile objects

supported languages right now:
- Python (.py)
- TypeScript (.ts)
- JavaScript (.js)
"""

from pathlib import Path

from repograph.core.models import RepositoryFile


IGNORE_DIRS = {
    ".git",
    "node_modules",
    "venv",
    "__pycache__",
    "dist",
    "build",
}


SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".ts": "typescript",
    ".js": "javascript",
}


class RepositoryLoader:

    def load(
        self,
        repo_path: str,
    ) -> list[RepositoryFile]:

        repo = Path(repo_path).resolve()

        files: list[RepositoryFile] = []

        for path in repo.rglob("*"):

            # Skip ignored directories
            if any(part in IGNORE_DIRS for part in path.parts):
                continue

            # Skip non-files
            if not path.is_file():
                continue

            extension = path.suffix

            # Skip unsupported file types
            if extension not in SUPPORTED_EXTENSIONS:
                continue

            try:

                content = path.read_text(
                    encoding="utf-8",
                )

                relative_path = str(
                    path.relative_to(repo)
                )

                files.append(
                    RepositoryFile(
                        path=relative_path,
                        language=SUPPORTED_EXTENSIONS[extension],
                        content=content,
                        size_bytes=path.stat().st_size,
                    )
                )

            except Exception as error:

                print(
                    f"Repository loader error "
                    f"for {path}: {error}"
                )

                continue

        return files
    
        
