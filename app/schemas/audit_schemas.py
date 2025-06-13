# schemas/audit_schemas.py
from pydantic import BaseModel
from typing import List

class AuditLog(BaseModel):
    timestamp: str
    user_id: str
    action: str
    resource_id: str
    details: str

    class Config:
        schema_extra = {
            "example": {
                "timestamp": "2024-06-09T10:30:00Z",
                "user_id": "admin",
                "action": "upload",
                "resource_id": "doc123",
                "details": "El usuario subió un archivo PDF."
            }
        }

class AuditQueryResponse(BaseModel):
    logs: List[AuditLog]

    class Config:
        schema_extra = {
            "example": {
                "logs": [
                    {
                        "timestamp": "2024-06-09T10:30:00Z",
                        "user_id": "admin",
                        "action": "upload",
                        "resource_id": "doc123",
                        "details": "El usuario subió un archivo PDF."
                    }
                ]
            }
        }
