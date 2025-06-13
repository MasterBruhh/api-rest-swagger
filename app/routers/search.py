from fastapi import APIRouter, HTTPException, Query
from app.schemas.search import SearchResponse
from app.services import search_service

router = APIRouter(prefix="/search", tags=["search"])

@router.get(
    "/",
    response_model=SearchResponse,
    summary="Buscar documentos",
    description="Busca texto en los documentos indexados mediante Meilisearch."
)
async def search_files(q: str = Query(..., min_length=1, description="Texto a buscar")):
    """Realiza la consulta en Meilisearch y devuelve coincidencias."""
    try:
        search_res = search_service.search_documents(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en búsqueda: {e}")
    results = []
    for hit in search_res.get("hits", []):
        results.append({
            "id": hit.get("id"),
            "filename": hit.get("filename"),
            "snippet": hit.get("_snippetResult", {}).get("content", {}).get("value", "")
        })
    return {"results": results}