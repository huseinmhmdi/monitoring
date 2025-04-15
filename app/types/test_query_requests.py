from pydantic import BaseModel


class TestQueryRequest(BaseModel):
    query: str
    data_source_id: int
