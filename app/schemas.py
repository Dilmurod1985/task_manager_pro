from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ── User Schemas ─────────────────────────────────────────────────────────────

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # позволяет работать с ORM-моделями (SQLAlchemy)


# ── Task Schemas ─────────────────────────────────────────────────────────────

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: str = Field(default="pending", pattern="^(pending|in_progress|completed)$")


class TaskCreate(TaskBase):
    pass  # для создания — те же поля, что в базе


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TaskOut(TaskBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True