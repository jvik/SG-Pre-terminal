from pydantic import BaseModel, EmailStr
import uuid

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: uuid.UUID
    is_active: bool = True

    class Config:
        from_attributes = True
