# services/auth_service.py
import firebase_admin
from firebase_admin import auth, credentials
import os
from fastapi import HTTPException

def ensure_firebase_initialized():
    """Initialize Firebase app if not already initialized"""
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDENTIALS") or os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
        if not cred_path:
            cred_path = "./firebase-service-account.json"

        # Si la ruta es relativa, construye la ruta absoluta basada en el directorio del proyecto
        if not os.path.isabs(cred_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # subir dos niveles desde /app/services
            alt_path = os.path.join(base_dir, cred_path)
            if os.path.exists(alt_path):
                cred_path = alt_path

        # Verificar de nuevo la existencia del archivo
        if not os.path.exists(cred_path):
            raise RuntimeError(
                "Firebase credentials not found. Ensure FIREBASE_CREDENTIALS is set to the correct path or place the JSON in the project root."
            )

        # Inicializar la app de Firebase con credenciales y bucket de Storage
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET")
        })


def login_user(email: str, password: str) -> dict:
    """
    Simula el proceso de login usando Firebase Admin SDK.
    IMPORTANTE: Firebase Admin SDK no permite verificar contraseñas directamente.
    En producción, este paso se realiza en el frontend con Firebase JS SDK.
    """
    ensure_firebase_initialized()
    try:
        user = auth.get_user_by_email(email)
        custom_token = auth.create_custom_token(user.uid)
        return {"token": custom_token.decode("utf-8"), "user_id": user.uid}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def validate_token(token: str) -> dict:
    ensure_firebase_initialized()
    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
