from sqlmodel import SQLModel,Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
from .link import UserTeamRoleLink

if TYPE_CHECKING:
    from .team import Team, Roles
    from .project import Project, Task, TaskComment


class User(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str
    first_name: str
    middle_name: str
    last_name: str
    suffix: str
    created_at: datetime = Field(default=datetime.now())

    team_link: List["UserTeamRoleLink"] = Relationship(back_populates='user')
    #cascades
    project: List["Project"] = Relationship(back_populates="user", cascade_delete=True)
    task: List['Task'] = Relationship(back_populates='user', cascade_delete=True)
    taskcomment: List['TaskComment'] = Relationship(back_populates='user', cascade_delete=True)
