from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    target_date: datetime
    is_completed: bool


class TaskPOST(BaseModel):
    title: str
    target_date: datetime


class TaskPatch(BaseModel):
    task_id: int
    title: Optional[str] = None
    target_date: Optional[datetime] = None
    is_completed: Optional[bool] = None


class TaskDelete(BaseModel):
    task_id: int
