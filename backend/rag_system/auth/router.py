from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ..db import get_db
from . import service
from .models import (
    UserCreate,
    User,
    Token,
    LoginRequest,
    RefreshTokenRequest,
    LogoutRequest
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return service.create_user(db, user)

@router.post("/login", response_model=Token)
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    user = service.authenticate_user(db, login.email, login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: RefreshTokenRequest, db: Session = Depends(get_db)):
    # TODO: Implement refresh token logic
    pass

@router.post("/logout")
def logout(token: LogoutRequest, db: Session = Depends(get_db)):
    # TODO: Implement logout logic with token blacklisting
    return {"detail": "Successfully logged out"}

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(service.get_current_active_user)):
    return current_user
