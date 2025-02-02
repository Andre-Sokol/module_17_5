from fastapi import APIRouter
from app.backend.db import Column, ForeignKey, Integer, String, Boolean, Base
from sqlalchemy.orm import relationship
from app.models import *

router = APIRouter(prefix="/task", tags=["task"])


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    priority = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    content = Column(String)
    title = Column(String)
    completed = Column(Boolean, default=False)
    slug = Column(String, unique=True, index=True)
    user = relationship("User", back_populates="tasks")


from sqlalchemy.schema import CreateTable

print(CreateTable(Task.__table__))
