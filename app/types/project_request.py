from pydantic import BaseModel
from typing import Optional


class CreateProjectRequest(BaseModel):
    name: str
    level_count: int
