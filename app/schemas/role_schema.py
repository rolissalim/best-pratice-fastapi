from typing import Optional, TYPE_CHECKING
from app.base import BaseSchema
from app.schemas.schema import BaseResponseSchema
from pydantic import Field, field_validator, ValidationInfo
from app.models import Role

class RoleBaseSchema(BaseSchema):
    name: str
    description: Optional[str] = None    
    permissions: list = Field(..., exclude=True)
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "employee",
                "description": "ini deskripsi employee",
                "permissions": [{"menu_id":1, "create":1, "read":1, "update":1, "delete":1},{"menu_id":2, "create":1, "read":1, "update":1, "delete":1},]
            }
        }
    }
        
class RoleCreateSchema(RoleBaseSchema):
    created_by: Optional[str] = None

    
class RoleUpdateSchema(RoleCreateSchema):
    ...


class MenuPermission(BaseSchema):
    create: bool
    read: bool
    update: bool
    delete: bool

class MenuRead(BaseSchema):
    id: int
    name: str
    route: str
    icon: Optional[str] = None
    description: Optional[str] = None
    is_active: bool
    parent_id: Optional[int] = None
    is_group: bool
    children: list['MenuRead'] = []
    permissions: Optional[MenuPermission] = None

    @staticmethod
    def set_menu_permissions(menu: 'MenuRead', role_permissions: dict, role_menu_ids: set):
        """Sets permissions for a menu and filters children based on database entries."""
        # Set permissions for the current menu
        menu.permissions = role_permissions.get(menu.id)

        # Filter children that exist in role_menu_ids
        menu.children = [child for child in menu.children if child.id in role_menu_ids]

        # Recursively set permissions for each child
        for child in menu.children:
            MenuRead.set_menu_permissions(child, role_permissions, role_menu_ids)


class RoleReadSchema(BaseSchema):
    id: int
    name: str
    description: Optional[str] = None

class RoleWithMenuSchema(RoleReadSchema):
    menus: Optional[list[MenuRead]] = None

    @field_validator('menus', mode="before")
    def menus_parent(cls, v: Optional[list[MenuRead]], info: ValidationInfo) -> Optional[list[MenuRead]]:
        from app.dependency.deps import get_session
        db = next(get_session())

        role_id = info.data.get('id')  # Ambil role_id dari schema
        if v and role_id:
            # Ambil daftar menu yang sesuai dengan role_id dari database
            role_has_menus = Role.get_role_has_menu_by_role_and_menu(db, role_id)
            role_menu_ids = {role_has_menu.menu_id for role_has_menu in role_has_menus}

            # Mapping menu_id ke permissions
            menu_permissions = {
                role_has_menu.menu_id: MenuPermission(
                    create=role_has_menu.create,
                    read=role_has_menu.read,
                    update=role_has_menu.update,
                    delete=role_has_menu.delete
                )
                for role_has_menu in role_has_menus
            }

            # Filter hanya parent menu yang ada dalam role_menu_ids
            filtered_menus = [
                menu for menu in v if menu.parent_id is None and menu.id in role_menu_ids
            ]

            # Set permissions dan filter children
            for menu in filtered_menus:
                MenuRead.set_menu_permissions(menu, menu_permissions, role_menu_ids)

            return filtered_menus
        return v
