# API REST - Indexador de Documentos con Gemini AI

Una API REST moderna construida con FastAPI que permite subir, indexar, buscar y descargar documentos utilizando Google Gemini para la extracción de metadatos y resúmenes, Firebase para autenticación y almacenamiento, y MeiliSearch para búsquedas full-text.

## Características

- **Carga de documentos**: Sube archivos y obtén metadatos automáticamente
- **Análisis con IA**: Utiliza Google Gemini para extraer información y generar resúmenes
- **Búsqueda avanzada**: Búsqueda full-text con MeiliSearch
- **Autenticación**: Sistema de autenticación con Firebase
- **Auditoría**: Sistema completo de auditoría de eventos
- **API Documentada**: Documentación automática con Swagger UI

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Firebase**: Autenticación y almacenamiento
- **MeiliSearch**: Motor de búsqueda full-text
- **Google Gemini AI**: Análisis de documentos con IA
- **Python 3.8+**: Lenguaje de programación

## Requisitos Previos

1. **Python 3.8 o superior**
2. **MeiliSearch**: Motor de búsqueda (ver instalación abajo)
3. **Cuenta de Firebase**: Para autenticación y almacenamiento
4. **API Key de Google Gemini**: Para análisis de documentos

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd API_REST
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Instalar MeiliSearch

#### Opción A: Descarga directa (Windows)
```bash
# Descargar MeiliSearch
curl -L https://github.com/meilisearch/meilisearch/releases/latest/download/meilisearch-windows-amd64.exe -o meilisearch.exe
```

#### Opción B: Usando package manager
```bash
# Con Chocolatey (Windows)
choco install meilisearch

# Con Homebrew (Mac)
brew install meilisearch

# Con Cargo (Rust)
cargo install meilisearch
```

### 5. Configurar variables de entorno
```bash
# Copiar el template de variables de entorno
cp env_template.txt .env
```

Editar `.env` con tus configuraciones:
- `FIREBASE_STORAGE_BUCKET`: Tu bucket de Firebase
- `GOOGLE_API_KEY`: Tu API key de Google Gemini
- `MEILISEARCH_URL`: URL de MeiliSearch (por defecto: http://localhost:7700)
- `MEILISEARCH_API_KEY`: API key de MeiliSearch

### 6. Configurar Firebase
- Coloca tu archivo `firebase-service-account.json` en la raíz del proyecto
- Asegúrate de que el archivo esté en `.gitignore`

## Uso

### 1. Iniciar MeiliSearch
```bash
# Si descargaste el ejecutable
./meilisearch.exe --master-key="YANbjf2cpIbWL4RKPaIaeOyTkKQ80Wo3i8yub5ToUeA"

# O si lo instalaste globalmente
meilisearch --master-key="YANbjf2cpIbWL4RKPaIaeOyTkKQ80Wo3i8yub5ToUeA"
```

### 2. Iniciar la aplicación
```bash
# Modo desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Modo producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Acceder a la documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Estructura del Proyecto

```
API_REST/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── routers/             # Rutas de la API
│   ├── services/            # Lógica de negocio
│   ├── schemas/             # Modelos Pydantic
│   └── utils/               # Utilidades
├── venv/                    # Entorno virtual
├── firebase-service-account.json  # Credenciales Firebase (no versionar)
├── env_template.txt         # Template de variables de entorno
├── requirements.txt         # Dependencias Python
├── .env                     # Variables de entorno (no versionar)
└── README.md               # Este archivo
```

## Endpoints Principales

### Autenticación
- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Iniciar sesión

### Documentos
- `POST /files` - Subir archivo
- `GET /files/{id}` - Obtener metadatos
- `GET /files/{id}/download` - Descargar archivo

### Búsqueda
- `GET /search?q=texto` - Buscar documentos

### Auditoría
- `GET /audit/events` - Obtener eventos de auditoría

## Resolución de Problemas

### MeiliSearch no inicia
1. Verifica que el puerto 7700 esté libre
2. Asegúrate de que la API key sea correcta
3. Verifica los permisos del ejecutable

### Errores de Firebase
1. Verifica que `firebase-service-account.json` esté presente
2. Confirma que el bucket de Firebase esté configurado
3. Verifica los permisos del proyecto Firebase

### Errores de Gemini AI
1. Verifica que tu API key sea válida
2. Confirma que tengas créditos disponibles
3. Verifica los límites de rate limiting

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contribución

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request 