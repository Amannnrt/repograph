from pydantic import BaseModel

class RepositoryFile(BaseModel):
    path: str
    language: str
    content: str
    size_bytes: int 

    
