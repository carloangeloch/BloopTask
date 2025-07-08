from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class CreateTask(BaseModel):
        title: str
        description: str
        assinged_to: List[int]
        start_date: datetime
        due_date: datetime
        priority: str

class GetTasks(BaseModel):
        id: int
        title: str
        description: str
        created_by: int
        assinged_to: List[int]
        created_at: datetime
        start_date: datetime
        due_date: datetime
        priority: str
        position: int

        model_config = ConfigDict(from_attributes=True)

class UpdateTask(BaseModel):
        title: str
        description: str
        assinged_to: List[int]
        start_date: datetime
        due_date: datetime
        priority: str
        position: int
        