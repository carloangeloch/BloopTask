from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from .enum import TaskPriorityEnum

if TYPE_CHECKING:
    from .user import User
    from .team import Team

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: Optional[int] = Field(foreign_key='team.id')
    name: str
    description: str
    created_by: Optional[int] = Field(foreign_key='user.id')
    created_at : datetime

    user: 'User' = Relationship(back_populates='project')
    team: 'Team' = Relationship(back_populates='project')
    #cascades
    tasklist: List['Tasklist'] = Relationship(back_populates='project', cascade_delete=True)

class Tasklist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: Optional[int] = Field(foreign_key='project.id')
    title: str
    description: str
    position: int

    project: 'Project' = Relationship(back_populates='tasklist')
    #cascades
    task: List['Task'] =Relationship(back_populates='tasklist', cascade_delete=True)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tasklist_id: Optional[int] = Field(foreign_key='tasklist.id')
    title: str
    description: str
    created_by: Optional[int] = Field(foreign_key='user.id')
    assinged_to: Optional[List[int]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime
    start_date: datetime
    due_date: datetime
    priority: TaskPriorityEnum = Field(default=TaskPriorityEnum.LOW)
    position: int

    user: Optional['User'] = Relationship(back_populates='task')
    tasklist: Optional['Tasklist'] = Relationship(back_populates='task') 
    #cascades
    taskcomment: List['TaskComment'] = Relationship(back_populates='task', cascade_delete=True)

class TaskComment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: Optional[int] = Field(foreign_key='task.id')
    user_id: Optional[int] = Field(foreign_key='user.id')
    comment: str
    created_at: datetime

    user: Optional['User'] = Relationship(back_populates='taskcomment')
    task: Optional['Task'] = Relationship(back_populates='taskcomment')
