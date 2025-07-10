from fastapi import APIRouter, Request, Depends
from sqlmodel import Session, select
import bcrypt
from datetime import datetime
import os
import json

from lib.jwt import create_token, verify_token
from serializers.auth import GetTeamUserData, GetTeam, LoginUser, UserTokenPayload
from models.user import User
from models.team import Team, Roles
from models.link import UserTeamRoleLink
from models.enum import UserRoleEnum
from .queries import get_session, get_user_by_email
from lib.responses import create_response

router = APIRouter() 

@router.get('/up')
async def auth_up():
    return create_response('success', 'Auth API working', 200)

@router.post('/team/check')
async def team_check(req:GetTeam, session: Session = Depends(get_session)):
    try:
        lookup_string = req.name.lower().strip().replace(' ','-')
        statement = select(Team).where(Team.urlname.contains(lookup_string))
        team = session.exec(statement).first()
        if team:
            return create_response('error', 'Team name exists', 400)
        return create_response('success', 'Team name available', 200)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on team check', 500)

@router.post('/signup')
async def signup(req:GetTeamUserData, session: Session = Depends(get_session)):
    try:
        user = get_user_by_email(req.email, session)
        if user:
            return create_response('error', 'Email already exists', 400)
        hashed_password=bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
        team_url = req.team_name.lower().strip().replace(' ','-') + '-' + os.urandom(8).hex()
        
        lookup_string = req.team_name.lower().strip().replace(' ','-')
        team_statement = select(Team).where(Team.urlname.contains(lookup_string))
        team = session.exec(team_statement).first()
        if team:
            return create_response('error', 'Team name exists', 400)
        new_team = Team(
            name = req.team_name,
            urlname=team_url,
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
        
        new_user = User(
            email = req.email,
            password=hashed_password,
            first_name=req.first_name,
            middle_name=req.middle_name,
            last_name=req.last_name,
            suffix=req.last_name,
            created_at=datetime.now(),
        )
        session.add(new_user)
        session.commit()

        new_link = UserTeamRoleLink(
            user = new_user,
            team = new_team,
            roles = new_role_admin
        )
        session.add(new_link)
        session.commit()

        session.refresh(new_user)
        session.refresh(new_team)
        session.refresh(new_role_admin) 
        session.refresh(new_role_mod) 
        session.refresh(new_role_member)
        session.refresh(new_link)

        res = create_response('success', "User, team and role has been created", 201)
        user_json = json.loads(UserTokenPayload.model_validate(new_user).model_dump_json())
        token = create_token(user_json)
        res.set_cookie(key='jwt',value=token, httponly=True, secure=True, samesite='strict', max_age=7*24*60*60)
        return res
    except Exception as e:
        print(e)
        return create_response('error', 'Error on new user signup', 500)

#Deprecated: Instead, create new user, then ask for invitation from the team.
# @router.post('/team/member/signup/{team_id}')
# async def member_signup(team_id: str, req:GetMemberUserData, session: Session = Depends(get_session)):
#     try:
#         team = get_team_by_urlname(team_id, session)
#         if not team:
#             return create_response('error', 'No team found', 400)
#         user = get_user_by_email(req.email, session)
#         if user:
#             return create_response('error', 'User already exists')
#             return JSONResponse({"Error":"User already exists"}, status_code=status.HTTP_400_BAD_REQUEST)
#         hashed_password = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
#         new_user = User(
#             email = req.email,
#             password=hashed_password,
#             first_name=req.first_name,
#             middle_name=req.middle_name,
#             last_name=req.last_name,
#             suffix=req.last_name,
#             created_at=datetime.now()
#         )
#         session.add(new_user)
#         session.commit()
        
#         role_statement = select(Roles).where(Roles.team_id == team.id, Roles.name == 'member')
#         role = session.exec(role_statement).first()

#         new_link = UserTeamRoleLink(
#             user = new_user,
#             team = team,
#             role = role.id
#         )
#         session.add(new_link)
#         session.commit()

#         session.refresh(new_user)
#         session.refresh(new_link)
#         #create token
#         res = create_response('success', f"New user from {team.name} has been created", 201)
#         user_json = json.loads(UserTokenPayload.model_validate(new_user).model_dump_json())
#         token = create_token(user_json)
#         res.set_cookie(key='jwt',value=token, httponly=True, secure=True, samesite='strict', max_age=7*24*60*60)

#         return res
#     except Exception as e:
#         print(e)
#         return create_response('error', 'Error on new member signup check', 500)

@router.post('/login')
async def login(req:LoginUser, session: Session = Depends(get_session)):
    try:
        user = get_user_by_email(req.email, session)
        if not user:
            return create_response('error', 'Invalid Credentials', 400)
        #check if not user 
        check_pwd = bcrypt.checkpw(req.password.encode('utf-8'), user.password.encode('utf-8'))
        #check if password incorrent
        if not check_pwd:
            return create_response('Error','Invalid Credentials', 400)
        user_json = json.loads(UserTokenPayload.model_validate(user).model_dump_json())
        res = create_response('success',"User logged in", 200)
        #create token
        token = create_token(user_json)
        res.set_cookie('jwt',value=token, httponly=True, secure=True, samesite='strict', max_age=7*24*60*60)
        return res
    except Exception as e:
        print(e)
        return create_response('error', 'Error on user login', 500)

@router.post('/logout')
async def logout():
    res = create_response('success', "User logged out", 200)
    res.delete_cookie('jwt')
    return res
    
@router.post('/check')
async def check(req: Request):
    token = req.cookies.get('jwt')
    if not token:
        return create_response('error',  "Unauthorized - No token found", 400)
    try:
        payload = verify_token(token)
        return create_response('data', payload, 200)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on check auth', 500)