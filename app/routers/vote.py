from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # found_vote = db.scalar(
    #     select(models.Vote).filter(
    #         models.Vote.post_id == vote.post_id,
    #         models.Vote.user_id == current_user.id,
    #     )
    # )

    found_vote = db.get(models.Vote, (current_user.id, vote.post_id))

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        try:
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {vote.post_id} does not exist",
            )
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        db.delete(found_vote)
        db.commit()

        return {"message": "successfully deleted vote"}
