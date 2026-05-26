from pydantic import BaseModel
from typing import Optional


class RepositoryFile(BaseModel):
    path: str
    language: str
    content: str
    size_bytes: int 

class CodeChunk(BaseModel):
    chunk_id: str
    file_path: str
    language: str
    chunk_type: str
    name: str
    content: str 
    start_line: int
    end_line: int
    docstring:Optional[str] = None
