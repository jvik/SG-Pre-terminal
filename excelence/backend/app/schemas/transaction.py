from pydantic import BaseModel
import uuid
from datetime import date

class TransactionBase(BaseModel):
    amount: float
    type: str
    date: date
    description: str | None = None
    category_id: uuid.UUID

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        from_attributes = True
