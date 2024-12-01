from datetime import datetime
from pydantic import BaseModel
from enum import IntEnum


class Role(IntEnum):
    teacher = 1
    student = 2


class UserBase(BaseModel):
    email: str
    role: Role


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
