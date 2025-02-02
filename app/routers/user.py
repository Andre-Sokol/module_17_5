from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import Task
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_Found, detail="User was not found")


@router.get('/user_id/tasks')
async def tasks_by_user_id(user_id, db: Annotated[Session, Depends(get_db)]):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='This is not task found')
    return tasks


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put("/update")
async def update_user(user_id: int, updated_user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.id == user_id)
    user = db.scalar(query)
    if user:
        db.execute(update(User).where(User.id == user_id).values(**updated_user.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User was not found")


@router.delete("/delete")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    query = select(User).where(User.id == user_id)
    user = db.scalar(query)
    if user:
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK,
                "transaction": "User and associated tasks were successfully deleted!"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User was not found")
