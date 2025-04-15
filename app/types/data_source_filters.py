from pydantic import BaseModel
from typing import Optional


class DataSourceFilter(BaseModel):
    id: Optional[int] = None
    name__icontains: Optional[str] = None
    type: Optional[str] = None
    url__icontains: Optional[str] = None
    