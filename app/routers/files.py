from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.files import FileUploadResponse, FileMetadataResponse
from app.services import storage_service, database_service as database, search_service
from app.utils.helpers import current_timestamp, extract_text_dummy
import uuid

router = APIRouter(prefix="/files", tags=["files"])

@router.post(
    "/",
    response_model=FileUploadResponse,
    status_code=201,
    summary="Subir e indexar archivo",
    description="""Sube un archivo (PDF, DOCX, PPTX, etc.), lo guarda en Firebase Storage,\nextrae metadatos y lo indexa en Meilisearch."""
)
async def upload_file(file: UploadFile = File(...)):
    """Recibe un archivo en *form‑data* y realiza el proceso completo de indexación."""
    if not file:
        raise HTTPException(status_code=400, detail="No se envió ningún archivo")
    file_id = str(uuid.uuid4())
    content = await file.read()
    file.file.seek(0)
    storage_service.upload_file(file)


    text = extract_text_dummy(content)
    metadata = {
        "id": file_id,
        "filename": file.filename,
        "upload_date": current_timestamp(),
        "summary": "Resumen simulado.",
        "keywords": ["demo", "archivo"],
        "versions": []
    }
    database.save_metadata(metadata)
    meta_for_index = metadata.copy()
    meta_for_index.pop("id", None)
    index_data = {"content": text, **meta_for_index}
    search_service.index_document(file_id, index_data)
    return {"id": file_id, "filename": file.filename, "message": "Archivo indexado correctamente"}

@router.get(
    "/{id}",
    response_model=FileMetadataResponse,
    summary="Obtener metadatos de un archivo",
    description="Devuelve los metadatos, resumen y keywords de un documento previamente indexado."
)
async def get_file_metadata(id: str):
    """Busca la metadata en Firestore a partir del ID del archivo."""
    data = database.get_metadata(id)
    if not data:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return {"file": data}
