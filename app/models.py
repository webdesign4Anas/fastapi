from .database import Base
from sqlalchemy import Column , String , Integer, Boolean,TIMESTAMP,ForeignKey
from sqlalchemy.sql.expression import text   
from sqlalchemy.orm import relationship
            
class Posts(Base):  
# that is the first table model so orm (sqlalchemy) will convert it to db table
    __tablename__="posts"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True', nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'), nullable=False) 
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="cascade"),nullable=False)
    owner=relationship("Users")

class Users(Base):
    __tablename__="users"   
    id=(Column(Integer,primary_key=True,nullable=False))     
    email=(Column(String,nullable=False,unique=True))
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False)\

class Votes(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="cascade"), primary_key=True)   
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="cascade"), primary_key=True) 
                    



