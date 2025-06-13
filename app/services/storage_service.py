# services/storage_service.py
import os
from google.cloud import storage
from fastapi import UploadFile, HTTPException
import uuid

client = None
bucket = None

def get_storage_client():
    global client, bucket
    if client is None:
        bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")
        
        # Try to get the credential path from environment variable, 
        # fallback to the local firebase-service-account.json file
        cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH") or os.getenv("FIREBASE_CREDENTIALS")
        if not cred_path:
            # Use the firebase-service-account.json file in the project root
            cred_path = "firebase-service-account.json"
            if not os.path.exists(cred_path):
                raise RuntimeError("Firebase service account key not found. Either set FIREBASE_SERVICE_ACCOUNT_KEY_PATH environment variable or place firebase-service-account.json in the project root.")

        client = storage.Client.from_service_account_json(cred_path)
        bucket = client.get_bucket(bucket_name)
    return bucket

def upload_file(file: UploadFile) -> str:
    try:
        bucket = get_storage_client()
        ext = file.filename.split('.')[-1]
        blob_name = f"uploads/{uuid.uuid4()}.{ext}"
        blob = bucket.blob(blob_name)
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()
        return blob.public_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")
