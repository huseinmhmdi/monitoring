from pydantic import BaseModel
from typing import Optional, Any


class CrawlMonitoringType(BaseModel):
    type: str
    text: str
    project_id: int
    step: int
    status: bool
    action: str
