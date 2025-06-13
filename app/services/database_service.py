# services/database_service.py
from google.cloud import firestore
import os

# Try to get the credential path from environment variable, 
# fallback to the local firebase-service-account.json file
cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
if not cred_path:
    # Use the firebase-service-account.json file in the project root
    cred_path = "firebase-service-account.json"
    if not os.path.exists(cred_path):
        raise RuntimeError("Firebase service account key not found. Either set FIREBASE_SERVICE_ACCOUNT_KEY_PATH environment variable or place firebase-service-account.json in the project root.")

client = firestore.Client.from_service_account_json(cred_path)

def save_document_metadata(doc_id: str, metadata: dict):
    client.collection("documents").document(doc_id).set(metadata)

def get_document_by_id(doc_id: str):
    doc = client.collection("documents").document(doc_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

def search_documents_by_keyword(keyword: str):
    # Búsqueda simple (simula búsqueda avanzada con Meilisearch)
    docs = client.collection("documents").where("keywords", "array_contains", keyword).stream()
    return [doc.to_dict() for doc in docs]
