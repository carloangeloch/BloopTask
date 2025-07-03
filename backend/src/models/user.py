from sqlmodel import SQLModel,Field, Relationship
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from .team import Team, Roles

class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str
    first_name: str
    middle_name: str
    last_name: str
    suffix: str
    team_id: int = Field(foreign_key='team.id', default=None)
    role_id: int = Field(foreign_key='roles.id', default=None)
    created_at: datetime = Field(default=datetime.now())

    team: Optional["Team"] = Relationship(back_populates='user')
    roles: Optional["Roles"] = Relationship(back_populates='user')
