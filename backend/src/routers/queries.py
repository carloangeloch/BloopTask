from sqlmodel import Session, select
from fastapi import Depends

from models.team import Team
from models.user import User

from lib.db import engine


def get_session():
    with Session(engine) as session:
        yield session

def get_team_by_urlname(urlname: str, session: Session = Depends(get_session)):
    """
        Returns Team model result using urlname
    """
    team_statement = select(Team).where(Team.urlname == urlname)
    team = session.exec(team_statement).first()
    return team

def get_user_by_email(email: str, session: Session = Depends(get_session)):
    """
        Returns User model result using email
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user