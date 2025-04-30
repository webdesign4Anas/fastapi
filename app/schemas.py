from pydantic import BaseModel,EmailStr,conint,Field
from datetime import datetime
from typing import Optional






class UserOut(BaseModel):
     email:EmailStr
     created_at:datetime
     id:int

class PostBase(BaseModel):
        title:str
        content:str
        published:bool= True

class PostCreate(PostBase):
   pass

class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    created_at:datetime
    owner:UserOut
    
    class Config:
         from_attributes=True

class PostOut(BaseModel):
    post: Post
    votes: int

class UsersCreate(BaseModel):
     email:EmailStr
     password:str





class UserLogin(BaseModel):
     email:EmailStr
     password:str

class Token(BaseModel):
     access_token:str
     token_type:str


class TokenData(BaseModel):
     id:Optional[int]

class Vote(BaseModel):
     post_id:int
     dir: int = Field(..., ge=0, le=1)