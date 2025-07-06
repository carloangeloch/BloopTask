from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from datetime import datetime

from lib.jwt import verify_token
from lib.db import engine
from models.user import User
from models.team import Team, Roles
from models.project import Project
from serializers.project import CreateProject
from .queries import get_session, get_team_by_urlname

router  = APIRouter()

@router.get('/up')
async def auth_up():
    return JSONResponse({"Success":"Project API working"}, status_code=status.HTTP_200_OK)

# async def get_team(payload):
    

#create project folder and default tasklist (Todo, Pending and Completed)
@router.post('/create/{team_id}')
async def create_project(team_id:str, req: Request, data: CreateProject, payload = Depends(verify_token), session: Session = Depends(get_session)):
    try:
        #check if team exists
        team = get_team_by_urlname(team_id)
        if not team:
            return JSONResponse({"Error":"No team found"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check if user is token verified
        if payload['team_id'] != team.id:
            return JSONResponse({"Error":"Invalid user"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check if user token is same with the registered user
        user_statement = select(User).where(User.email == payload['email'])
        user = session.exec(user_statement).first()
        if not user:
            return JSONResponse({"Error":"Invalid user"}, status_code=status.HTTP_400_BAD_REQUEST)
        role_statement = select(Roles).where(Roles.team_id == team.id, Roles.id == payload['role_id'])
        role = session.exec(role_statement).first()
        if role.name != 'admin':
            return JSONResponse({"Error":"Access Denied"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check if project name exists in the team"
        if team.name == data.name:
            return JSONResponse({"Error":"Project alreadt exist"}, status_code=status.HTTP_400_BAD_REQUEST)
        new_project = Project(
            team_id=team.id,
            name= data.name,
            description=data.description,
            created_by=user.id,
            created_at=datetime
        )
        session.add(new_project)
        session.commit()
        session.refresh(new_project)
        return JSONResponse({"Success":f"New project has been created in {team.name}"}, status_code=status.HTTP_201_CREATED)
    except:
        return JSONResponse({"Error":"Error on creating project"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @router.get('/all/{team_id}')
# async def get_projects(team_id:str, payload=Depends(verify_token)):
    

#crud new tasklist 

#crud new Task

#crud new taskcomment