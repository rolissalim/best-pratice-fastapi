from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional,Union
import math

T = TypeVar("T")
class BaseResponse(BaseModel, Generic[T]):
    message: str
    data: Union[T, List[T]]   # <-- bisa object atau list
    
def response_json(data, message) -> BaseResponse[T]:
    return BaseResponse(
        message=message,
        data=data
    )

class Pagination(BaseModel):
    page: int
    per_page: int
    total_pages: int
    total_count: Optional[int] = None


class BaseResponsePagination(BaseModel, Generic[T]):
    message: str
    data: List[T]
    pagination: Pagination


def response_json_pagination(data, message, common_params, count: int) -> BaseResponsePagination[T]:
    return BaseResponsePagination(
        message=message,
        data=data,
        pagination=Pagination(
            page=common_params.page, 
            per_page=common_params.limit, 
            total_pages=math.ceil(count/common_params.limit),
            total_count=count
        )
    )
