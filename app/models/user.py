from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.user_role import UserRole
from app.models.role import Role


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True)
    full_name = Column(String(200), index=True)
    hashed_password = Column(String(200))
    is_active = Column(Boolean, default=True)
    roles = relationship("Role", secondary="user_role")

    def __init__(self, email, full_name, hashed_password):
        self.email = email
        self.full_name = full_name
        self.hashed_password = hashed_password
