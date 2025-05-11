from fastapi import FastAPI,Depends
from .routers import posts,users,auth,vote
from random import randrange
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine,get_db,Base
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI() 
#models.Base.metadata.create_all(bind=engine) # this creates the models eg the tables
Base.metadata.create_all(bind=engine)
origins=["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return{"message" : "hello anas"}
      
      



