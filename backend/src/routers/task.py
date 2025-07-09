from fastapi import APIRouter, Request, Depends
from sqlmodel import Session, select, desc
from datetime import datetime
import json
from typing import List, Dict

from lib.jwt import verify_token
from .queries import get_session, get_user_by_email, get_tasklist_by_tlid
from lib.responses import create_response
from models.project import Task
from serializers.task import CreateTask, GetTasks, UpdateTask
router = APIRouter()



@router.get('/up')
async def task_up():
    return create_response('success', 'Task API working', 200)

@router.post('/create/{tlid}')
async def create_task(tlid: int, req: Request, data: CreateTask, session: Session = Depends(get_session)):
    try:
        #verify user
        payload = verify_token(req.cookies.get('jwt'))
        if not payload: 
            return create_response('error','Unautorized - no token found', 401)
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'No user found', 400)
        tasklist = get_tasklist_by_tlid(tlid, session)
        if not tasklist:
            return create_response('error', 'No tasklist found', 400)
        task_statement = select(Task).where(Task.tasklist_id == tasklist.id).order_by(desc(Task.position))
        task = session.exec(task_statement).first()
        new_task = Task(
            tasklist_id= tasklist.id,
            title= data.title,
            description = data.description,
            created_by = user.id,
            assinged_to = data.assinged_to,
            created_at = datetime.now(),
            start_date = data.start_date,
            due_date = data.due_date,
            priority = data.priority,
            position = task.position + 1 if task else 0
        )
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return create_response('success', f'New task on {tasklist.id} has been created', 201)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
       print(e)
       return create_response('error', 'Error on creating task', 500)
    
@router.get('/all/{tlid}')
async def get_tasks(tlid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #verify user
        payload = verify_token(req.cookies.get('jwt'))
        if not payload: 
            return create_response('error','Unautorized - no token found', 401)
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'No user found', 400)
        tasklist = get_tasklist_by_tlid(tlid, session)
        if not tasklist:
            return create_response('error', 'No tasklist found', 400)
        task_statement = select(Task).where(Task.tasklist_id == tasklist.id)
        tasks = session.exec(task_statement).all()
        print(tasks)
        task_json: List[Dict] = [
            json.loads(GetTasks.model_validate(task).model_dump_json())
            for task in tasks
        ]
        return create_response('data', task_json, 200)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
       print(e)
       return create_response('error', 'Error on getting all task', 500)
    
@router.get('/{tid}/{tlid}')
async def get_task(tid: int, tlid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #verify user
        payload = verify_token(req.cookies.get('jwt'))
        if not payload: 
            return create_response('error','Unautorized - no token found', 401)
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'No user found', 400)
        tasklist = get_tasklist_by_tlid(tlid, session)
        if not tasklist:
            return create_response('error', 'No tasklist found', 400)
        task_statement = select(Task).where(Task.tasklist_id == tasklist.id, Task.id == tid)
        task = session.exec(task_statement).first()
        if not task:
            return create_response('error', 'No data found', 404)
        task_json = json.loads(GetTasks.model_validate(task).model_dump_json())
        return create_response('data', task_json, 200)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
       print(e)
       return create_response('error', 'Error on getting a task', 500)
    
@router.put('/{tid}/{tlid}')
async def update_task(tid: int, tlid: int, req: Request, data: UpdateTask, session: Session = Depends(get_session)):
    try:
        #verify user
        payload = verify_token(req.cookies.get('jwt'))
        if not payload: 
            return create_response('error','Unautorized - no token found', 401)
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'No user found', 400)
        tasklist = get_tasklist_by_tlid(tlid, session)
        if not tasklist:
            return create_response('error', 'No tasklist found', 400)
        task_statement = select(Task).where(Task.tasklist_id == tasklist.id, Task.id == tid)
        task = session.exec(task_statement).first()
        if not task:
            return create_response('error', 'No data found', 404)
        task.title = data.title
        task.description = data.description
        task.assinged_to = data.assinged_to
        task.start_date = data.start_date
        task.due_date = data.due_date
        task.priority = data.priority
        task.position = data.position
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return create_response('success', f'Task {task.id} on tasklist {tasklist.id} has beed updated', 202)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
       print(e)
       return create_response('error', 'Error on updating task', 500)
    
@router.delete('/{tid}/{tlid}')
async def delete_task(tid: int, tlid: int, req: Request, session: Session = Depends(get_session)):
    try:
        #verify user
        payload = verify_token(req.cookies.get('jwt'))
        if not payload: 
            return create_response('error','Unautorized - no token found', 401)
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'No user found', 400)
        tasklist = get_tasklist_by_tlid(tlid, session)
        if not tasklist:
            return create_response('error', 'No tasklist found', 400)
        task_statement = select(Task).where(Task.tasklist_id == tasklist.id, Task.id == tid)
        task = session.exec(task_statement).first()
        if not task:
            return create_response('error', 'No data found', 404)
        session.delete(task)
        session.commit()
        return create_response('success', f'Task {tid} in tasklist {tlid} has been deleted', 202)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
       print(e)
       return create_response('error', 'Error on deleting task', 500)