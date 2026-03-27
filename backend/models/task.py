from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING

class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    result: Optional[Dict[str, Any]]
    error: Optional[str]
