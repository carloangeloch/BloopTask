from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse


from lib.jwt import verify_token
from models.user import User
from models.team import Team, Roles

router  = APIRouter()


@router.get('/up')
async def auth_up():
    return JSONResponse({"Success":"Project API working"}, status_code=status.HTTP_200_OK)