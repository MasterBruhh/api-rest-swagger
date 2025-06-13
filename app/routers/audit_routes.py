# routes/audit_routes.py
from fastapi import APIRouter, Query, status
from app.services import audit_service
from app.schemas.audit_schemas import AuditLog, AuditLogCreate
from typing import List

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Registrar evento de auditoría")
def create_audit_log(log: AuditLogCreate):
    """Registra un nuevo evento en los logs de auditoría."""
    audit_service.log_audit_event(
        action=log.action,
        user_id=log.user_id,
        resource_id=log.resource_id,
        details=log.details
    )
    return {"message": "Evento registrado exitosamente"}


@router.get("/", response_model=List[AuditLog], summary="Listar eventos recientes de auditoría")
def list_audit_logs(limit: int = Query(50, ge=1, le=100)):
    """Devuelve los eventos más recientes registrados en auditoría (máx. 100)."""
    logs = audit_service.get_audit_logs(limit=limit)
    return logs
