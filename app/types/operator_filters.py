from pydantic import BaseModel
from typing import Optional


class OperatorFilter(BaseModel):
    id: Optional[int] = None
    name__icontains: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    value__icontains: Optional[str] = None
