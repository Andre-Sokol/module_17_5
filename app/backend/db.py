from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship


engine = create_engine("sqlite:///taskmanager.db", echo=True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass