from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select, desc
from .queries import get_session, get_user_by_email, get_team_by_urlname, get_project_by_teamid_pid
from lib.jwt import verify_token
from typing import List, Dict
import json

from models.project import Project, Tasklist
from models.team import Team, Roles
from models.user import User
from serializers.tasklist import CreateTasklist, GetAllTasklist, UpdateTasklist

router = APIRouter()


@router.get('/up')
async def tasklist_up():
    return JSONResponse({"Success":"Tasklist API is working"}, status_code=status.HTTP_200_OK)

@router.post('/create/{pid}/{team_id}')
async def create_tasklist(team_id: str,pid: int ,req: Request, data: CreateTasklist, session: Session = Depends(get_session)):
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
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return JSONResponse({"Error":"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)
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
        return JSONResponse({"Success":f"New Tasklist is created on Project {project.name} at team {team.name}"}, status_code=status.HTTP_201_CREATED)
    except:
         return JSONResponse({"Error":"Error on creating project tasklist"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@router.get('/all/{pid}/{team_id}')
async def get_tasklists(team_id: str, pid: int, req: Request, session: Session = Depends(get_session)):
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
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return JSONResponse({"Error":"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)
        tasklists = session.exec(select(Tasklist)).all()
        if not tasklists:
            return JSONResponse({"Error":"No tasklist available"}, status_code=status.HTTP_400_BAD_REQUEST)
        tasklist_json: List[Dict] = [
            json.loads(GetAllTasklist.model_validate(tasklist).model_dump_json())
            for tasklist in tasklists
        ]
        return JSONResponse(tasklist_json, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse({"Error":"Error on getting all project tasklist"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.get('/{tlid}/{pid}/{team_id}')
async def get_tasklist(team_id: str, pid: int, tlid: int, req: Request, session: Session = Depends(get_session)):
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
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return JSONResponse({"Error":"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)
        tasklist_statement = select(Tasklist).where(Tasklist.id == tlid)
        tasklist = session.exec(tasklist_statement).first()
        if not tasklist:
            return JSONResponse({"Error":"No tasklist available"}, status_code=status.HTTP_400_BAD_REQUEST)
        tasklist_json= json.loads(GetAllTasklist.model_validate(tasklist).model_dump_json())
        return JSONResponse(tasklist_json, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse({"Error":"Error on getting single project tasklist"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{tlid}/{pid}/{team_id}')
async def update_tasklist(team_id: str, pid: int, tlid: int, data: UpdateTasklist, req:Request, session: Session = Depends(get_session)):
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
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return JSONResponse({"Error":"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)
        tasklist_statement = select(Tasklist).where(Tasklist.id == tlid)
        tasklist = session.exec(tasklist_statement).first()
        if not tasklist:
            return JSONResponse({"Error":"No tasklist available"}, status_code=status.HTTP_400_BAD_REQUEST)
        tasklist.title = data.title
        tasklist.description = data.description
        tasklist.position = data.position
        session.add(tasklist)
        session.commit()
        session.refresh(tasklist)
        return JSONResponse({"Success":f"Successfully updated tasklist {tlid} on project {pid} on team {team.name}"}, status_code=status.HTTP_202_ACCEPTED)
    except:
        return JSONResponse({"Error":"Error on updating tasklist"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete('/{tlid}/{pid}/{team_id}')
async def delete_tasklist(team_id: str, pid: int, tlid: int, req: Request, session: Session = Depends(get_session)):
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
        project = get_project_by_teamid_pid(team.id, pid, session)
        if not project:
            return JSONResponse({"Error":"No project found"}, status_code=status.HTTP_400_BAD_REQUEST)
        tasklist_statement = select(Tasklist).where(Tasklist.id == tlid)
        tasklist = session.exec(tasklist_statement).first()
        if not tasklist:
            return JSONResponse({"Error":"No tasklist available"}, status_code=status.HTTP_400_BAD_REQUEST)
        session.delete(tasklist)
        session.commit()
    except:
        return JSONResponse({"Error":"Error on deletting tasklist"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
