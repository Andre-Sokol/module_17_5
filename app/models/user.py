from fastapi import APIRouter
from app.backend.db import Column, Integer, String, Base
from sqlalchemy.orm import relationship

router = APIRouter(prefix='/user', tags=['user'])


class User(Base):
    __tablename__ = 'users'
    username = Column(String)
    firstname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    lastname = Column(String)
    id = Column(Integer, primary_key=True, index=True)


    tasks = relationship("Task", back_populates="user")



from sqlalchemy.schema import CreateTable

print(CreateTable(User.__table__))
