from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.db.session import supabase
from gotrue.errors import AuthApiError

router = APIRouter()

# Pydantic models for request and response bodies
class ItemCreate(BaseModel):
    title: str
    description: str | None = None

class Item(BaseModel):
    id: int
    title: str
    description: str | None = None
    owner_id: str # Supabase uses UUIDs as strings

# Dependency to get the current user from the Supabase session
# NOTE: This is a simplified dependency. In a real app, you would
# likely have a more robust way to handle the JWT from the request header.
async def get_user(token: str):
    try:
        user = supabase.auth.get_user(token)
        return user
    except AuthApiError as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=Item)
def create_item(item: ItemCreate, user: dict = Depends(get_user)):
    """
    Create a new item for the current user.
    """
    try:
        # The user object from Supabase has a 'user' attribute
        # which contains the user details, including the id.
        owner_id = user.user.id
        data, count = supabase.table('items').insert({
            "title": item.title,
            "description": item.description,
            "owner_id": owner_id
        }).execute()
        
        # The data returned from insert is a list containing a dictionary
        created_item = data[1][0]
        return Item(
            id=created_item['id'],
            title=created_item['title'],
            description=created_item['description'],
            owner_id=str(created_item['owner_id'])
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Item])
def read_items(user: dict = Depends(get_user)):
    """
    Retrieve all items for the current user.
    """
    try:
        owner_id = user.user.id
        # RLS policy ensures users can only select their own items.
        data, count = supabase.table('items').select("*").eq('owner_id', owner_id).execute()
        return [Item(**item) for item in data[1]]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
