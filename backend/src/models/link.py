from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .team import Team, Roles


class UserTeamRoleLink(SQLModel, table=True):
    user_id : Optional[int] = Field(default=None, primary_key=True, foreign_key='user.id')
    team_id : Optional[int] = Field(default=None, primary_key=True, foreign_key='team.id')
    role_id : Optional[int] = Field(default=None, foreign_key='roles.id')

    user: Optional["User"] = Relationship(back_populates='team_link')
    team: Optional["Team"] = Relationship(back_populates='user_link')
    roles: Optional["Roles"] = Relationship(back_populates='user_team_link')

