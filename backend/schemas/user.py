from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str  # Use str instead of EmailStr to avoid needing email-validator
    password: str
    full_name: str
    department: Optional[str] = None
    semester: Optional[int] = None
    enrollment_number: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    department: Optional[str] = None
    semester: Optional[int] = None
    enrollment_number: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str
