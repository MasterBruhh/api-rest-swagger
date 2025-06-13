from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    id: str
    filename: str
    snippet: str

class SearchResponse(BaseModel):
    results: List[SearchResult]