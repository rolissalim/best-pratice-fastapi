from pydantic import EmailStr, field_validator
from typing import Optional
from app.base import BaseSchema
from datetime import datetime
from app.models.role_model import Role
from pydantic_core.core_schema import ValidationInfo
from app.base.base_schema import DefaultSchema
# from app.modules.role.schema import RoleWithMenuSchema
from uuid import UUID

class UserBaseSchema(BaseSchema):
    email: EmailStr
    name: str
    updated_at: Optional[datetime] = None
    role_id:int
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "rahasia123"
            }
        }
    }
   

         
class UserCreateSchema(UserBaseSchema):
    password: str

class UserUpdateSchema(UserBaseSchema):
    password: Optional[str] = None
    
    # class Config:
    #     orm_mode = True
    #     extra = "ignore"  # <-- biar field tak dikenal di body diabaikan

class UserChangePasswordSchema(BaseSchema):
    new_password: str
    repeat_password: str

    @field_validator("repeat_password", mode="before")
    @classmethod
    def passwords_match(cls, value: str, values: ValidationInfo):
        if "new_password" in values.data and value != values.data["new_password"]:
            raise ValueError("Passwords do not match!")
        return value
    
class UserReadSchema(UserBaseSchema):
        id: UUID
        is_active: Optional[bool] = False
        role: Optional[DefaultSchema] = None
        role_id:int
        # photo: Optional[str] = None
        created: Optional[DefaultSchema] = None   

# class UserReadSchema(UserBaseSchema):
#     id: str
#     # partai_id: Optional[int] = None 
#     # partai: Optional[PartaiReadSchema] = None
#     workspace_id: Optional[str] = None
#     workspace: Optional[WorkspaceReadSchema] = None
