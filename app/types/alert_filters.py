from pydantic import BaseModel
from typing import Optional


class AlertFilter(BaseModel):
    id: Optional[int] = None
    monitor_id: Optional[int] = None
    operator_id: Optional[int] = None
    name__icontains: Optional[str] = None
    name: Optional[str] = None
    condition__icontains: Optional[str] = None
    duration: Optional[int] = None
    level: Optional[int] = None



class AlertResultFilter(BaseModel):
    id: Optional[int] = None
    alert_id: Optional[int] = None
    project_name__icontains: Optional[str] = None
    level: Optional[int] = None
    is_passed: Optional[bool] = None
    