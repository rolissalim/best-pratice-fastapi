
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Union


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    
    
class DefaultSchema(BaseSchema):
    id: Union[str, int]
    name: Optional[str] = None

class BaseResponseSchema(DefaultSchema):
    description: Optional[str] = None
    is_active: Optional[bool] = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created: Optional[DefaultSchema] = None