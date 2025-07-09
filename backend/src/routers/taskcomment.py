from fastapi import APIRouter, Request, Depends
from sqlmodel import Session, select
from datetime import datetime
import json
from typing import List, Dict

from lib.responses import create_response
from .queries import get_session, get_user_by_email
from lib.jwt import verify_token
from models.project import Task, TaskComment
from serializers.taskcomment import CreateTaskComment, GetComment
router = APIRouter()

@router.get('/up')
async def task_comment_up():
    return create_response('success', 'Task comment API working', 200)

@router.post('/create/{tid}')
async def create_task_comment(tid: int, req: Request,data: CreateTaskComment, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Unauthrized - No user found', 400)
        task_statement = select(Task).where(Task.id == tid)
        task = session.exec(task_statement).first()
        if not task:
            return create_response('error', 'No task found', 400)
        new_comment = TaskComment(
            task_id = task.id,
            user_id = user.id,
            comment = data.comment,
            created_at = datetime.now()
        )
        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)
        return create_response('success', f'New comment has been created by {user.first_name}', 201)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on creating task comment', 500)
    
@router.get('/all/{tid}')
async def get_comments(tid: int, req: Request, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Unauthrized - No user found', 400)
        task_statement = select(Task).where(Task.id == tid)
        task = session.exec(task_statement).first()
        if not task:
            return create_response('error', 'No task found', 400)
        comment_statement = select(TaskComment).where(TaskComment.task_id == tid)
        comments = session.exec(comment_statement).all()
        comments_json: List[Dict] = [
            json.loads(GetComment.model_validate(comment).model_dump_json())
            for comment in comments
        ]
        return create_response('data', comments_json, 200)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting all task comment', 500)
    
@router.get('/{tcid}/{tid}')
async def get_comment(tcid: int, tid: int, req: Request, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Unauthrized - No user found', 400)
        task_statement = select(Task).where(Task.id == tid)
        task = session.exec(task_statement).first()
        if not task:
            return create_response('error', 'No task found', 400)
        comment_statement = select(TaskComment).where(TaskComment.id == tcid)
        comments = session.exec(comment_statement).first()
        comments_json = json.loads(GetComment.model_validate(comments).model_dump_json())
        return create_response('data', comments_json, 200)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on getting single task comment', 500)
    
@router.put('/{tcid}/{tid}')
async def update_comment(tcid: int, tid: int, req: Request, data: CreateTaskComment , session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Unauthrized - No user found', 400)
        task_statement = select(Task).where(Task.id == tid)
        task = session.exec(task_statement).first()
        if not task:
            return create_response('error', 'No task found', 400)
        comment_statement = select(TaskComment).where(TaskComment.id == tcid, TaskComment.user_id == user.id)
        comment = session.exec(comment_statement).first()
        if not comment:
            return create_response('error', 'Access Denied', 400)
        comment.comment = data.comment

        session.add(comment)
        session.commit()
        session.refresh(comment)
        return create_response('success', f'Comment on task {task.id} has been updated', 202)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on updating task comment', 500)
    
@router.delete('/{tcid}/{tid}')
async def delete_comment(tcid: int, tid: int, req: Request, session: Session = Depends(get_session)):
    try:
        payload = verify_token(req.cookies.get('jwt'))
        user = get_user_by_email(payload['email'], session)
        if not user:
            return create_response('error', 'Unauthrized - No user found', 400)
        task_statement = select(Task).where(Task.id == tid)
        task = session.exec(task_statement).first()
        if not task:
            return create_response('error', 'No task found', 400)
        comment_statement = select(TaskComment).where(TaskComment.id == tcid, TaskComment.user_id == user.id)
        comment = session.exec(comment_statement).first()
        if not comment:
            return create_response('error', 'Access Denied', 400)
        session.delete(comment)
        session.commit()
        return create_response('success', f'Comment on task {task.id} has been deleted', 202)
    except TypeError as te:
        return create_response('error', str(te), 401)
    except ValueError as ve:
        return create_response('error', str(ve), 401)
    except Exception as e:
        print(e)
        return create_response('error', 'Error on deleting task comment', 500)