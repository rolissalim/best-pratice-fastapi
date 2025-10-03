from sqlalchemy import Boolean, Column, DateTime, func, ForeignKey, Integer, String
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from app.config.database import Base
# from app.models.role_model import RoleHasMenu
from app.utils.util import get_local_time

class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    route = Column(String(150), nullable=False)
    icon = Column(String(50), nullable=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_group = Column(Boolean, default=False)
    parent_id = Column(Integer, ForeignKey('menus.id', use_alter=True, ondelete='SET NULL'), nullable=True)
    order = Column(Integer, nullable=True)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=get_local_time())
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    # Self-referencing relationship for nested menu structure
    parent = relationship('Menu', remote_side=[id], backref=backref('children', cascade='all, delete-orphan'))
    # roles = relationship('Role', secondary=RoleHasMenu.__table__, back_populates='menus')
    # role_permissions = relationship('RoleHasMenu', back_populates='menu')

    def __repr__(self):
        return f'<Menu(name={self.name}, route={self.route})>'