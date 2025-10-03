from pydantic import EmailStr
from typing import Optional
from app.base import BaseSchema

class TokenSchema(BaseSchema):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    
    
class UserLoginSchema(BaseSchema):
    username: str
    password: str
    
class VerifiyAccount(BaseSchema):
    token: str
    email: EmailStr

class RefreshToken(BaseSchema):
    refresh_token: str
    
class UserRegisterSchema(BaseSchema):
    email: EmailStr
    name: str
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "password": "rahasia123"
            }
        }
    }
   