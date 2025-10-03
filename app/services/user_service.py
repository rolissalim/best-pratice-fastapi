
from app.base import *
from sqlalchemy.orm import Session
from app.models.user_model import User
from datetime import datetime
from app.schemas.user_schema import UserCreateSchema,UserReadSchema
from app.config.security import hash_password
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseService):
    model = User    
    module="user"
    
    async def get_user(self, common_params, db: Session):
        data, count = await self.get_all(common_params=common_params, db=db)
        if not data:
            raise NotFoundException("User", data={"params":common_params})
        return data, count
    
    
    async def get_user_by_id(self, id: str, db: Session):
        data = await self.get_by_id(id=id, db=db)
        if not data:
            raise NotFoundException("User", data={"user_id":id})
        return data   # <-- convert ORM object ke schema
        # return UserReadSchema.from_orm(data)   # <-- convert ORM object ke schema
    
    async def create_user(
    self, 
    user_schema: UserCreateSchema, 
    db: Session, 
) -> UserReadSchema:
     user_schema.password = hash_password(user_schema.password)
     user = await self.create(obj_data=user_schema, db=db) 

     return user
    #  return UserReadSchema.from_orm(user)
    

    async def update(self, id, obj_data, db: Session):
        data = await self.get_by_id(db=db, id=id)
        if data:
            if obj_data.password:
                obj_data.password = hash_password(obj_data.password)
            for field, value in obj_data.model_dump(exclude_unset=True).items():
                if value is not None:  # Skip fields where the value is None
                    setattr(data, field, value)
            db.commit()
            return data
        else:
            return None
        
    async def change_password(self, id, schema, db):
        user = await self.get_user_by_id(id, db)

        hashed_password = pwd_context.hash(schema.new_password)
        user.password = hashed_password

        db.commit()  # Simpan perubahan ke database
        db.refresh(user)  # Refresh user agar mendapatkan data terbaru dari DB

        return user
    