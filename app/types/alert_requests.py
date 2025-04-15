from pydantic import BaseModel
from typing import Optional


class CreateAlert(BaseModel):
    monitor_id: int
    operator_id: int
    name: str
    condition: str
    duration: int
    tolerance: int
    status: str
    level: int


class UpdateAlert(BaseModel):
    monitor_id: Optional[int] = None
    operator_id: Optional[int] = None
    name: Optional[str] = None
    condition: Optional[str] = None
    duration: Optional[int] = None
    tolerance: Optional[int] = None
    status: Optional[str] = None
    level: Optional[int] = None
