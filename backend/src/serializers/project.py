from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CreateProject(BaseModel):
    name: str
    description: str

class GetProjectList(BaseModel):
    id: int
    name: str
    description: str
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
