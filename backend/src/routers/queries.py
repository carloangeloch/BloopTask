from sqlmodel import Session, select
from fastapi import Depends

from models.team import Team
from models.user import User
from models.project import Project, Tasklist

from lib.db import engine


def get_session():
    with Session(engine) as session:
        yield session

def get_team_by_urlname(urlname: str, session: Session):
    """
        Returns Team model result using urlname
    """
    team_statement = select(Team).where(Team.urlname == urlname)
    team = session.exec(team_statement).first()
    return team

def get_user_by_email(email: str, session: Session):
    """
        Returns User model result using email
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user

def get_project_by_teamid_pid(teamid:int, pid: int, session: Session):
    """
        Returns Project model result using project id and team id\n
        team id = team.id \n
        pid = project_id
    """
    project_statement = select(Project).where(Project.team_id == teamid, Project.id == pid)
    project = session.exec(project_statement).first()
    return project

def get_tasklist_by_tlid(tlid: int, session: Session):
    """
        Returns Tasklist model result using tasklist id
    """
    tasklist_statement = select(Tasklist).where(Tasklist.id == tlid)
    tasklist = session.exec(tasklist_statement).first()
    return tasklist