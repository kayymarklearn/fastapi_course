from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import func
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/", response_model=List[schemas.PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.execute(
    #     select(models.Post)
    #     .offset(offset=skip)
    #     .limit(limit=limit)
    #     .filter(models.Post.title.contains(search))
    # ).scalars()

    results = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes"),
        )
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search))
        .group_by(models.Post.id)
        .offset(offset=skip)
        .limit(limit=limit)
    ).all()
    return results  # posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )

    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)  # add new row/entry to the database
    db.commit()
    db.refresh(new_post)  # retrieve that newly added row into new_post
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    
    # post = db.execute(select(models.Post).where(models.Post.id == id)).scalar()
    #post = db.get(models.Post, id)

    post = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes"),
        )
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).filter(models.Post.id == id)
        .group_by(models.Post.id)
    ).first()

    if post:
        return post

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id: {id} was not found!"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} was not found!",
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    # post = db.execute(select(models.Post).where(models.Post.id == id)).scalar()
    post = db.get(models.Post, id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    db.delete(post)
    db.commit()


@router.put(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    #  cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # post = cursor.fetchone()
    # conn.commit()

    data = post.dict(exclude_unset=True)

    update_post = db.execute(select(models.Post).where(models.Post.id == id)).scalar()

    if update_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    if update_post:
        update_post.title = post.title
        update_post.content = post.content
        for k, v in data.items():
            setattr(update_post, k, v)
        db.commit()
        db.refresh(update_post)
        return update_post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {id} does not exist.",
    )
