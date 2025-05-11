from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from app.database import get_db,Base
from fastapi.testclient import TestClient
from app.oauth2 import create_access_token
from app import models
import pytest
client=TestClient(app)

TEST_DB_NAME = "fastapi_test"
SQL_ALCHEMY_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{TEST_DB_NAME}'

engine=create_engine(SQL_ALCHEMY_URL)

TestingSessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)





@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session

        finally: session.close()    

    app.dependency_overrides [get_db]=override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_json={"email":"anasahmed22@gmail.com","password":"22526618a"}
    res=client.post("/users",json=user_json)
    new_user=res.json()
    new_user["password"]=user_json["password"]
    return new_user
    

@pytest.fixture
def token (test_user):
    token = create_access_token({"user_id": test_user["id"]})
    return token

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user,session):
    post_data = [
    {
        "title": "Random Post 1",
        "content": "This is the content for post 1. Random text.",
        "owner_id": test_user['id']
    },
    {
        "title": "Random Post 2",
        "content": "This is the content for post 2. Random text.",
        "owner_id": test_user['id']
    },
    {
        "title": "Random Post 3",
        "content": "This is the content for post 3. Random text.",
        "owner_id": test_user['id']
    }
    ]

    def postfunc(post):
        return models.Posts(**post)
    post_map=map(postfunc,post_data)
    posts=list(post_map)
    session.add_all(posts)
    session.commit()
    posts=session.query(models.Posts).all()
    return posts
