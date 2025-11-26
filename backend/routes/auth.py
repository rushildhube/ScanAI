from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, validator
from pymongo.results import InsertOneResult
from bson import ObjectId
from config.database import db
from auth.jwt_handler import signJWT, decodeJWT
from auth.oauth_handlers import oauth, handle_oauth_callback
import secrets
import re
from datetime import datetime
from typing import Optional

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    mobile: Optional[str] = None
    sex: Optional[str] = None

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name is required')
        if len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()

    @validator('password')
    def validate_password(cls, v):
        if not v or not v.strip():
            raise ValueError('Password is required')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

    @validator('email')
    def validate_email(cls, v):
        if not v or not v.strip():
            raise ValueError('Email is required')
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower().strip()

    @validator('age')
    def validate_age(cls, v):
        if v is not None and (v < 0 or v > 150):
            raise ValueError('Age must be between 0 and 150')
        return v

    @validator('mobile')
    def validate_mobile(cls, v):
        if v and not re.match(r'^[\+]?[1-9][\d]{0,15}$', v.replace(' ', '').replace('-', '')):
            raise ValueError('Invalid mobile number format')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not v or not v.strip():
            raise ValueError('Email is required')
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower().strip()

    @validator('password')
    def validate_password(cls, v):
        if not v or not v.strip():
            raise ValueError('Password is required')
        return v

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decode and validate token
        payload = decodeJWT(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        user = await db.db["users"].find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if account is still active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is not active. Contact support.",
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    try:
        user_collection = db.db["users"]
        
        # Check if user already exists
        existing_user = await user_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(
                status_code=400, 
                detail="User already exists. Please log in."
            )

        # Hash password
        password_hash = pwd_context.hash(user.password)
        
        # Prepare user data
        user_data = user.dict()
        user_data["password_hash"] = password_hash
        del user_data["password"]
        user_data["auth_provider"] = "email"
        user_data["is_active"] = True
        user_data["created_at"] = datetime.now()
        user_data["last_login"] = None

        # Create user account
        result: InsertOneResult = await user_collection.insert_one(user_data)
        if not result.inserted_id:
            raise HTTPException(
                status_code=500, 
                detail="Unable to create account. Please try again later."
            )
        
        user_id = str(result.inserted_id)
        return {
            "message": "User registered successfully", 
            "access_token": signJWT(user_id)["access_token"],
            "user_id": user_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Something went wrong. Please try again."
        )

@router.post("/login")
async def login(user: UserLogin):
    try:
        user_collection = db.db["users"]
        user_db = await user_collection.find_one({"email": user.email})
        
        # Check if user exists
        if not user_db:
            raise HTTPException(
                status_code=404, 
                detail="User not found. Please sign up first."
            )
        
        # Check if account is active
        if not user_db.get("is_active", True):
            raise HTTPException(
                status_code=403, 
                detail="Account is not active. Contact support."
            )
        
        # Verify password
        if not pwd_context.verify(user.password, user_db["password_hash"]):
            raise HTTPException(
                status_code=401, 
                detail="Incorrect password. Please try again."
            )
        
        # Update last login
        await user_collection.update_one(
            {"_id": user_db["_id"]}, 
            {"$set": {"last_login": datetime.now()}}
        )
        
        return {
            "message": "Login successful", 
            "access_token": signJWT(str(user_db["_id"]))["access_token"],
            "user_id": str(user_db["_id"])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Something went wrong. Please try again."
        )

@router.get("/google")
async def google_login(request: Request):
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback", name="google_callback")
async def google_callback(request: Request):
    return await handle_oauth_callback('google', request)

@router.get("/facebook")
async def facebook_login(request: Request):
    redirect_uri = request.url_for('facebook_callback')
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

@router.get("/facebook/callback", name="facebook_callback")
async def facebook_callback(request: Request):
    return await handle_oauth_callback('facebook', request)

@router.get("/me")
async def get_user_profile(user: dict = Depends(get_current_user)):
    user["_id"] = str(user["_id"])
    del user["password_hash"]
    return user

@router.post("/logout")
async def logout(user: dict = Depends(get_current_user)):
    try:
        # In a real application, you might want to:
        # 1. Add the token to a blacklist
        # 2. Update user's last logout time
        # 3. Clear any server-side sessions
        
        user_collection = db.db["users"]
        await user_collection.update_one(
            {"_id": ObjectId(user["_id"])}, 
            {"$set": {"last_logout": datetime.now()}}
        )
        
        return {"message": "You have successfully logged out."}
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Logout failed. Please try again."
        )

@router.get("/check-session")
async def check_session(user: dict = Depends(get_current_user)):
    """Check if user session is valid"""
    return {
        "valid": True,
        "user_id": str(user["_id"]),
        "email": user["email"],
        "message": "Session is valid"
    }
