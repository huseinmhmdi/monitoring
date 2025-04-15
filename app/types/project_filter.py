from pydantic import BaseModel
from typing import Optional


class ProjectFilter(BaseModel):
    id: Optional[int] = None
    name__icontains: Optional[str] = None
