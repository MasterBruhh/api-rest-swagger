from pydantic import BaseModel
from typing import List, Optional

class FileUploadResponse(BaseModel):
    id: str
    filename: str
    message: str

class FileMetadata(BaseModel):
    id: str
    filename: str
    upload_date: str
    summary: Optional[str]
    keywords: List[str] = []
    versions: List[str] = []

class FileMetadataResponse(BaseModel):
    file: FileMetadata