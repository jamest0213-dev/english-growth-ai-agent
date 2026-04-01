from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_input = Column(Text)
    ai_output = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)