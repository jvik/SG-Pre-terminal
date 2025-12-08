from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
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
        
        # Check if signup was successful
        # When a user already exists and email confirmations are enabled,
        # Supabase may return an empty user or specific identities
        if res.user:
            # Check if this is a fake confirmation (duplicate user)
            # Supabase returns identities[] only for real new signups or existing confirmed users
            identities = getattr(res.user, 'identities', None)
            if identities is not None and len(identities) == 0:
                # Empty identities array means user already exists but Supabase is hiding it
                raise HTTPException(
                    status_code=400,
                    detail="A user with this email already exists. Please log in or use a different email."
                )
        
        return res
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
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

@router.get("/callback")
def auth_callback():
    """
    Handle email verification callback from Supabase.
    Redirects to frontend with hash parameters preserved.
    """
    # Supabase will send the user here after email verification
    # We redirect to frontend which will handle the token in the hash
    return RedirectResponse(url="http://localhost:5173", status_code=307)