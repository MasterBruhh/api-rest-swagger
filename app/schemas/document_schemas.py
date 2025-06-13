# schemas/document_schemas.py
from pydantic import BaseModel
from typing import List, Optional

class DocumentUploadResponse(BaseModel):
    document_id: str
    status: str
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "doc123",
                "status": "procesado",
                "url": "https://storage.firebase.com/documents/doc123"
            }
        }

class DocumentMetadataResponse(BaseModel):
    id: str
    filename: str
    resumen: str
    keywords: List[str]
    url: str

class SearchResult(BaseModel):
    id: str
    filename: str
    resumen: str
    keywords: List[str]
    score: Optional[float] = None

class DocumentResponse(BaseModel):
    id: str
    filename: str
    resumen: str
    keywords: List[str]
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc123",
                "filename": "archivo.pdf",
                "resumen": "Este es un resumen generado por Gemini AI del contenido del archivo.",
                "keywords": ["inteligencia artificial", "resumen", "Firebase"],
                "url": "https://firebase.storage/documents/doc123"
            }
        }

class SearchResults(BaseModel):
    results: List[DocumentResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {
                        "id": "doc123",
                        "filename": "archivo.pdf",
                        "resumen": "Resumen generado automáticamente por Gemini AI.",
                        "keywords": ["IA", "indexación"],
                        "url": "https://firebase.storage/documents/doc123"
                    }
                ]
            }
        }
