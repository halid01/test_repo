from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Post(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(Text)
    created_id = Column(DateTime)
    author_id = Column
    
    
    user_id = Column(Integer, ForeignKey('users.id'))