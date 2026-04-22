from pydantic import BaseModel, EmailStr, validator, Field
from datetime import datetime
from typing import Optional
from typing import List


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str

    @validator("password")
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v



class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class PostCreate(BaseModel):
    title: str
    status: str
    content: str

class UserData(BaseModel):
    id: int
    full_name: str
    email: str


class PostResponse(BaseModel):
    id: int
    title: str
    status: str
    content: str
    is_active: bool
    created_at: datetime
    user: UserData

    class Config:
        from_attributes = True



class LoginRequest(BaseModel):
    email: EmailStr
    password: str

