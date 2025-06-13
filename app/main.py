"""
Punto de arranque del backend FastAPI.

Contiene la instancia `app` con una descripción extensa que se 
mostrará en Swagger UI (`/docs`) y ReDoc (`/redoc`).
Agrupa las rutas por tags con iconos para facilitar la navegación.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

import os

# Routers
from app.routers import files, search, auth_routes as auth, audit_routes as audit, document_routes

# ----------------------------------------------------------------------
# Cargar variables de entorno (.env)
# ----------------------------------------------------------------------

APP_NAME = os.getenv("APP_NAME", "Indexador de Archivos API")
DEBUG_MODE = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

# Descripción larga que se mostrará en Swagger / ReDoc
long_description = """
# API REST – Indexador de Documentos con Gemini AI

Bienvenido a la API que permite **subir, indexar, buscar y descargar** documentos
utilizando Google Gemini para la extracción de metadatos y resúmenes,
Firebase para autenticación y almacenamiento, y Meilisearch para búsquedas *full-text*.

## Flujo general
1. **POST /documents/upload** – El cliente sube un archivo.
2. El backend lo guarda en Firebase Storage, lo analiza con Gemini,
   guarda los metadatos en Firestore y lo indexa en Meilisearch.
3. El cliente puede consultar metadatos en **GET /documents/{id}**
   o buscar texto en **GET /search?q=…**.
"""

openapi_tags = [
    {"name": "🔐 Autenticación", "description": "Registro y datos del usuario"},
    {"name": "📄 Documentos", "description": "Carga, descarga y metadatos de archivos"},
    {"name": "🔍 Búsqueda", "description": "Consulta de documentos indexados"},
    {"name": "📊 Auditoría", "description": "Eventos y estadísticas de auditoría"},
]

# ----------------------------------------------------------------------
# Crear instancia FastAPI
# ----------------------------------------------------------------------
app = FastAPI(
    title=APP_NAME,
    description=long_description,
    version="1.0.0",
    debug=DEBUG_MODE,
    openapi_tags=openapi_tags,
)

# ----------------------------------------------------------------------
# CORS
# ----------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS.split(",") if ALLOWED_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# Ruta raíz para evitar 404 en "/"
# ----------------------------------------------------------------------
@app.get("/", summary="Bienvenida")
def root():
    return {
        "message": "🚀 Bienvenido al Indexador de Archivos con Gemini AI",
        "version": app.version,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "✅ Operativo",
    }

# ----------------------------------------------------------------------
# Incluir routers con respuestas globales
# ----------------------------------------------------------------------
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["🔐 Autenticación"],
    responses={
        401: {"description": "No autorizado"},
        403: {"description": "Prohibido"},
        500: {"description": "Error interno"},
    },
)

app.include_router(
    files.router,
    tags=["📄 Documentos"],
    responses={
        400: {"description": "Solicitud incorrecta"},
        404: {"description": "No encontrado"},
        413: {"description": "Archivo demasiado grande"},
        500: {"description": "Error interno"},
    },
)

app.include_router(
    document_routes.router,
    tags=["📄 Documentos"],
    responses={
        400: {"description": "Solicitud incorrecta"},
        404: {"description": "No encontrado"},
        413: {"description": "Archivo demasiado grande"},
        500: {"description": "Error interno"},
    },
)

app.include_router(
    search.router,
    prefix="/search",
    tags=["🔍 Búsqueda"],
    responses={
        400: {"description": "Solicitud incorrecta"},
        500: {"description": "Error interno"},
    },
)

app.include_router(
    audit.router,
    prefix="/audit",
    tags=["📊 Auditoría"],
    responses={
        401: {"description": "No autenticado"},
        403: {"description": "Prohibido"},
        500: {"description": "Error interno"},
    },
)
