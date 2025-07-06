from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from datetime import datetime
from typing import List, Dict
import json

from lib.jwt import verify_token
from models.team import Roles
from models.project import Project
from serializers.project import CreateProject, GetProjectList
from .queries import get_session, get_team_by_urlname, get_user_by_email

router  = APIRouter()

@router.get('/up')
async def auth_up():
    return JSONResponse({"Success":"Project API working"}, status_code=status.HTTP_200_OK)

#create project folder and default tasklist (Todo, Pending and Completed)
@router.post('/create/{team_id}')
async def create_project(team_id:str, req: Request,  data: CreateProject, session: Session = Depends(get_session)):
    try:
        #check if user token is same with the registered user
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return JSONResponse({"Error":"Invalid user"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            return JSONResponse({"Error":"No team found"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check if user is token verified
        if payload['team_id'] != team.id:
            return JSONResponse({"Error":"Invalid user"}, status_code=status.HTTP_400_BAD_REQUEST)
        role_statement = select(Roles).where(Roles.team_id == team.id, Roles.id == payload['role_id'])
        role = session.exec(role_statement).first()
        if role.name != 'admin':
            return JSONResponse({"Error":"Access Denied"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check if project name exists in the teawm"
        if team.name == data.name:
            return JSONResponse({"Error":"Project alreadt exist"}, status_code=status.HTTP_400_BAD_REQUEST)
        new_project = Project(
            team_id=team.id,
            name= data.name,
            description=data.description,
            created_by=user.id,
            created_at=datetime.now()
        )
        session.add(new_project)
        session.commit()
        session.refresh(new_project)
        return JSONResponse({"Success":f"New project has been created in {team.name}"}, status_code=status.HTTP_201_CREATED)
    except:
        return JSONResponse({"Error":"Error on creating project"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get('/all/{team_id}', response_model=List[GetProjectList])
async def get_projects(team_id:str, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user is verified 
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
                return JSONResponse({"Error":"Invalid user"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check team based on team id
        team = get_team_by_urlname(team_id, session)
        if not team:
            return JSONResponse({"Error":"No team found"}, status_code=status.HTTP_400_BAD_REQUEST)
        #get projects where is in team
        project_statement = select(Project).where(Project.team_id == team.id)
        projects = session.exec(project_statement).all()
        project_json: List[Dict] = [
            json.loads(GetProjectList.model_validate(project).model_dump_json())
            for project in projects
        ]
        return JSONResponse(project_json, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse({"Error":"Error on get all projects"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get('/{pid}/{team_id}/')
async def get_project(team_id: str, pid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user is verified 
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
                return JSONResponse({"Error":"Invalid user"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check team based on team id
        team = get_team_by_urlname(team_id, session)
        if not team:
            return JSONResponse({"Error":"No team found"}, status_code=status.HTTP_400_BAD_REQUEST)
        project_statement = select(Project).where(Project.team_id == team.id, Project.id == pid)
        project = session.exec(project_statement).first()
        if not project:
            return JSONResponse({"Error":"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)
        project_json = json.loads(GetProjectList.model_validate(project).model_dump_json())
        return JSONResponse(project_json, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse({"Error":"Error on get single project"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.put('/{pid}/{team_id}')
async def update_project(team_id: str, pid: int, req: Request, data: CreateProject, session: Session = Depends(get_session)):
    try:
        #check if user is verified 
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
                return JSONResponse({"Error":"Invalid user"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check team based on team id
        team = get_team_by_urlname(team_id, session)
        if not team:
            return JSONResponse({"Error":"No team found"}, status_code=status.HTTP_400_BAD_REQUEST)
        project_statement = select(Project).where(Project.team_id == team.id, Project.id == pid)
        project = session.exec(project_statement).first()
        if not project:
            return JSONResponse({"Error":"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)
        project.name = data.name
        project.description = data.description

        session.add(project)
        session.commit()
        session.refresh(project)
        return JSONResponse({"Success":f"Project id numnber {pid} has been updated"}, status_code=status.HTTP_202_ACCEPTED)
    except:
        return JSONResponse({"Error":"Error on get updating project"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.delete('/{pid}/{team_id}')
async def delete_project(team_id: str, pid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user is verified 
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
                return JSONResponse({"Error":"Invalid user"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check team based on team id
        team = get_team_by_urlname(team_id, session)
        if not team:
            return JSONResponse({"Error":"No team found"}, status_code=status.HTTP_400_BAD_REQUEST)
        project_statement = select(Project).where(Project.team_id == team.id, Project.id == pid)
        project = session.exec(project_statement).first()
        if not project:
            return JSONResponse({"Error":"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)
        session.delete(project)
        session.commit()
        return JSONResponse({"Success":f"Project id numnber {pid} has been deleted"}, status_code=status.HTTP_202_ACCEPTED)
        
    except:
        return JSONResponse({"Error":"Error on get deleting project"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)