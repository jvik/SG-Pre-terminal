from pydantic import BaseModel, EmailStr
import uuid

class User(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool = True
