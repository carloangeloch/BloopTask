from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from lib.db import engine, create_tables
from contextlib import asynccontextmanager

from routers import auth, project

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    engine.begin()
    create_tables() 


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def start_app():
    return JSONResponse({"Succss":"Server Running"}, status_code=status.HTTP_200_OK)

app.include_router(auth.router, prefix='/api/auth', tags=['auth'])
app.include_router(project.router, prefix='/api/project', tags=['project'])