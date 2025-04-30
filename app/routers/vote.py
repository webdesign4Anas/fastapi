from fastapi import FastAPI,HTTPException,Response,status,Depends,APIRouter
from .. import database,models,schemas,oauth2
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Posts).filter(models.Posts.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with id {vote.post_id}is not even here")
    vote_query=db.query(models.Votes).filter(models.Votes.post_id==vote.post_id,models.Votes.user_id==current_user.id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="you already liked that post")
        new_vote=models.Votes(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message":"your vote added succesfully"}
    if not found_vote:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="you cant do that its not even liked")
    db.delete(found_vote)
    db.commit()
    return{"message": "your vote deleted succesfully"}


