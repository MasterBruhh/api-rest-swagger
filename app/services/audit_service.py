import os
from google.cloud import firestore
from datetime import datetime

# Obtiene la ruta de credenciales igual que los otros services
cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
if not cred_path:
    cred_path = "firebase-service-account.json"
    if not os.path.exists(cred_path):
        raise RuntimeError(
            "No se encontró el archivo de credenciales. "
            "Define FIREBASE_SERVICE_ACCOUNT_KEY_PATH en .env "
            "o coloca firebase-service-account.json en la raíz del proyecto."
        )

client = firestore.Client.from_service_account_json(cred_path)

def log_audit_event(action: str, user_id: str, resource_id: str, details: dict):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "user_id": user_id,
        "resource_id": resource_id,
        "details": details,
    }
    client.collection("audit_logs").add(event)

def get_audit_logs(limit: int = 50):
    logs = (
        client.collection("audit_logs")
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    return [log.to_dict() for log in logs]
