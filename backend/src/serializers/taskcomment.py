from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CreateTaskComment(BaseModel):
    comment:str

class GetComment(BaseModel):
    id: int
    task_id: int
    user_id: int
    comment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
