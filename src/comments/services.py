from typing import List

from fastapi import HTTPException
from fastapi import status
from posts.models import Post
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Comment


async def create_new_comment(db: AsyncSession, comment: Comment) -> Comment:
    try:
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )
    return comment


async def get_post_comments(db: AsyncSession, post_id) -> List[Comment]:
    post_statement = select(Post).where(Post.id == post_id)
    try:
        result = await db.execute(post_statement)
        result.scalar_one()
    except (NoResultFound, SQLAlchemyError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )

    statement = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .options(selectinload(Comment.user))
    )
    try:
        results = await db.execute(statement)
        comments = results.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong",
        )
    return comments


async def get_a_comment(db: AsyncSession, comment_id: int, post_id: int) -> Comment:
    post_statement = select(Post).where(Post.id == post_id)
    try:
        res = await db.execute(post_statement)
        res.scalar_one()
    except (NoResultFound, SQLAlchemyError):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
    statement = (
        select(Comment)
        .where(Comment.id == comment_id, Comment.post_id == post_id)
        .options(selectinload(Comment.user))
    )
    try:
        result = await db.execute(statement)
        comment = result.scalar_one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="comment not found",
        )
    return comment
