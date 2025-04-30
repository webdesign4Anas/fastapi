
from fastapi import FastAPI,HTTPException,Response,status,Depends,APIRouter
from .. import models,schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
router=APIRouter(
   prefix="/posts",
   tags=['Posts']
)
#@router.get("/",response_model=list[schemas.Post])
@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10, skip:int = 0,search:Optional[str]=""):
   posts=db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
   postvote=db.query(models.Posts,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id==models.Posts.id,isouter=True,).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
   print(postvote)
   return [{"post": post, "votes": votes} for post, votes in postvote]


@router.get("/{id}", response_model=schemas.PostOut)
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_vote=db.query(models.Posts,func.count(models.Votes.post_id).label("votes"))\
    .join(models.Votes,models.Votes.post_id==models.Posts.id,isouter=True)\
    .group_by(models.Posts.id)\
    .filter(models.Posts.id==id)\
    .first()
    if not post_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    post,votes=post_vote
    return{"post":post,
           "votes":votes
           }
    
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
  print(current_user.id)
  new_post=models.Posts(owner_id=current_user.id,**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def DeleteUsers(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Query to find the post by ID
    query = db.query(models.Posts).filter(models.Posts.id == id).first()
    
    # Check if the post exists
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Check if the current user is the owner of the post
    if current_user.id != query.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized")
    
    # Delete the post from the database
    db.delete(query)
    db.commit()
    
    # No content returned (status code 204)
    return None

   
   
   


@router.put("/{id}")
def Update_Post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
   post_query=db.query(models.Posts).filter(models.Posts.id==id)
   postup=post_query.first()
   if not postup:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the id you are getting not found {id}")
   if current_user.id != postup.owner_id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not authorized")
   post_query.update(post.dict(), synchronize_session=False)
   db.commit()
   
   return  post_query.first()
