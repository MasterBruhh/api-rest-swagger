# routes/document_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Optional, List
from app.services import storage_service, gemini_service, search_service, database_service
from app.schemas.document_schemas import DocumentUploadResponse, DocumentMetadataResponse, SearchResult
from starlette import status

router = APIRouter(
    prefix="/documents",
    tags=["Documentos"]
)

@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Subir y procesar documento",
    responses={
        201: {"description": "Documento subido y procesado exitosamente."},
        400: {"description": "Archivo inválido o error en procesamiento."},
        500: {"description": "Error interno del servidor."}
    }
)
def upload_document(file: UploadFile = File(...)):
    """Carga un archivo al storage, lo analiza con Gemini y lo indexa para búsqueda posterior."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Archivo inválido")

    file_url = storage_service.upload_file(file)
    gemini_result = gemini_service.extract_metadata(file_url)
    doc_id = database_service.save_metadata(gemini_result)
    search_service.index_document(doc_id, gemini_result)

    return DocumentUploadResponse(
        document_id=doc_id,
        status="procesado",
        url=file_url
    )

@router.get(
    "/{document_id}",
    response_model=DocumentMetadataResponse,
    summary="Consultar metadatos de un documento",
    responses={
        200: {"description": "Metadatos obtenidos exitosamente."},
        404: {"description": "Documento no encontrado."}
    }
)
def get_document(document_id: str):
    """Devuelve los metadatos extraídos e indexados de un documento por su ID."""
    document = database_service.get_document_metadata(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return document

@router.get(
    "/search",
    response_model=List[SearchResult],
    summary="Buscar documentos por contenido",
    responses={
        200: {"description": "Resultados de búsqueda retornados con éxito."},
        400: {"description": "Consulta inválida o vacía."}
    }
)
def search_documents(q: str = Query(..., min_length=3, description="Consulta textual a buscar en documentos indexados")):
    """Realiza una búsqueda textual en los documentos previamente indexados."""
    if not q:
        raise HTTPException(status_code=400, detail="Consulta vacía")

    results = search_service.search_documents(q)
    return results
