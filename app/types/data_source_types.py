from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class MysqlDataSource(BaseModel):
    host: str
    port: int
    password: Optional[str] = None
    user: str
    db: str

    class Config:
        title = 'Mysql'


class ElasticsearchDataSource(BaseModel):
    url: str

    class Config:
        title = 'Elasticsearch'


class RestDataSource(BaseModel):
    
    class Type(Enum):
        POST = "post"
        GET = "get"

    type: Type
    headers: List[str]
    url: str
    body: Optional[List[str]] = None

    class Config:
        title = 'Rest'
