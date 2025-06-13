# routes/audit_routes.py
from fastapi import APIRouter, Query, status
from app.services import audit_service
from app.schemas.audit_schemas import AuditLog, AuditLogCreate
from typing import List

router = APIRouter(
    prefix="/audit",
    tags=["Auditoría"]
)

@router.post(
    "/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar evento de auditoría",
    responses={
        201: {"description": "Evento registrado exitosamente."},
        500: {"description": "Error al registrar evento."}
    }
)
def create_audit_log(log: AuditLogCreate):
    """Registra un nuevo evento en los logs de auditoría."""
    audit_service.log_audit_event(
        action=log.action,
        user_id=log.user_id,
        resource_id=log.resource_id,
        details=log.details
    )
    return {"message": "Evento registrado exitosamente"}

@router.get(
    "/",
    response_model=List[AuditLog],
    summary="Listar eventos recientes de auditoría",
    responses={
        200: {"description": "Listado de eventos retornado con éxito."},
        500: {"description": "Error al obtener eventos."}
    }
)
def list_audit_logs(limit: int = Query(50, ge=1, le=100, description="Número máximo de eventos a retornar (1-100)")):
    """Devuelve los eventos más recientes registrados en auditoría (máx. 100)."""
    logs = audit_service.get_audit_logs(limit=limit)
    return logs
