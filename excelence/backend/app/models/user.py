from pydantic import BaseModel, EmailStr
import uuid
from typing import Optional

class User(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool = True
    access_token: Optional[str] = None  # JWT token for RLS
