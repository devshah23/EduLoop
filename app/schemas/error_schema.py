# schemas/error.py
from typing import List, Optional, Union
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    loc: Optional[List[Union[str, int]]] = None
    msg: str
    type: Optional[str] = None

class ErrorResponse(BaseModel):
    message: str
    errors: Optional[List[ErrorDetail]] = None
    code: Optional[str] = None 
