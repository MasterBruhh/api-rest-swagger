# services/auth_service.py
import firebase_admin
from firebase_admin import auth, credentials
import os
from fastapi import HTTPException

cred_path = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def login_user(email: str, password: str) -> dict:
    """
    Simula el proceso de login usando Firebase Admin SDK.
    IMPORTANTE: Firebase Admin SDK no permite verificar contraseñas directamente.
    En producción, este paso se realiza en el frontend con Firebase JS SDK.
    """
    try:
        user = auth.get_user_by_email(email)
        custom_token = auth.create_custom_token(user.uid)
        return {"token": custom_token.decode("utf-8"), "user_id": user.uid}
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def validate_token(token: str) -> dict:
    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
