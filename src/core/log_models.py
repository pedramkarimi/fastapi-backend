# app/core/log_models.py
from typing import Any, Optional
from pydantic import BaseModel


class RequestLog(BaseModel):
    method: str
    path: str
    status_code: int
    duration_ms: float
    client_ip: Optional[str] = None
    user_id: Optional[str] = None  
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    extra: dict[str, Any] = {}
