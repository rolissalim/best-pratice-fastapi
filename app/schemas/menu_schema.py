from typing import Optional
from app.base import BaseSchema,base_schema

class MenuBaseSchema(BaseSchema):
    name: str
    route: str
    icon: Optional[str] = None    
    description: Optional[str] = None    
    is_group: int
    parent_id: Optional[int] = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "user",
                "description": "ini deskripsi employee",
                "route": "str",
                "icon": "",
                "is_group": 0,
                "parent_id": None,
            }
        }
    }
        
class MenuCreateSchema(MenuBaseSchema):
    ...

    
class MenuUpdateSchema(MenuCreateSchema):
    ...
    
class MenuReadSchema(BaseResponseSchema):
    route: str
    is_group: Optional[int] = None
    parent_id: Optional[int] = None