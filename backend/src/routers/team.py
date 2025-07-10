from fastapi import APIRouter, Request, Depends
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
from serializers.team import CreateTeam, GetTeam

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
            return create_response('error', 'Invalid User', 401)
        lookup_string = data.name.lower().strip().replace(' ','-')
        team_statement = select(Team).where(Team.urlname.contains(lookup_string))
        team = session.exec(team_statement).first()
        if team:
            return create_response('error', 'Team name exists', 400)
        new_team = Team(
            name = data.name,
            urlname=lookup_string+ '-' + os.urandom(8).hex(),
            created_at=datetime.now()
        )
        session.add(new_team)
        session.commit()

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

        print('new role admin id', new_role_admin.id)

        new_link = UserTeamRoleLink(
            user = user,
            team = new_team,
            roles = new_role_admin
        )
        session.add(new_link)
        session.commit()

        session.refresh(new_team)
        session.refresh(new_role_admin)
        session.refresh(new_role_member)
        session.refresh(new_role_mod)
        session.refresh(new_link)

        return create_response('success', f'User {user.first_name} has created a new team', 201)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on creating team', 500)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)

@router.get('/all')
async def get_teams(req: Request, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Invalid User', 401)
        #get all team that the user is added to
        user_team_statement = select(UserTeamRoleLink).where(UserTeamRoleLink.user == user)
        user_team = session.exec(user_team_statement).all()
        teams = [team.team for team in user_team]
        team_json = [
            json.loads(GetTeam.model_validate(team).model_dump_json())
            for team in teams
        ]
        return create_response('data', team_json, 200)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting all teams', 500)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    
@router.get('/{team_id}')
async def get_team(team_id: str, req: Request, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Invalid User', 401)
        team = get_team_by_urlname(team_id, session)
        if not team:
            create_response('error', 'No team found', 404)
        user_team_statement = select(UserTeamRoleLink).where(UserTeamRoleLink.user == user, UserTeamRoleLink.team == team)
        user_team = session.exec(user_team_statement).first()
        print('user team', user_team)
        if not user_team:
            raise ValueError('No team in user found')
        team_json = json.loads(GetTeam.model_validate(team).model_dump_json())
        return create_response('data', team_json, 200)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting single teams', 500)
    

#TODO: Check all exceptions and create custom error handlers