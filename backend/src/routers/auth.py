from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get('/up')
async def auth_up():
    return JSONResponse({"Success":"AUth API working"}, status_code=status.HTTP_200_OK)