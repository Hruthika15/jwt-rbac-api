from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import User, UserCreate, UserLogin, Token
from database import get_session
from auth import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pw = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pw, role=user.role)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    token = create_access_token({"sub": new_user.username, "role": new_user.role})
    return Token(access_token=token)

@router.post("/login", response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user.username, "role": db_user.role})
    return Token(access_token=token)
