from typing import Dict
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Post


async def create_new_post(db: AsyncSession, post: Post):
    try:
        db.add(post)
        await db.commit()
        await db.refresh(post)
    except SQLAlchemyError:
        raise HTTPException(500, detail="Something went wrong")
    return post


async def get_all_posts(db: AsyncSession):
    statement = select(Post).options(selectinload(Post.user))
    try:
        posts = await db.execute(statement)
    except SQLAlchemyError:
        raise HTTPException(500, detail="Something went wrong")
    return posts.scalars().all()


async def get_post(db: AsyncSession, post_id: int) -> Post:
    statement = (
        select(Post).where(Post.caption == post_id).options(selectinload(Post.user))
    )
    try:
        results = await db.execute(statement)
        post = results.scalar_one()
    except (MultipleResultsFound, SQLAlchemyError):
        raise HTTPException(500, detail="Something went wrong")
    return post


async def get_my_posts(db: AsyncSession, user_id: UUID):
    statement = select(Post).select(Post.user_id == user_id)
    try:
        results = await db.execute(statement)
        posts = await results.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(500, detail="Something went wrong")
    return posts


async def update_a_post(
    db: AsyncSession, post_data: Dict[str, str], post_id: int, user_id: UUID
):
    statement = select(Post).where(Post.id == post_id, Post.user_id == user_id)
    try:

        post = await db.scalar(statement)
        if post is None:
            raise HTTPException(404, detail="Post not found")
    except SQLAlchemyError:
        raise HTTPException(500, detail="Something went wrong")
    for key, value in post_data.items():
        setattr(post, key, value)
    try:
        db.add(post)
        await db.commit()
        await db.refresh(post)
    except SQLAlchemyError:
        raise HTTPException(500, detail="Something went wrong")
    return post


async def delete_a_post(db: AsyncSession, post_id: int, user_id: UUID):
    try:
        post = await db.scalar(
            select(Post).where(Post.id == post_id, Post.user_id == user_id)
        )
        if post is None:
            raise HTTPException(404, detail="Post not found")
    except SQLAlchemyError:
        raise HTTPException(500, detail="Something went wrong")
    try:
        await db.delete(post)
        await db.commit()
    except SQLAlchemyError:
        raise HTTPException(500, detail="Something went wrong")
    return True
