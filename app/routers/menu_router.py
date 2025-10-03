from app.base import *
from app.modules import *
from app.dependency import *
from app.modules.menu import *
from app.dependency.deps import menu_service_dependency
from app.modules.user.model import User
from app.schemas.schema import DeleteMany
from typing import Optional
class MenuRouter(BaseRouter):
    
    base_router = BaseRouter(
        module=MODULE, # declare module name and prefix api
        dependencies=[current_user_dependency] # security only user logged can access this api
    )
    
    router = base_router.get_router()

    # this is route for get Menu
    @router.get("", response_model=BaseResponsePagination[MenuReadSchema])
    async def get_menu(
        service: menu_service_dependency,
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
            raise InternalServerException(MODULE, e, common_params.dict())
    

    # this is route for create Menu
    @router.post("", response_model=BaseResponse[MenuReadSchema], status_code=status.HTTP_201_CREATED)
    async def create_menu(
        create_schema: MenuCreateSchema,
        db: db_dependency, 
        service: menu_service_dependency,
        current_user: User = current_user_dependency
    ):
        try:
            data = await service.create(create_schema, db)
            return response_json(
                message=f"Successfully created {MODULE}",
                data=data,
            )
        except HTTPException as http_ex:
            raise
        except Exception as e:
             raise InternalServerException(MODULE, e, create_schema)


    # this is route for delete Menu
    @router.delete("/delete-many")
    async def delete_many(
        delete_schema: DeleteMany,
        db: db_dependency, 
        service: menu_service_dependency
    ):
        try:
            await service.destroy_many(delete_schema, db)            
            return {"deleted": True}
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException(MODULE, e, data={f"{MODULE}_id": id})

        
    # this is route for get Menu by id
    @router.get("/{id}", response_model=BaseResponse[MenuReadSchema])
    async def get_menu_by_id(
        id: int,
        db: db_dependency, 
        service: menu_service_dependency, 
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
        
    
    # this is route for update Menu
    @router.put("/{id}", response_model=BaseResponse[MenuReadSchema])
    async def update_menu(
        id: int,
        update_schema: MenuUpdateSchema,
        db: db_dependency, 
        service: menu_service_dependency
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

        
    # this is route for delete Menu
    @router.delete("/{id}")
    async def delete_menu(
        id: int,
        db: db_dependency, 
        service: menu_service_dependency
    ):
        try:
            await service.destroy(id, db)            
            return {"deleted": True}
        except HTTPException as http_ex:
            raise
        except Exception as e:
            raise InternalServerException(MODULE, e, data={f"{MODULE}_id": id})