from pydantic import BaseModel
from enum import Enum
from typing import Optional, List


class UpsetDataSource(BaseModel):

    class Type(Enum):
        POST = "post"
        GET = "get"

    class Type(Enum):
        MYSQL = "mysql"
        REST = "rest"
        ELASTICSEARCH = "elasticsearch"

    name: str
    type: Type
    host: Optional[str] = None
    port: Optional[int] = None
    password: Optional[str] = None
    user: Optional[str] = None
    db: Optional[str] = None
    type: Optional[Type] = None
    headers: Optional[List[str]] = None
    url: Optional[str] = None
    body: Optional[List[str]] = None
