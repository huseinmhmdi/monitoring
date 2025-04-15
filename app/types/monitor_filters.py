from pydantic import BaseModel
from typing import Optional


class MonitorFilter(BaseModel):
    id: Optional[int] = None
    name__icontains: Optional[str] = None
    source_id: Optional[int] = None
    project_id: Optional[int] = None
    query__icontains: Optional[str] = None
    interval: Optional[int] = None
    is_active: Optional[bool] = None
