from pydantic import BaseModel, ConfigDict

class CreateTasklist (BaseModel):
    title: str
    description: str

class GetAllTasklist(BaseModel):
    project_id: int
    title: str
    description: str
    position: int

    model_config = ConfigDict(from_attributes=True)

class UpdateTasklist(BaseModel):
    title: str
    description: str
    position: int