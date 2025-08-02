from sqlmodel import SQLModel, Field
from typing import Optional

# User Table
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    role: str  # "admin" or "user"

# Input Models
class UserCreate(SQLModel):
    username: str
    password: str
    role: str

class UserLogin(SQLModel):
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Project Table
class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

# Input Model for Project
class ProjectCreate(SQLModel):
    name: str
    description: str
