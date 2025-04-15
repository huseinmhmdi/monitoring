from pydantic import BaseModel

from typing import Optional


class UpsertMonitor(BaseModel):
    name: str
    source_id: Optional[int] = None
    project_id: int
    query: str
    interval: int
    is_active: Optional[bool] = None


class UpdateDurationRequest(BaseModel):
    duration: int
    level: int


class MonitorResultCreate(BaseModel):
    data: dict
    monitor_id: int
