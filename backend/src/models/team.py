from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime

if TYPE_CHECKING:
    from .user import User

class Team(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    urlname: str
    created_at: datetime = Field(default=datetime.now())

    roles: List["Roles"] = Relationship(back_populates="team")
    user: List["User"] = Relationship(back_populates='team')

class Roles(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    team_id: int = Field(foreign_key='team.id')

    team: Optional["Team"] = Relationship(back_populates='roles')
    user: Optional["User"] = Relationship(back_populates='roles')