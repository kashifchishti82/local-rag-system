from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    token: str
