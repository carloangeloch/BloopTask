from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CreateTeam(BaseModel):
    name: str

class GetTeam(BaseModel):
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)