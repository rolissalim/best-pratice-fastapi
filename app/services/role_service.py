from app.base import *
from app.models import Menu,Role
from sqlalchemy import and_
from sqlalchemy.orm import Session

class RoleService(BaseService):
    model = Role
    module = "role"


    async def create(self, obj_data, db: Session):
        obj = self.model(**obj_data.model_dump(exclude_unset=True))
        db.add(obj)
        db.commit()

        # for permission in obj_data.permissions:
        #     menu = db.query(Menu).filter(Menu.id == permission['menu_id']).first()
        #     if not menu:
        #         raise NotFoundException("menu")
            
        #     role_menu = RoleHasMenu(
        #         role_id=obj.id,
        #         menu_id=permission['menu_id'],
        #         create=permission['create'],
        #         read=permission['read'],
        #         update=permission['update'],
        #         delete=permission['delete'],
        #     )
        #     db.add(role_menu)
        #     db.commit()
        
        db.refresh(obj)


        return obj


    async def update(self, id, obj_data, db: Session):
        data = await self.get_by_id(db=db, id=id)
        if not data:
            return None  # Role not found

        # ✅ Update role fields
        for field, value in obj_data.model_dump(exclude_unset=True).items():
            setattr(data, field, value)
        db.commit()

        # ✅ Delete all existing permissions for this role
        # db.query(RoleHasMenu).filter(RoleHasMenu.role_id == data.id).delete()
        # db.commit()

        # ✅ Insert new permissions
        # new_permissions = []
        # for permission in obj_data.permissions:
        #     menu = db.query(Menu).filter(Menu.id == permission['menu_id']).first()
        #     if not menu:
        #         raise NotFoundException("menu")

        #     new_permissions.append(RoleHasMenu(
        #         role_id=data.id,
        #         menu_id=permission['menu_id'],
        #         create=permission['create'],
        #         read=permission['read'],
        #         update=permission['update'],
        #         delete=permission['delete'],
        #     ))

        # db.add_all(new_permissions)  # Bulk insert for efficiency
        # db.commit()

        return data
