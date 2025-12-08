from pydantic import BaseModel
import uuid

class CategoryBase(BaseModel):
    name: str
    emoji: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        from_attributes = True
