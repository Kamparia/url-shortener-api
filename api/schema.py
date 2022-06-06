from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, dataclasses


class Url(BaseModel):
    """
    UrlShortener class
    """
    long_url: str
    hash_value: str
    clicks: Optional[int] = 0
    created_at: Optional[datetime] = datetime.now()
    deleted: Optional[bool] = False

    class Config:
        orm_mode = True


@dataclasses.dataclass
class UrlResponse:
    """
    Filtered response attributes for Url class
    """
    long_url: str
    short_url: str
    clicks: int


class Status(str, Enum):
    """
    Status class
    """
    OK = "OK"
    ERROR = "ERROR"


class Response(BaseModel):
    """
    Response class
    """
    status: Status
    code: int = 200
    message: str
    data: Optional[UrlResponse] = None
