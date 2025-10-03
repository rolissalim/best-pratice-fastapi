from app.base import *
from app.modules import *
from app.dependency import *
from app.modules.role import *
from app.dependency.deps import role_service_dependency
from app.modules.user.model import User
from app.schemas.schema import DeleteMany
class RoleRouter(BaseRouter):
    
    base_router = BaseRouter(
        module=MODULE, # declare module name and prefix api
        dependencies=[current_user_dependency] # security only user logged can access this api
    )
    
    router = base_router.get_router()

    # this is route for get role
    @router.get("", response_model=BaseResponsePagination[RoleReadSchema])
    async def get_role(
        service: role_service_dependency,
        db: db_dependency,
        common_params: common_params_dependency,
    ):
        try:
            data, count = await service.get_all(common_params, db)            
            return response_json_pagination(
                data=data, 
                message=f"Successfully retrieved {MODULE}",
                common_params=common_params, 
                count=count
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException(MODULE, e, common_params)
        
    
    # this is route for get role menu
    @router.get("/menu/{id}", response_model=BaseResponse[RoleWithMenuSchema])
    async def get_role(
        id: int, 
        service: role_service_dependency,
        db: db_dependency,
        common_params: common_params_dependency,
    ):
        try:
            data = await service.get_by_id(id, db)        
            return response_json(
                message=f"Successfully retrieved {MODULE}",
                data=data, 
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException(MODULE, e, common_params)
    

    # this is route for create role
    @router.post("", response_model=BaseResponse[RoleReadSchema], status_code=status.HTTP_201_CREATED)
    async def create_role(
        create_schema: RoleCreateSchema,
        db: db_dependency, 
        service: role_service_dependency,
        current_user: User = current_user_dependency
    ):
        try:
            create_schema.created_by = current_user.id
            data = await service.create(create_schema, db)
            return response_json(
                message=f"Successfully created {MODULE}",
                data=data,
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
             raise InternalServerException(MODULE, e, create_schema)


    # this is route for delete role
    @router.delete("/delete-many")
    async def delete_many(
        delete_schema: DeleteMany,
        db: db_dependency, 
        service: role_service_dependency
    ):
        try:
            await service.destroy_many(delete_schema, db)            
            return {"deleted": True}
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException(MODULE, e, data={f"{MODULE}_id": id})

        
    # this is route for get role by id
    @router.get("/{id}", response_model=BaseResponse[RoleReadSchema])
    async def get_role_by_id(
        id: int,
        db: db_dependency, 
        service: role_service_dependency, 
    ):
        try:
            data = await service.get_by_id(id, db)        
            return response_json(
                message=f"Successfully retrieved {MODULE}",
                data=data, 
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException(MODULE, e, data={f"{MODULE}_id": id})
        
    
    # this is route for update role
    @router.put("/{id}", response_model=BaseResponse[RoleReadSchema])
    async def update_role(
        id: int,
        update_schema: RoleUpdateSchema,
        db: db_dependency, 
        service: role_service_dependency
    ):
        try:
            data = await service.update(id, update_schema, db)                        
            return response_json(
                message=f"Successfully updated {MODULE}",
                data=data,
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException(MODULE, e, data={f"{MODULE}_id": id})

        
    # this is route for delete role
    @router.delete("/{id}")
    async def delete_role(
        id: int,
        db: db_dependency, 
        service: role_service_dependency
    ):
        try:
            await service.destroy(id, db)            
            return {"deleted": True}
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException(MODULE, e, data={f"{MODULE}_id": id})