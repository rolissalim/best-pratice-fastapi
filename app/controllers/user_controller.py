from fastapi import HTTPException, status
from app.base import *
from app.dependency.deps import current_user_dependency, db_dependency, user_service_dependency, common_params_dependency
from app.schemas.user_schema import UserReadSchema, UserCreateSchema, UserUpdateSchema, UserChangePasswordSchema
from app.models.user_model import User

class UserController(BaseRouter):
    base_router = BaseRouter(
        module="User", # declare module name and prefix api
        dependencies=[current_user_dependency] # security only user logged can access this api
    )

    router = base_router.get_router()

    # this is route for get user
    @router.get("", response_model=BaseResponsePagination[UserReadSchema])
    async def get_user(
        service: user_service_dependency,
        db: db_dependency,
        common_params: common_params_dependency,
    ):
        try:
            users, count = await service.get_user(common_params, db)            
            return response_json_pagination(
                data=users, 
                message=f"Successfully retrieved user",
                common_params=common_params, 
                count=count
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException("user", e, data={"params": common_params})    

    
    # this is route for get profile user
    @router.get("/profile", response_model=BaseResponse[UserReadSchema])
    async def get_profile(
        service: user_service_dependency,
        db: db_dependency,
        current_user: User = current_user_dependency
    ):
        try:
            data = await service.get_user_by_id(current_user.id, db)
            return response_json(
                message="successfully get profile",
                data=data,
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException("user", e, data={"user_id": current_user})
        

    @router.post("", status_code=status.HTTP_201_CREATED, response_model=BaseResponse[UserReadSchema])
    async def create_user(
        create_schema: UserCreateSchema,
        db: db_dependency, 
        service: user_service_dependency,
    ):
        try:
            data = await service.create_user(create_schema, db)
            return response_json(
                message=f"Successfully register new user",
                data=data,
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
             raise InternalServerException("Auth", e, create_schema)
        

    @router.post("/change-password", response_model=BaseResponse[UserReadSchema])
    async def change_password(
        schema: UserChangePasswordSchema,
        db: db_dependency, 
        service: user_service_dependency,
        current_user: User = current_user_dependency
    ):   
        try:
            data = await service.change_password(current_user.id, schema, db)
            return response_json(
                message=f"Successfully change password",
                data=data,
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
             raise InternalServerException("Auth", e, schema)
            
    @router.put("/{id}", response_model=BaseResponse[UserReadSchema])
    async def update_user(
        id: str,
        schema: UserUpdateSchema,
        db: db_dependency, 
        service: user_service_dependency,
    ):
        try:
            data = await service.update(id, schema, db)
            return response_json(
                message=f"Successfully register new user",
                data=data,
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
             raise InternalServerException("Auth", e, schema)