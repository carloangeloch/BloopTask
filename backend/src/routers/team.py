from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime
import os
import json

from lib.responses import create_response
from lib.jwt import verify_token
from .queries import get_session, get_user_by_email, get_team_by_urlname
from models.team import Team, Roles
from models.enum import UserRoleEnum
from models.link import UserTeamRoleLink
from serializers.team import CreateTeam, GetTeam, UpdateTeam

router = APIRouter()

@router.get('/up')
async def team_up():
    return create_response('success', 'Team API working', 200)

#any user can create their own team as admin

@router.post('/create')
async def create_taem(req: Request, data: CreateTeam, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException(401, 'Invalid User')
        lookup_string = data.name.lower().strip().replace(' ','-')
        team = session.exec(select(Team).where(Team.urlname.contains(lookup_string))).first()
        if team:
            raise HTTPException(400,'Team name exists')
        new_team = Team(
            name = data.name,
            urlname=lookup_string+ '-' + os.urandom(8).hex(),
            created_at=datetime.now(),
            is_active=True
        )
        session.add(new_team)
        session.commit()
        session.refresh(new_team)

        new_role_admin = Roles(
            name = UserRoleEnum.ADMIN.value,
            team_id = new_team.id
        )
        new_role_mod = Roles(
            name = UserRoleEnum.MODERATOR.value,
            team_id = new_team.id
        )
        new_role_member = Roles(
            name = UserRoleEnum.MEMBER.value,
            team_id = new_team.id
        )
        
        session.add_all([new_role_admin, new_role_member, new_role_mod])
        session.commit() 
        session.refresh(new_role_admin)

        new_link = UserTeamRoleLink(
            user = user,
            team = new_team,
            roles = new_role_admin
        )
        session.add(new_link)
        session.commit()
        return create_response('success', f'User {user.first_name} has created a new team', 201)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on creating team', 500)

@router.get('/all')
async def get_teams(req: Request, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException(401,'Invalid User')
        #get all team that the user is added to
        user_team_statement = select(UserTeamRoleLink).where(UserTeamRoleLink.user == user)
        user_team = session.exec(user_team_statement).all()
        teams = [team.team for team in user_team]
        team_json = [
            json.loads(GetTeam.model_validate(team).model_dump_json())
            for team in teams
        ]
        return create_response('data', team_json, 200)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting all teams', 500)
    
@router.get('/{team_id}')
async def get_team(team_id: str, req: Request, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException(401,'Invalid User')
        team = get_team_by_urlname(team_id, session)
        if not team:
            raise HTTPException(404, 'No teama found')
        user_team = session.exec(select(UserTeamRoleLink).where(
                UserTeamRoleLink.user == user, UserTeamRoleLink.team == team
            )).first()
        if not user_team:
            raise HTTPException(404, 'No team in user found')
        team_json = json.loads(GetTeam.model_validate(team).model_dump_json())
        return create_response('data', team_json, 200)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting single teams', 500)

@router.put('/{team_id}')
async def get_team(team_id: str, req: Request, data:UpdateTeam, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException( 401 , 'Invalid User')
        team = get_team_by_urlname(team_id, session)
        if not team:
            raise HTTPException(404, 'Not team found')
        #after team and user is validated, user will be check if admin
        role = session.exec(select(Roles).where(
                Roles.team_id == team.id, Roles.name == 'admin'
            )).first() # no need validation since 'admin' is created by default
        user_team = session.exec(select(UserTeamRoleLink).where(
                UserTeamRoleLink.user == user,
                UserTeamRoleLink.team == team,
                UserTeamRoleLink.roles == role
            )).first()
        if not user_team:
            raise HTTPException(403, 'Access denied')
        team.name = data.name
        team.urlname = data.name.lower().strip().replace(' ','-')+ '-' + os.urandom(8).hex()
        team.is_active = data.is_active
        session.add(team)
        session.commit()
        return create_response('success', 'Team has been updated', 202)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on update single teams', 500)
    
@router.delete('/{team_id}')
async def delete(team_id:str, req: Request, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            raise HTTPException( 401 , 'Invalid User')
        team = get_team_by_urlname(team_id, session)
        if not team:
            raise HTTPException(404, 'Not team found')
        #after team and user is validated, user will be check if admin
        role = session.exec(select(Roles).where(
            Roles.team_id == team.id, Roles.name == 'admin')
        ).first() # no need validation since 'admin' is created by default
        user_team = session.exec(select(UserTeamRoleLink).where(
                UserTeamRoleLink.user == user,
                UserTeamRoleLink.team == team,
                UserTeamRoleLink.roles == role
            )).first()
        if not user_team:
            raise HTTPException(403, 'Access denied')
        session.delete(team)
        session.commit()
        return create_response('success', 'Team has been deleted', 202)
    except HTTPException as h:
        return create_response('error', h.detail, h.status_code)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on update single teams', 500)