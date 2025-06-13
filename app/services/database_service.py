# services/database_service.py
from google.cloud import firestore
import os

client = None

def get_client():
    global client
    if client is None:
        # Try to get the credential path from environment variable, 
        # fallback to the local firebase-service-account.json file
        cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH") or os.getenv("FIREBASE_CREDENTIALS")
        if not cred_path:
            # Use the firebase-service-account.json file in the project root
            cred_path = "firebase-service-account.json"
            if not os.path.exists(cred_path):
                raise RuntimeError("Firebase service account key not found. Either set FIREBASE_SERVICE_ACCOUNT_KEY_PATH environment variable or place firebase-service-account.json in the project root.")
        
        client = firestore.Client.from_service_account_json(cred_path)
    return client

def save_document_metadata(doc_id: str, metadata: dict):
    get_client().collection("documents").document(doc_id).set(metadata)

def save_metadata(metadata: dict) -> str:
    # Si el diccionario ya tiene un id, usarlo como clave del documento
    if "id" in metadata:
        doc_id = metadata["id"]
        get_client().collection("documents").document(doc_id).set(metadata)
        return doc_id
    else:
        # Si no hay id, agregar el documento con ID automático
        doc_ref = get_client().collection("documents").add(metadata)
        # .add() retorna una tupla (write_result, document_ref)
        return doc_ref[1].id

def get_document_by_id(doc_id: str):
    doc = get_client().collection("documents").document(doc_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

def get_metadata(doc_id: str):
    """Alias for get_document_by_id for compatibility"""
    return get_document_by_id(doc_id)

def get_document_metadata(doc_id: str):
    """Another alias for get_document_by_id for compatibility"""
    return get_document_by_id(doc_id)

def search_documents_by_keyword(keyword: str):
    # Búsqueda simple (simula búsqueda avanzada con Meilisearch)
    docs = get_client().collection("documents").where("keywords", "array_contains", keyword).stream()
    return [doc.to_dict() for doc in docs]
