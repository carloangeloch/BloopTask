from fastapi import APIRouter, status, Request, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
import bcrypt
from datetime import datetime
import os
import json

from lib.jwt import create_token, verify_token
from serializers.auth import GetTeamUserData, GetTeam, LoginUser, UserTokenPayload, GetMemberUserData
from models.user import User
from models.team import Team, Roles
from models.link import UserTeamRoleLink
from models.enum import UserRoleEnum
from .queries import get_session, get_team_by_urlname, get_user_by_email
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
    except:
        return create_response('error', 'Error on team check', 500)

@router.post('/signup')
async def signup(req:GetTeamUserData, session: Session = Depends(get_session)):
    try:
        #received data for team and user
        #check if team name not yet exists via /team/check api
        #check if user email not yet exists
        user = get_user_by_email(req.email, session)
        if user:
            return create_response('error', 'Email already exists', 400)
        hashed_password=bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
        team_url = req.team_name.lower().strip().replace(' ','-') + '-' + os.urandom(8).hex()
        #create team data
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

        #create roles data
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
        
        #create user data
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

        #create token
        res = create_response('success', "User, team and role has been created", 201)
        user_json = json.loads(UserTokenPayload.model_validate(new_user).model_dump_json())
        token = create_token(user_json)
        res.set_cookie(key='jwt',value=token, httponly=True, secure=True, samesite='strict', max_age=7*24*60*60)
        return res
    except Exception as e:
        print(e)
        return create_response('error', 'Error on new user signup check', 500)

@router.post('/team/member/signup/{team_id}')
async def member_signup(team_id: str, req:GetMemberUserData, session: Session = Depends(get_session)):
    try:
        team = get_team_by_urlname(team_id, session)
        if not team:
            return JSONResponse({"Error":"No team found!"}, status_code=status.HTTP_400_BAD_REQUEST)
        user = get_user_by_email(req.email, session)
        if user:
            return JSONResponse({"Error":"User already exists"}, status_code=status.HTTP_400_BAD_REQUEST)
        hashed_password = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
        new_user = User(
            email = req.email,
            password=hashed_password,
            first_name=req.first_name,
            middle_name=req.middle_name,
            last_name=req.last_name,
            suffix=req.last_name,
            created_at=datetime.now()
        )
        session.add(new_user)
        session.commit()
        #TODO: Fix role delaration on member creation
        
        #pull 

        # new_link = UserTeamRoleLink(
        #     user = new_user,
        #     team = team,
        #     role = 
        # )

        session.refresh(new_user)
        #create token
        res = JSONResponse({"Success": f"New user from {team.name} has been created"}, status_code=status.HTTP_201_CREATED)
        user_json = json.loads(UserTokenPayload.model_validate(new_user).model_dump_json())
        token = create_token(user_json)
        res.set_cookie(key='jwt',value=token, httponly=True, secure=True, samesite='strict', max_age=7*24*60*60)

        return res
    except:
        return JSONResponse({'Error':'Error on member signup check'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post('/login')
async def login(req:LoginUser, session: Session = Depends(get_session)):
    try:
        user = get_user_by_email(req.email, session)
        if not user:
            return JSONResponse({"Error":"Invalid Credentials"}, status_code=status.HTTP_400_BAD_REQUEST)
        #check if not user 
        check_pwd = bcrypt.checkpw(req.password.encode('utf-8'), user.password.encode('utf-8'))
        #check if password incorrent
        if not check_pwd:
            return JSONResponse({"Error":"Invalid Credentials"}, status_code=status.HTTP_400_BAD_REQUEST)
        user_json = json.loads(UserTokenPayload.model_validate(user).model_dump_json())
        res = JSONResponse({"Success":"User logged in"},status_code=status.HTTP_200_OK)
        #create token
        token = create_token(user_json)
        res.set_cookie('jwt',value=token, httponly=True, secure=True, samesite='strict', max_age=7*24*60*60)
        return res
    except:
        return JSONResponse({"Error":"Error on login"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post('/logout')
async def logout():
    res = JSONResponse({"Success":"User logged out"}, status_code=status.HTTP_200_OK)
    res.delete_cookie('jwt')
    return res
    
@router.post('/check')
async def check(req: Request):
    token = req.cookies.get('jwt')
    if not token:
        return JSONResponse({"Error": "Unauthorized - No token found"}, status_code=status.HTTP_400_BAD_REQUEST)
    try:
        payload = verify_token(token)
        return JSONResponse(payload, status_code=status.HTTP_200_OK)
    except:
        return JSONResponse({"Error":"Error on check auth"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)