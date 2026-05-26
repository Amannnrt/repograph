from pydantic import BaseModel,Field
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
    imports_used: list[str] = Field(default_factory=list)
    parent_class: Optional[str] = None
    is_async: bool = False
