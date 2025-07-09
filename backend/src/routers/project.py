from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from datetime import datetime
from typing import List, Dict
import json

from lib.jwt import verify_token
from lib.responses import create_response
from models.project import Project
from serializers.project import CreateProject, GetProjectList
from .queries import get_session, get_team_by_urlname, get_user_by_email, get_role_by_teamid_id, get_project_by_teamid_pid

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
            return create_response('error', 'Invalid user', 401)
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        role = get_role_by_teamid_id(payload['role_id'],team.id, session)
        if role.name != 'admin':
            return create_response('error', 'Access Denied', 401)
        #check if project name exists in the team"
        project_statement = select(Project).where(Project.team_id == team_id, Project.name == data.name)
        project = session.exec(project_statement).first()
        if project:
            return create_response('error','Project already exists', 400)
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
        return create_response('success', f"New project has been created in {team.name}", 201)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
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
            return create_response('error', 'Invalid user', 401)
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        #get projects where is in team
        project_statement = select(Project).where(Project.team_id == team.id)
        projects = session.exec(project_statement).all()
        project_json: List[Dict] = [
            json.loads(GetProjectList.model_validate(project).model_dump_json())
            for project in projects
        ]
        return create_response('data', project_json, 200)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting all project', 500)

@router.get('/{pid}/{team_id}/')
async def get_project(team_id: str, pid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user token is same with the registered user
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Invalid user', 401)
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return create_response('error', 'No project found', 404)
        project_json = json.loads(GetProjectList.model_validate(project).model_dump_json())
        return create_response('data', project_json, 200)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
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
            return create_response('error', 'Invalid user', 401)
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return create_response('error', 'No project found', 404)
        #check if user is admin or moderator
        role = get_role_by_teamid_id(payload['role_id'],team.id, session)
        if role.name != 'admin':
            return create_response('error', 'Access Denied', 401)
        project.name = data.name
        project.description = data.description

        session.add(project)
        session.commit()
        session.refresh(project)
        return create_response('success', f"Project id numnber {pid} has been updated", 202)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
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
            return create_response('error', 'Invalid user', 401)
        #check if team exists
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return create_response('error', 'No project found', 404)
        #check if user is admin or moderator
        role = get_role_by_teamid_id(payload['role_id'],team.id, session)
        if role.name != 'admin':
            return create_response('error', 'Access Denied', 401)
        session.delete(project)
        session.commit()
        return JSONResponse({"Success":f"Project id numnber {pid} has been deleted"}, status_code=status.HTTP_202_ACCEPTED)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on deleting single project', 500)