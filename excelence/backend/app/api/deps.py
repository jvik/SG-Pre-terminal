from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app import models
from app.db.session import supabase

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

def get_current_user(token: str = Depends(reusable_oauth2)) -> models.User:
    try:
        user = supabase.auth.get_user(token).user
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Adapt the Supabase user model to your internal models.User
        return models.User(id=user.id, email=user.email, is_active=True)
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user