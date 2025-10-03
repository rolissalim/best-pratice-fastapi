from typing import Optional, Any
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

class NotFoundException(HTTPException):
    def __init__(self, name: str, data:Optional[Any] = None):
        logging.error(msg=f"{name} not found", extra={"data": jsonable_encoder(data)})
        super().__init__(status_code=404, detail=f"{name} not found")
        
        
class InternalServerException(HTTPException):
    def __init__(self, name: str, exc, data:Optional[Any] = None):
        logging.error(
            msg=f"Failed to retrieve {name} due to an unexpected error", 
            extra={"error": str(exc), "params": jsonable_encoder(data)}
        )
        # super().__init__(status_code=500, detail="internal server error")
        super().__init__(status_code=500, detail=str(exc))


class ErrorResponseData(BaseModel):
    fields: Dict[str, list[str]]

class ErrorResponse(BaseModel):
    status: bool
    message: str
    errors: ErrorResponseData


async def custom_validation(exc: RequestValidationError):
    error_fields = {}
    for error in exc.errors():
        field = error["loc"][-1]
        message = error["msg"]
        if field in error_fields:
            error_fields[field].append(message)
        else:
            error_fields[field] = [message]
    
    error_response = ErrorResponse(
        status=False,
        message="The given data was invalid.",
        errors=ErrorResponseData(fields=error_fields)
    )

    return error_response