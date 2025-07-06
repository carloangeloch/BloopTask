from pydantic import BaseModel, EmailStr, ConfigDict

class GetTeamUserData(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    middle_name: str
    last_name: str
    suffix: str
    team_name: str

class GetMemberUserData(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    middle_name: str
    last_name: str
    suffix: str

class GetTeam(BaseModel):
    name: str

class LoginUser(BaseModel):
    email: str
    password: str

class UserTokenPayload(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    team_id: int
    role_id: int

    model_config = ConfigDict(from_attributes=True)