from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from lib.db import engine, create_tables
from contextlib import asynccontextmanager

from routers import auth, project, tasklist, task, taskcomment, team

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    engine.begin()
    create_tables() 

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/up")
async def start_app():
    return JSONResponse({"Succss":"Server Running"}, status_code=status.HTTP_200_OK)

app.include_router(auth.router, prefix='/api/auth', tags=['auth'])
app.include_router(team.router, prefix='/api/team', tags=['team'])
app.include_router(project.router, prefix='/api/project', tags=['project'])
app.include_router(tasklist.router, prefix='/api/tasklist', tags=['tasklist'])
app.include_router(task.router, prefix='/api/task', tags=['task'])
app.include_router(taskcomment.router, prefix='/api/taskcomment', tags=['task comment'])