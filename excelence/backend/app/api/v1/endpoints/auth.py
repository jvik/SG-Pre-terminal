from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.db.session import supabase

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(user: UserCreate):
    """
    Create a new user.
    """
    try:
        res = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
        })
        
        # Supabase returns user without session when email confirmation is required
        # This is normal behavior for new users, not a duplicate
        return res
    except Exception as e:
        error_msg = str(e)
        # Check for common duplicate user error messages from Supabase
        if "already registered" in error_msg.lower() or "already exists" in error_msg.lower() or "user already registered" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists. Please log in or use a different email."
            )
        raise HTTPException(status_code=400, detail=error_msg)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return a token.
    """
    try:
        res = supabase.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password,
        })
        if res.session:
            return {
                "access_token": res.session.access_token,
                "token_type": "bearer"
            }
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

class ResendVerification(BaseModel):
    email: str

@router.post("/resend-verification")
def resend_verification(data: ResendVerification):
    """
    Resend verification email to the user.
    """
    try:
        res = supabase.auth.resend({
            "type": "signup",
            "email": data.email,
        })
        return {"message": "Verification email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))