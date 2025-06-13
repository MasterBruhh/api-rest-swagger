# services/search_service.py
import os
import requests
from fastapi import HTTPException

MEILISEARCH_URL = os.getenv("MEILISEARCH_URL")
MEILISEARCH_KEY = os.getenv("MEILISEARCH_KEY")
INDEX_NAME = "documents"

headers = {
    "X-Meili-API-Key": MEILISEARCH_KEY,
    "Content-Type": "application/json"
}

def index_document(doc_id: str, content: dict):
    url = f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/documents"
    data = [dict(id=doc_id, **content)]
    try:
        res = requests.post(url, json=data, headers=headers)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error al indexar documento en Meilisearch: {str(e)}")

def search_documents(query: str):
    url = f"{MEILISEARCH_URL}/indexes/{INDEX_NAME}/search"
    try:
        res = requests.post(url, json={"q": query}, headers=headers)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error en búsqueda Meilisearch: {str(e)}")
