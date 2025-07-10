from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from .link import UserTeamRoleLink

if TYPE_CHECKING:
    from .user import User
    from .project import Project

class Team(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    urlname: str
    created_at: datetime = Field(default=datetime.now())
    is_active: bool

    #cascades
    user_link: List["UserTeamRoleLink"] = Relationship(back_populates='team', cascade_delete=True)
    role : List['Roles'] = Relationship(back_populates='team', cascade_delete=True)
    project: List["Project"] = Relationship(back_populates='team', cascade_delete=True)

class Roles(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    team_id: Optional[int] = Field(foreign_key='team.id', default=None)

    user_team_link: List["UserTeamRoleLink"] = Relationship(back_populates='roles')
    team: Optional['Team'] = Relationship(back_populates='role')  