from pydantic import BaseModel
from typing import Optional


class SmsOperator(BaseModel):
    phone_number: str

    class Config:
        title = "Sms"


class CallOperator(BaseModel):
    phone_number: str

    class Config:
        title = "Call"


class EmailOperator(BaseModel):
    email: str

    class Config:
        title = "Email"


class RestOperator(BaseModel):
    url: str
    method: str
    data: Optional[dict] = {}
    headers: Optional[dict] = {}

    class Config:
        title = "Rest"
