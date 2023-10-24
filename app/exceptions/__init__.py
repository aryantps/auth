from fastapi import HTTPException
from pydantic import BaseModel
from typing import Any


class AppException(HTTPException):
    def __init__(self,
                 status_code: int,
                 detail: Any = None
                 ):
        super().__init__(status_code=status_code, detail=detail)


class ErrorResponse(BaseModel):
    detail: str
