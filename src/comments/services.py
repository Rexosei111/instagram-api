from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Comment


async def create_new_comment(db: AsyncSession, comment: Comment) -> Comment:
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def get_post_comments(db: AsyncSession, post_id) -> List[Comment]:
    statement = (
        select(Comment)
        .where(Comment.post_id == post_id)
        .options(selectinload(Comment.user))
    )
    comments = await db.execute(statement)
    return comments.scalars().all()


async def get_a_comment(db: AsyncSession, comment_id: int, post_id: int) -> Comment:
    statement = (
        select(Comment)
        .where(Comment.id == comment_id, Comment.post_id == post_id)
        .options(selectinload(Comment.user))
    )
    comment = await db.execute(statement)
    return comment.scalar_one_or_none()
