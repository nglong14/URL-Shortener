from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional
from .models import InterviewType

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    class Config():
        model_config = ConfigDict(from_attributes=True)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config():
        model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class InterviewBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=200)
    interview_type: InterviewType
    scheduled_at: datetime
    notes: Optional[str] = None
    location: Optional[str] = None

class InterviewCreate(InterviewBase):
    pass

class InterviewUpdate(BaseModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=200)
    interview_type: Optional[InterviewType] = None
    scheduled_at: Optional[datetime] = None
    notes: Optional[str] = None
    location: Optional[str] = None

class InterviewResponse(InterviewBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config():
        model_config = ConfigDict(from_attributes=True)
