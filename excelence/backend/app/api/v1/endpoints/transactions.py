from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from app.db.session import supabase
from app.api import deps
from app import crud, models
import uuid
from datetime import date

router = APIRouter()

# --- Pydantic Models ---
class TransactionCreate(BaseModel):
    amount: float
    type: str  # "income" or "expense"
    date: date
    description: Optional[str] = None
    category_id: uuid.UUID

class Transaction(BaseModel):
    id: uuid.UUID
    amount: float
    type: str
    date: date
    description: Optional[str] = None
    user_id: uuid.UUID
    category_id: uuid.UUID

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None  # "income" or "expense"
    date: Optional[str] = None  # Accept string in ISO format
    description: Optional[str] = None
    category_id: Optional[str] = None  # Accept string UUID

# --- API Endpoints ---
@router.get("/", response_model=List[Transaction])
def list_transactions(user: models.User = Depends(deps.get_current_user)):
    """
    Retrieve all transactions for the current user.
    """
    try:
        user_id = user.id
        response = supabase.table('transactions').select('*').match({
            'user_id': str(user_id)
        }).order('date', desc=True).execute()

        if not response.data:
            return []

        return [Transaction(**t) for t in response.data]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(transaction_id: uuid.UUID, transaction: TransactionUpdate, user: models.User = Depends(deps.get_current_user)):
    """
    Update a transaction for the current user.
    """
    try:
        user_id = user.id
        update_data = transaction.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided.")

        response = supabase.table('transactions').update(update_data).match({
            'id': str(transaction_id),
            'user_id': str(user_id)
        }).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Transaction not found or user does not have permission.")

        updated_transaction = response.data[0]
        return Transaction(**updated_transaction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=Transaction)
def create_transaction(transaction: TransactionCreate, user: models.User = Depends(deps.get_current_user)):
    """
    Create a new transaction for the current user.
    """
    try:
        user_id = user.id
        response = supabase.table('transactions').insert({
            "amount": transaction.amount,
            "type": transaction.type,
            "date": str(transaction.date),
            "description": transaction.description,
            "category_id": str(transaction.category_id),
            "user_id": str(user_id)
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create transaction.")

        created_transaction = response.data[0]
        return Transaction(**created_transaction)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{transaction_id}", response_model=dict)
def delete_transaction(transaction_id: uuid.UUID, user: models.User = Depends(deps.get_current_user)):
    """
    Delete a transaction for the current user.
    """
    try:
        user_id = user.id
        success = crud.delete_transaction(transaction_id, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Transaction not found or user does not have permission.")

        return {"detail": "Transaction deleted successfully"}
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=str(e))
