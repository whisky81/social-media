from fastapi import APIRouter 
from ..db import session_dependency
from .. import schemas, models 
from fastapi import Body, Query, Path, HTTPException, status
from typing import Annotated
from sqlmodel import select
from ..oauth2 import current_user_dependency
from sqlalchemy.sql import func


router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)



# @router.get("/", response_model=list[schemas.PublicPost])
@router.get("/", response_model=list[schemas.PostOut])
def get_posts(
    session: session_dependency,
    current_user: current_user_dependency,
    offset: Annotated[int | None, Query(ge=0)] = 0,
    limit: Annotated[int | None, Query(ge=3)] = 3
):
    """
    - Get posts
    - **offset**: the number of records you want to skip, the default value is 0
    - **limit**: the number of recores you want to retrieve, the default value is 3 (least posts)
    """
    # posts = session.exec(select(models.Post).offset(offset).limit(limit)).all()

    
    statement = select(models.Post, func.count(models.Vote.post_id)).join(models.Vote, isouter=True).group_by(models.Post)
    
    
    result = session.exec(statement).all()
    posts = []
    for post, votes in result:
        posts.append(
            {
                "post": post,
                "votes": votes
            }
        )
    
    
    return posts 


@router.get("/{post_id}", response_model=schemas.PublicPost)
def get_post_with_id(session: session_dependency, current_user: current_user_dependency, post_id: Annotated[int, Path(gt=0)]):
    """
    - Get a post with id
    """
    
    post = session.get(models.Post, post_id)
    
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} not found!")
    
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PublicPost)
def create_new_post(
    session: session_dependency,
    current_user: current_user_dependency,
    post: Annotated[
        schemas.CreatePost, 
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal post with publish",
                    "description": "A normal post with title, content and pushlished auto true",
                    "value": {
                        "title": "roadmap for backend dev",
                        "content": "on roadmap.sh",
                        "published": True
                    }
                }
            }
        )
    ]):
    """
    Create a post with:
    - **title**: Each post must have a title(string)
    - **content**: Each post must have a content(string)
    - **published**: Optional but defaults to True if user doesn't set it
    """
    post = models.Post.model_validate(post)
    post.owner_id = current_user.id 
    session.add(post)
    session.commit()
    session.refresh(post)
    
    return post 


@router.put("/{post_id}", response_model=schemas.PublicPost)
def update_post(
    session: session_dependency,
    current_user: current_user_dependency,
    post_id: Annotated[int, Path(gt=0)],
    update_post: Annotated[schemas.UpdatePost, Body()],
):
    """
    Update a post with given id
    
    All fields will be updated
    - **title**: optional
    - **content**: optional
    - **published**: optional
    """
    
    post = session.get(models.Post, post_id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # extract datas from update post (exclude attributes unset) that get from user
    update_data = update_post.model_dump(exclude_unset=True)
    # update current post that has got post_id 
    post.sqlmodel_update(update_data)
    
    # add and commit
    session.add(post)
    session.commit()
    session.refresh(post)
    
    return post 


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    session: session_dependency,
    current_user: current_user_dependency,
    post_id: Annotated[int, Path(ge=1)]
):
    """ 
    - delete post with id 
    """
    post = session.get(models.Post, post_id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} not found")
    
    if post.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    session.delete(post)
    session.commit()
    
