from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = False
    recurrence_rule: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_rule: Optional[str] = None


class TaskRead(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    status: str
    priority: Optional[str]
    tags: Optional[str]
    due_date: Optional[datetime]
    is_recurring: bool
    recurrence_rule: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
