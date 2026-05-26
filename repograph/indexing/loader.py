#file : repograph/indexing/loader.py 
"""
purpose :
recursively scan repos,
ignore junk folders,
detect,supported files
return structred object

supported languages right now - .py, .ts, .js
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
    def load(self,repo_path:str) -> list[RepositoryFile]:
        repo = Path(repo_path)

        files = []
        for path in repo.rglob("*"):
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            if not path.is_file():
                continue 
            extension = path.suffix 

            if extension not in SUPPORTED_EXTENSIONS:
                continue 

            try:
                content = path.read_text(encoding="utf-8")

                files.append(
                    RepositoryFile(
                        path = str(path),
                        language = SUPPORTED_EXTENSIONS[extension],
                        content = content,
                        size_bytes = path.stat().st_size,
                    )
                )
            except Exception:
                print("repository loader error")
                continue 

        return files 

    
        
