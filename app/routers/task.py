from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.query(Task).all()
    return tasks


@router.get("/task_id")
async def task_by_id(task_id, db: Annotated[Session, Depends(get_db)]):
    task = db.query(Task).get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='This is not task found')
    return task


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user = db.scalars(select(User).where(User.id == user_id)).all()
    if user:
        db.execute(insert(Task).values(title=create_task.title,
                                       content=create_task.content,
                                       priority=create_task.priority,
                                       user_id=user_id,
                                       slug=slugify(create_task.title)))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')


@router.put("/update")
async def update_task(user_id: int, updated_task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.id == user_id)
    task = db.scalar(query)
    if task:
        db.execute(update(Task).where(Task.id == task_id).values(**updated_task.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User was not found")


@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='This is not task found')
    db.execute(
        delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successful'}
