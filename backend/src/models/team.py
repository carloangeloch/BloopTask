from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime

if TYPE_CHECKING:
    from .user import User
    from .project import Project

class Team(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    urlname: str
    created_at: datetime = Field(default=datetime.now())

    #cascades
    roles: List["Roles"] = Relationship(back_populates="team", cascade_delete=True)
    user: List["User"] = Relationship(back_populates='team', cascade_delete=True)
    project: List["Project"] = Relationship(back_populates='team', cascade_delete=True)

class Roles(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    team_id: int = Field(foreign_key='team.id')

    team: Optional["Team"] = Relationship(back_populates='roles')
    user: Optional["User"] = Relationship(back_populates='roles')