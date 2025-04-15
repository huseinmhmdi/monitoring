from pydantic import BaseModel
from enum import Enum


class UpsetOperator(BaseModel):
    class Type(Enum):
        SMS = "sms"
        EMAIL = "email"
        CALL = "call"
        REST = "rest"

    name: str
    type: Type
    args: dict
