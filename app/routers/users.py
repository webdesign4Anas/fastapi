
from fastapi import FastAPI,HTTPException,Response,status,Depends,APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session
router=APIRouter(
   prefix="/users",
   tags=['Users']
)
@router.post("/",response_model=schemas.UserOut,status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UsersCreate,db:Session=Depends(get_db)):
   hashed_password=utils.hash(user.password)
   user.password=hashed_password
   created_user=models.Users(**user.dict())
   db.add(created_user)
   db.commit()
   db.refresh(created_user)
   return created_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_users(id:int,db:Session=Depends(get_db)):
   the_user=db.query(models.Users).filter(models.Users.id==id).first()
   if not the_user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the user with the id of : {id} not available " )
   return the_user   