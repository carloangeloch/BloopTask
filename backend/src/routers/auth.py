from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
import bcrypt
from datetime import datetime
import os
import json

from lib.db import engine
from lib.jwt import create_token, verify_token
from serializers.auth import GetTeamUserData, GetTeam, LoginUser, UserTokenPayload, GetMemberUserData
from models.user import User
from models.team import Team, Roles
from models.enum import UserRoleEnum



router = APIRouter()


@router.get('/up')
async def auth_up():
    return JSONResponse({"Success":"AUth API working"}, status_code=status.HTTP_200_OK)

@router.post('/team/check')
async def team_check(req:GetTeam):
    with Session(engine) as sesssion:
        print(req.name)
        statement = select(Team).where(Team.name == req.name)
        team = sesssion.exec(statement).first()
        if team:
            return JSONResponse({"Error":"Team Name exists"}, status_code=status.HTTP_400_BAD_REQUEST)
        return JSONResponse({'Success':'No team name exist'}, status_code=status.HTTP_200_OK)
    return JSONResponse({'Error':'Error on team check'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post('/signup')
async def signup(req:GetTeamUserData):
    with Session(engine) as session:
        #received data for team and user
        #check if team name not yet exists via /team/check api
        #check if user email not yet exists
        user_statement = select(User).where(User.email == req.email)
        user = session.exec(user_statement).first()
        if user:
            return JSONResponse({"Error":"Email already exists"}, status_code=status.HTTP_400_BAD_REQUEST)
        hashed_password= bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

        team_url = req.team_name.lower().strip().replace(' ','-') + '-' + os.urandom(8).hex()
        #create team data
        new_team = Team(
            name = req.team_name,
            urlname=team_url,
            created_at=datetime.now()
        )
        session.add(new_team)
        session.commit()
        session.refresh(new_team)
        team_statement = select(Team).where(Team.urlname == team_url)
        team = session.exec(team_statement).first()

        #create roles data
        new_role_admin = Roles(
            name = UserRoleEnum.ADMIN.value,
            team_id=team.id
        )
        new_role_mod = Roles(
            name = UserRoleEnum.MODERATOR.value,
            team_id=team.id
        )
        new_role_member = Roles(
            name = UserRoleEnum.MEMBER.value,
            team_id=team.id
        )
        
        session.add_all([new_role_admin, new_role_member, new_role_mod])
        session.commit()
        session.refresh(new_role_admin) 
        session.refresh(new_role_mod) 
        session.refresh(new_role_member) 
        role_statement = select(Roles).where(Roles.name == 'admin')
        role = session.exec(role_statement).first()
        
        #create user data
        new_user = User(
            email = req.email,
            password=hashed_password,
            first_name=req.first_name,
            middle_name=req.middle_name,
            last_name=req.last_name,
            suffix=req.last_name,
            team_id=team.id,
            role_id=role.id,
            created_at=datetime.now()
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        #create token
        res = JSONResponse({"Success": "User, team and role has been created"}, status_code=status.HTTP_201_CREATED)
        user_json = json.loads(UserTokenPayload.model_validate(new_user).model_dump_json())
        token = create_token(user_json)
        res.set_cookie(key='jwt',value=token, httponly=True, secure=True, samesite='strict', max_age=7*24*60*60)

        return res
    return JSONResponse({'Error':'Error on signup check'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post('/team/member/signup/{team_id}')
async def member_signup(team_id: str, req:GetMemberUserData):
    with Session(engine) as session:
        team_statement = select(Team).where(Team.urlname == team_id)
        team = session.exec(team_statement).first()
        if not team:
            return JSONResponse({"Error":"No team found!"}, status_code=status.HTTP_400_BAD_REQUEST)
        user_statement = select(User).where(User.email == req.email)
        user = session.exec(user_statement).first()
        if user:
            return JSONResponse({"Error":"User already exists"}, status_code=status.HTTP_400_BAD_REQUEST)
        hashed_password = bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
        role_statement = select(Roles).where(Roles.team_id == team.id, Roles.name == 'member')
        role = session.exec(role_statement).first()
        new_user = User(
            email = req.email,
            password=hashed_password,
            first_name=req.first_name,
            middle_name=req.middle_name,
            last_name=req.last_name,
            suffix=req.last_name,
            team_id=team.id,
            role_id=role.id,
            created_at=datetime.now()
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        #create token
        res = JSONResponse({"Success": f"New user from {team.name} has been created"}, status_code=status.HTTP_201_CREATED)
        user_json = json.loads(UserTokenPayload.model_validate(new_user).model_dump_json())
        token = create_token(user_json)
        res.set_cookie(key='jwt',value=token, httponly=True, secure=True, samesite='strict', max_age=7*24*60*60)

        return res
    return JSONResponse({'Error':'Error on member signup check'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/login')
async def login(req:LoginUser):
    with Session(engine) as session:
        statement = select(User).where(User.email == req.email)
        user = session.exec(statement).first()
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