from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: constr(min_length=3, max_length=8)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    password: Optional[str] = None


class User(BaseModel):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
