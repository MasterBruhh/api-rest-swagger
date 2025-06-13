from fastapi import APIRouter, HTTPException
from app.services import auth_service
from app.schemas.auth_schemas import LoginRequest, LoginResponse

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesión",
    responses={
        404: {"description": "Usuario no encontrado"},
        500: {"description": "Error en el servidor"}
    }
)
def login(request: LoginRequest):
    """
    Autentica a un usuario con email y contraseña, devolviendo un token de Firebase.
    """
    result = auth_service.login_user(request.email, request.password)
    return result
