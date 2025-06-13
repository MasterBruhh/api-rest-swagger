from datetime import datetime

def current_timestamp():
    return datetime.utcnow().isoformat()

def extract_text_dummy(content: bytes) -> str:
    return "Contenido simulado del archivo para indexación."