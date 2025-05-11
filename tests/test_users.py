from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from app.database import get_db,Base
from fastapi.testclient import TestClient
from app import schemas
from jose import JWTError,jwt
from fastapi import status
import pytest



def test_root(client):
    res=client.get("/")
    assert res.status_code==200
    assert res.json().get("message")=="hello anas"

def test_user_create(client):
    json_data={"email":"anasahmed22@gmail.com","password":"22526618a"}
    res=client.post("/users",json=json_data)
    new_user=schemas.UserOut(**res.json())
    assert res.status_code==201
    assert new_user.email=="anasahmed22@gmail.com"

def test_user_login(client,test_user):
    res=client.post("/login",data={"username":test_user["email"],"password":test_user["password"]})
    res_login=schemas.Token(**res.json())
    payload=jwt.decode(res_login.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id:int=payload.get("user_id")
    assert id==test_user["id"]
    assert res.status_code==200


def test_incorrect_login(client,test_user):
   res=client.post("/login",data={"username":test_user['email'],"password":"wrongpassword"})
   assert res.status_code==403
       

    
    

   