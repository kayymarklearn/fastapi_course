from .database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.types import TIMESTAMP
from datetime import datetime
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(
        Boolean, server_default="TRUE", nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    author: Mapped["User"] = relationship(back_populates="posts")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()")
    )

    posts: Mapped[list[Post]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )


class Vote(Base):
    __tablename__ = "votes"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
