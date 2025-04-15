from pydantic import BaseModel
from typing import Optional, Any


class ApiResponse(BaseModel):
    status: bool
    message: Optional[str] = None
    data: Any
