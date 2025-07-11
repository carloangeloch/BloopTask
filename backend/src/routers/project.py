from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
from typing import List, Dict
import json

from lib.jwt import verify_token
from lib.responses import create_response
from models.project import Project, Tasklist
from models.link import UserTeamRoleLink
from serializers.project import CreateProject, GetProjectList
from .queries import get_session, get_team_by_urlname, get_user_by_email, get_project_by_teamid_pid, get_role_by_teamid_roletype

router  = APIRouter()

@router.get('/up')
async def auth_up():
    return create_response('success', "Project API working", 200)

#create project folder and default tasklist (Todo, Pending and Completed)
@router.post('/create/{team_id}')
async def create_project(team_id:str, req: Request,  data: CreateProject, session: Session = Depends(get_session)):
    try:
        #check if user token is same with the registered user
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException(401, 'Invalid user')
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            raise HTTPException(404, 'No team found')
        #validate if user is admin and is in team
        role = get_role_by_teamid_roletype(team.id, 'admin', session)
        user_team = session.exec(select(UserTeamRoleLink).where(UserTeamRoleLink.user == user, UserTeamRoleLink.team == team , UserTeamRoleLink.roles == role)).first()
        if not user_team:
            raise HTTPException(403, 'Acces Denied')
        #check if project name exists in the team"
        project_statement = select(Project).where(Project.team_id == team.id, Project.name == data.name)
        project = session.exec(project_statement).first()
        if project:
            raise HTTPException(404, 'Project already exists')
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

        new_task_todo = Tasklist(
            project_id = new_project.id,
            title = 'Pending',
            description = 'Tasks that are needed to be done',
            position = 0
        )
        new_task_ongoing = Tasklist(
            project_id = new_project.id,
            title = 'Ongoing',
            description = 'Tasks that are currently working with',
            position = 1
        )
        new_task_completed = Tasklist(
            project_id = new_project.id,
            title = 'Completed',
            description = 'Tasks that are done',
            position = 2
        )
        session.add_all([new_task_todo, new_task_ongoing, new_task_completed])
        session.commit()
        return create_response('success', f"New project has been created in {team.name}", 201)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on creating project', 500)

@router.get('/all/{team_id}')
async def get_projects(team_id:str, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user token is same with the registered user
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException(401, 'Invalid user')
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            raise HTTPException(404, 'No team found')
        #validate is user is under the team
        user_team = session.exec(select(UserTeamRoleLink).where(UserTeamRoleLink.team == team, UserTeamRoleLink.user == user)).first()
        if not user_team:
            raise HTTPException(400, 'User is not in the team')
        #get projects where is in team
        project_statement = select(Project).where(Project.team_id == team.id)
        projects = session.exec(project_statement).all()
        project_json: List[Dict] = [
            json.loads(GetProjectList.model_validate(project).model_dump_json())
            for project in projects
        ]
        return create_response('data', project_json, 200)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting all project', 500)

@router.get('/{pid}/{team_id}')
async def get_project(team_id: str, pid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user token is same with the registered user
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException(401, 'Invalid User')
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            raise HTTPException(404, 'No team found')
        #validate is user is under the team
        user_team = session.exec(select(UserTeamRoleLink).where(UserTeamRoleLink.team == team, UserTeamRoleLink.user == user)).first()
        if not user_team:
            raise HTTPException(400, 'User is not in the team')
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            raise HTTPException(404, 'No project found')
        project_json = json.loads(GetProjectList.model_validate(project).model_dump_json())
        return create_response('data', project_json, 200)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting single project', 500)
    
@router.put('/{pid}/{team_id}')
async def update_project(team_id: str, pid: int, req: Request, data: CreateProject, session: Session = Depends(get_session)):
    try:
        #check if user token is same with the registered user
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException(401, 'Invalid User')
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            raise HTTPException(404, 'No team found')
        #validate if user is not member and is in team
        role = get_role_by_teamid_roletype(team.id, 'member', session)
        user_team = session.exec(select(UserTeamRoleLink).where(UserTeamRoleLink.user == user, UserTeamRoleLink.team == team , UserTeamRoleLink.roles == role)).first()
        if user_team:
            raise HTTPException(403, 'Acces Denied')
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            raise HTTPException(404, 'No project found')
        project.name = data.name
        project.description = data.description

        session.add(project)
        session.commit()
        return create_response('success', f"Project id numnber {pid} has been updated", 202)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on updating single project', 500)
    
@router.delete('/{pid}/{team_id}')
async def delete_project(team_id: str, pid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user token is same with the registered user
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException(401, 'Invalid User')
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            raise HTTPException(404, 'No team found')
        #validate if user is not member and is in team
        role = get_role_by_teamid_roletype(team.id, 'admin', session)
        user_team = session.exec(select(UserTeamRoleLink).where(UserTeamRoleLink.user == user, UserTeamRoleLink.team == team , UserTeamRoleLink.roles == role)).first()
        if not user_team:
            raise HTTPException(403, 'Acces Denied')
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            raise HTTPException(404, 'No project found')
        session.delete(project)
        session.commit()
        return create_response('success', f"Project id numnber {pid} has been deleted", 202)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on deleting single project', 500)