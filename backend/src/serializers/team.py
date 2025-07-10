from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CreateTeam(BaseModel):
    name: str

class UpdateTeam(BaseModel):
    name: str
    is_active: bool

class GetTeam(BaseModel):
    name: str
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)