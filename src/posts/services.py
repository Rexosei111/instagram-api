from typing import Dict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Post


async def create_new_post(db: AsyncSession, post: Post):
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post


async def get_all_posts(db: AsyncSession):
    statement = select(Post).options(selectinload(Post.user))
    posts = await db.execute(statement)
    return posts.scalars().all()


async def get_post(db: AsyncSession, post_id: int) -> Post:
    statement = select(Post).where(Post.id == post_id).options(selectinload(Post.user))
    post = await db.execute(statement)
    return post.scalar_one_or_none()


async def get_my_posts(db: AsyncSession, user_id: UUID):
    statement = select(Post).select(Post.user_id == user_id)
    posts = await db.execute(statement)
    return await posts.scalars().all()


async def update_a_post(
    db: AsyncSession, post_data: Dict[str, str], post_id: int, user_id: UUID
):
    print(post_data)
    statement = select(Post).where(Post.id == post_id, Post.user_id == user_id)
    post = await db.scalar(statement)
    for key, value in post_data.items():
        setattr(post, key, value)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def delete_a_post(db: AsyncSession, post_id: int, user_id: UUID):
    post = await db.scalar(
        select(Post).where(Post.id == post_id, Post.user_id == user_id)
    )
    await db.delete(post)
    await db.commit()
    return True
