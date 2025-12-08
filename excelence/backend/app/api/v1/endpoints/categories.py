from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.session import supabase
from app.api import deps
from app import models
import uuid

router = APIRouter()

# --- Pydantic Models ---
class CategoryCreate(BaseModel):
    name: str
    emoji: str | None = None

class CategoryUpdate(BaseModel):
    name: str
    emoji: str | None = None

class Category(BaseModel):
    id: uuid.UUID
    name: str
    emoji: str | None = None
    user_id: uuid.UUID

# --- API Endpoints ---
@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, user: models.User = Depends(deps.get_current_user)):
    """
    Create a new category for the current user.
    """
    try:
        user_id = user.id
        response = supabase.table('categories').insert({
            "name": category.name,
            "emoji": category.emoji,
            "user_id": str(user_id)
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create category.")

        created_category = response.data[0]
        return Category(
            id=created_category['id'],
            name=created_category['name'],
            emoji=created_category.get('emoji'),
            user_id=created_category['user_id']
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Category])
def read_categories(user: models.User = Depends(deps.get_current_user)):
    """
    Retrieve all categories for the current user.
    """
    try:
        user_id = user.id
        response = supabase.table('categories').select("*").eq('user_id', str(user_id)).order('name').execute()
        return [Category(**cat) for cat in response.data]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{category_id}", response_model=Category)
def update_category(category_id: uuid.UUID, category: CategoryUpdate, user: models.User = Depends(deps.get_current_user)):
    """
    Update a category for the current user.
    """
    try:
        user_id = user.id
        # RLS in Supabase should enforce ownership, but we double-check here.
        response = supabase.table('categories').update({
            "name": category.name,
            "emoji": category.emoji
        }).eq('id', str(category_id)).eq('user_id', str(user_id)).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Category not found or user does not have permission.")

        updated_category = response.data[0]
        return Category(**updated_category)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{category_id}", response_model=dict)
def delete_category(category_id: uuid.UUID, user: models.User = Depends(deps.get_current_user)):
    """
    Delete a category for the current user.
    Blocks deletion if the category is in use by any transactions.
    """
    try:
        user_id = user.id

        # Deletion Blocking Logic (Subtask 1.5)
        # Check if any transactions are using this category
        transaction_check = supabase.table('transactions').select('id', count='exact').eq('category_id', str(category_id)).eq('user_id', str(user_id)).execute()
        
        if transaction_check.count > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete category: It is currently in use by {transaction_check.count} transaction(s)."
            )

        # Proceed with deletion
        response = supabase.table('categories').delete().eq('id', str(category_id)).eq('user_id', str(user_id)).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Category not found or user does not have permission.")

        return {"detail": "Category deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
