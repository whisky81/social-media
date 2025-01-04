from fastapi import APIRouter 
from ..db import session_dependency
from .. import schemas, models 
from fastapi import HTTPException, status
from sqlmodel import select
from ..oauth2 import current_user_dependency



router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    session: session_dependency,
    current_user: current_user_dependency,
    vote: schemas.Vote
):
    
    """
    - **If dir == True, if you want to like it, or False if you don't like it.**
    """
    post_in_db = session.get(models.Post, vote.post_id)
    found_post = post_in_db is not None 
    if found_post == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} not found") 


    vote_in_db = session.exec(select(models.Vote).where(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)).first()
    found_vote = vote_in_db is not None 
    
    
    if vote.dir== True:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"this post with id: {vote.post_id} has already been liked by this user")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"this post with id: {vote.post_id} has not been liked yet")
        
        session.delete(vote_in_db)
        session.commit() 
    
    return "success"

