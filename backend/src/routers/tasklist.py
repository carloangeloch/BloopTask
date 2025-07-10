from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import Session, select, desc
from .queries import get_session, get_user_by_email, get_team_by_urlname, get_project_by_teamid_pid, get_role_by_teamid_roletype
from lib.jwt import verify_token
from typing import List, Dict
import json

from models.project import Tasklist
from models.link import UserTeamRoleLink
from serializers.tasklist import CreateTasklist, GetTasklist, UpdateTasklist
from lib.responses import create_response

router = APIRouter()


@router.get('/up')
async def tasklist_up():
    return create_response('success', 'Tasklist API is working', 200)

@router.post('/create/{pid}/{team_id}')
async def create_tasklist(team_id: str,pid: int ,req: Request, data: CreateTasklist, session: Session = Depends(get_session)):
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
        return create_response('success', f"New Tasklist is created on Project {project.name} at team {team.name}", 201)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on creating project tasklist', 500)
        
        
@router.get('/all/{pid}/{team_id}')
async def get_tasklists(team_id: str, pid: int, req: Request, session: Session = Depends(get_session)):
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
        user_team = session.exec(select(UserTeamRoleLink).where(UserTeamRoleLink.user == user, UserTeamRoleLink.team == team)).first()
        if not user_team:
            raise HTTPException(403, 'Acces Denied')
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            raise HTTPException(404, 'No project found')
        tasklists = session.exec(select(Tasklist).order_by(Tasklist.position)).all()
        if not tasklists:
            raise HTTPException(404, 'No tasklist found')
        tasklist_json: List[Dict] = [
            json.loads(GetTasklist.model_validate(tasklist).model_dump_json())
            for tasklist in tasklists
        ]
        return create_response('data', tasklist_json, 200)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting all project tasklist', 500)
    
@router.get('/{tlid}/{pid}/{team_id}')
async def get_tasklist(team_id: str, pid: int, tlid: int, req: Request, session: Session = Depends(get_session)):
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
        user_team = session.exec(select(UserTeamRoleLink).where(UserTeamRoleLink.user == user, UserTeamRoleLink.team == team)).first()
        if not user_team:
            raise HTTPException(403, 'Acces Denied')
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            raise HTTPException(404, 'No project found')
        tasklist = session.exec(select(Tasklist)).first()
        if not tasklist:
            raise HTTPException(404, 'No tasklist found')
        tasklist_json= json.loads(GetTasklist.model_validate(tasklist).model_dump_json())
        return create_response('data', tasklist_json, 200)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting single project tasklist', 500)


@router.put('/{tlid}/{pid}/{team_id}')
async def update_tasklist(team_id: str, pid: int, tlid: int, data: UpdateTasklist, req:Request, session: Session = Depends(get_session)):
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
        user_team = session.exec(select(UserTeamRoleLink).where(UserTeamRoleLink.user == user, UserTeamRoleLink.team == team, UserTeamRoleLink.roles == role)).first()
        if user_team:
            raise HTTPException(403, 'Acces Denied')
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            raise HTTPException(404, 'No project found')
        tasklist = session.exec(select(Tasklist).where(Tasklist.id == tlid)).first()
        print('tasklist', tasklist)
        if not tasklist:
            raise HTTPException(404, 'No tasklist found')
        current_position = tasklist.position 
        new_position = data.position
        if(current_position > new_position):
            tasklists_shift = session.exec(
                select(Tasklist).where(
                    Tasklist.position >= new_position,
                    Tasklist.position < current_position,
                    Tasklist.project_id == project.id
            )).all()
            for t in tasklists_shift:
                t.position += 1
                session.add(t)
        elif (current_position < new_position):
            print('moving down')
            tasklists_shift = session.exec(
                select(Tasklist).where(
                    Tasklist.position <= new_position,
                    Tasklist.position > current_position,
                    Tasklist.project_id == project.id
            )).all()
            for t in tasklists_shift:
                t.position -= 1
                session.add(t)
        tasklist.position = data.position
        tasklist.title = data.title
        tasklist.description = data.description
        session.add(tasklist)
        session.commit()
        return create_response('success', f"Successfully updated tasklist {tlid} on project {pid} on team {team.name}", 202)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on updating tasklist', 500)

@router.delete('/{tlid}/{pid}/{team_id}')
async def delete_tasklist(team_id: str, pid: int, tlid: int, req: Request, session: Session = Depends(get_session)):
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
        user_team = session.exec(select(UserTeamRoleLink).where(UserTeamRoleLink.user == user, UserTeamRoleLink.team == team, UserTeamRoleLink.roles == role)).first()
        if user_team:
            raise HTTPException(403, 'Acces Denied')
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            raise HTTPException(404, 'No project found')
        tasklist = session.exec(select(Tasklist).where(Tasklist.id == tlid)).first()
        if not tasklist:
            raise HTTPException(404, 'No tasklist found')
        #once task list is deleted, all preceeding positions should be move back
        tasklist_shift = session.exec(select(Tasklist).where(
            Tasklist.position > tasklist.position ,
            Tasklist.project_id == project.id
        )).all()
        print(tasklist_shift)
        for t in tasklist_shift:
            t.position -= 1
            session.commit()

        session.delete(tasklist)
        session.commit()
        return create_response('success', 'Tasklist has been deleted', 202)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on deleting tasklist', 500)
