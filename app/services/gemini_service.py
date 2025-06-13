# services/gemini_service.py
import os
import requests
from fastapi import HTTPException

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

headers = {
    "Content-Type": "application/json"
}

def summarize_and_extract_metadata(text: str) -> dict:
    payload = {
        "contents": [{"parts": [{"text": f"Resume y extrae metadata del siguiente contenido: \n{text}"}]}]
    }
    try:
        res = requests.post(f"{GEMINI_URL}?key={GEMINI_API_KEY}", json=payload, headers=headers)
        res.raise_for_status()
        candidates = res.json().get("candidates", [])
        if not candidates:
            raise ValueError("Sin respuesta de Gemini")
        return {"summary": candidates[0]["content"]["parts"][0]["text"]}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error en Gemini API: {str(e)}")
