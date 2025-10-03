from sqlalchemy import Column, DateTime,  ForeignKey, func, String, Integer
from datetime import datetime
from sqlalchemy.orm import relationship, Session
from app.config.database import Base
import uuid
from sqlalchemy import or_
import pytz
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = 'users'
  # Di bagian import

# Di model User dan UserToken
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(100),nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=True)
    # created_at = Column(DateTime, nullable=False,oncreate=datetime.now(pytz.timezone('Asia/Jakarta')))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now(pytz.timezone('Asia/Jakarta')))
    tokens = relationship("UserToken", back_populates="user")
    role = relationship("Role", back_populates="users")
    
    @classmethod
    def check_user_login(cls, username: str, db: Session) -> "User":
        return db.query(User).filter(or_(User.email == username)).first()

class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="tokens")