from pydantic import BaseModel


class TestExecRequest(BaseModel):
    condition: str
    duration: int = 10


class TestProjectRequest(BaseModel):
    count: int
    duration: int = 10
