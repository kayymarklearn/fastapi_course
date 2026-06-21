from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user.email = user.email.lower()
    new_user = models.User(**user.dict())
    db.add(new_user)  # add new row/entry to the database
    db.commit()
    db.refresh(new_user)  # retrieve that newly added row into new_post
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, id)

    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found!"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found!",
        )

    return user
