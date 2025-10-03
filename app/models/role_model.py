from sqlalchemy import Boolean, Column, DateTime, func, ForeignKey, Integer, String, JSON
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import relationship, Session
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

# from app.utils.util import get_local_time
# from typing import Optional

# class RoleHasMenu(Base):
#     __tablename__ = 'role_has_menus'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'))
#     menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'))
#     read = Column(Boolean, default=False)
#     create = Column(Boolean, default=False)
#     update = Column(Boolean, default=False)
#     delete = Column(Boolean, default=False)
#     updated_at = Column(DateTime, nullable=True, default=None, onupdate=get_local_time())
#     created_at = Column(DateTime, nullable=False, server_default=func.now())

#     def __repr__(self):
#         return f'<RoleHasMEnu(id={self.id}, menu_id={self.menu_id})>'

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False,unique=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    # user = relationship("User", uselist=False, primaryjoin="User.role_id == Role.id") #Kalau benar-benar butuh one-to-one (jarang kasusnya di Role-User),
    users = relationship("User", back_populates="role")  

    # menus = relationship('Menu', secondary=RoleHasMenu.__table__, back_populates='roles')
    # New relationship with RoleHasMenu to access permissions
    # permissions = relationship('RoleHasMenu', backref='role', lazy='joined')

    @classmethod
    def get_role_by_id(cls, id: int, db: Session) -> "Role":
        return db.query(Role).filter(Role.id == id).first()
    
    @classmethod
    def validate_role_id(cls, id, db_session):
        if not Role.get_role_by_id(id, db_session):
            raise HTTPException(status_code=404, detail="Role ID does not exist")

    # @staticmethod  # <-- Tambahkan decorator ini
    # def get_role_has_menu_by_role_and_menu(db: Session, role_id: int, menu_id: Optional[int] = None):
    #     query = db.query(RoleHasMenu).filter(RoleHasMenu.role_id == role_id)
    #     if menu_id is not None:
    #         query = query.filter(RoleHasMenu.menu_id == menu_id)
    #     return query.all()
    
    def __repr__(self):
        return f'<Role(id={self.id}>'
