# schemas/auth_schemas.py
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@ejemplo.com",
                "password": "passwordSeguro123"
            }
        }

class LoginResponse(BaseModel):
    token: str
    user_id: str

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
                "user_id": "uid_usuario_firebase"
            }
        }
