from fastapi import APIRouter, Request, Depends
from sqlmodel import Session, select, desc
from .queries import get_session, get_user_by_email, get_team_by_urlname, get_project_by_teamid_pid, get_role_by_teamid_id
from lib.jwt import verify_token
from typing import List, Dict
import json

from models.project import Tasklist
from serializers.tasklist import CreateTasklist, GetTasklist, UpdateTasklist
from lib.responses import create_response

router = APIRouter()


@router.get('/up')
async def tasklist_up():
    return create_response('success', 'Tasklist API is working', 200)

@router.post('/create/{pid}/{team_id}')
async def create_tasklist(team_id: str,pid: int ,req: Request, data: CreateTasklist, session: Session = Depends(get_session)):
    try:
        #check if user is verified 
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Invalid User', 400)
        #check team based on team id
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        project = get_project_by_teamid_pid(team.id, pid, session)
        role = get_role_by_teamid_id(payload['role_id'],team.id, session)
        if role.name == 'member':
            return create_response('error', 'Access Denied', 401)
        if not project:
            return create_response('error', 'No project found', 404)
        tasklist_statement = select(Tasklist).where(Tasklist.project_id == pid).order_by(desc(Tasklist.position))
        tasklist = session.exec(tasklist_statement).first()
              
        new_tasklist = Tasklist(
              project_id=pid,
              title= data.title,
              description=data.description,
              position = tasklist.position+1 if tasklist else 0
        )
        
        session.add(new_tasklist)
        session.commit()
        session.refresh(new_tasklist)
        return create_response('success', f"New Tasklist is created on Project {project.name} at team {team.name}", 201)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on creating project tasklist', 500)
        
        
@router.get('/all/{pid}/{team_id}')
async def get_tasklists(team_id: str, pid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user is verified 
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Invalid User', 400)
        
        #check team based on team id
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return create_response('error', 'No project found', 404)
        tasklists = session.exec(select(Tasklist)).all()
        if not tasklists:
            return create_response('error', 'No tasklist found', 404)
        tasklist_json: List[Dict] = [
            json.loads(GetTasklist.model_validate(tasklist).model_dump_json())
            for tasklist in tasklists
        ]
        return create_response('data', tasklist_json, 200)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting all project tasklist', 500)
    
@router.get('/{tlid}/{pid}/{team_id}')
async def get_tasklist(team_id: str, pid: int, tlid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user is verified 
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Invalid User', 400)
        #check team based on team id
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return create_response('error', 'No project found', 404)
        tasklist_statement = select(Tasklist).where(Tasklist.id == tlid)
        tasklist = session.exec(tasklist_statement).first()
        if not tasklist:
            return create_response('error', 'No tasklist found', 404)
        tasklist_json= json.loads(GetTasklist.model_validate(tasklist).model_dump_json())
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
        return create_response('data', tasklist_json, 200)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting single project tasklist', 500)


@router.put('/{tlid}/{pid}/{team_id}')
async def update_tasklist(team_id: str, pid: int, tlid: int, data: UpdateTasklist, req:Request, session: Session = Depends(get_session)):
    try:
        #check if user is verified 
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Invalid User', 400)
        #check team based on team id
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        role = get_role_by_teamid_id(payload['role_id'],team.id, session)
        if role.name == 'member':
            return create_response('error', 'Access Denied', 401)
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return create_response('error', 'No project found', 404)
        tasklist_statement = select(Tasklist).where(Tasklist.id == tlid)
        tasklist = session.exec(tasklist_statement).first()
        if not tasklist:
            return create_response('error', 'No tasklist found', 404)
        tasklist.title = data.title
        tasklist.description = data.description
        tasklist.position = data.position
        session.add(tasklist)
        session.commit()
        session.refresh(tasklist)
        return create_response('success', f"Successfully updated tasklist {tlid} on project {pid} on team {team.name}", 202)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on updating tasklist', 500)

@router.delete('/{tlid}/{pid}/{team_id}')
async def delete_tasklist(team_id: str, pid: int, tlid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #check if user is verified 
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Invalid User', 400)
        #check team based on team id
        team = get_team_by_urlname(team_id, session)
        if not team:
            return create_response('error', 'No team found', 404)
        #check if team is token verified
        if payload['team_id'] != team.id:
            return create_response('error', 'Invalid user', 401)
        role = get_role_by_teamid_id(payload['role_id'],team.id, session)
        if role.name == 'member':
            return create_response('error', 'Access Denied', 401)
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return create_response('error', 'No project found', 404)
        tasklist_statement = select(Tasklist).where(Tasklist.id == tlid)
        tasklist = session.exec(tasklist_statement).first()
        if not tasklist:
            return create_response('error', 'No tasklist found', 404)
        session.delete(tasklist)
        session.commit()
        return create_response('success', 'Tasklist has been deleted', 202)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on deleting tasklist', 500)
