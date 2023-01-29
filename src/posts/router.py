from typing import List

from auth.models import User
from auth.router import get_current_active_user
from db.database import get_async_session
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post
from .schemas import PostCreate
from .schemas import PostRead
from .schemas import PostUpdate
from .services import create_new_post
from .services import delete_a_post
from .services import get_all_posts
from .services import get_post
from .services import update_a_post

post_router = APIRouter(prefix="/posts", tags=["Posts"])


@post_router.post("/", response_model=PostRead)
async def create_post(
    postData: PostCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    new_post: Post = Post.from_orm(postData)
    new_post.user = user
    new_post.user_id = user.id
    return await create_new_post(db=db, post=new_post)


@post_router.get("/", response_model=List[PostRead])
async def get_posts(db: AsyncSession = Depends(get_async_session)):
    posts = await get_all_posts(db)
    return posts


@post_router.get("/{post_id}", response_model=PostRead)
async def get_a_post(*, db: AsyncSession = Depends(get_async_session), post_id: int):
    post = await get_post(db, post_id)
    return post


@post_router.patch("/{post_id}", response_model=PostRead)
async def update_post(
    *,
    db: AsyncSession = Depends(get_async_session),
    post_id: int,
    post_data: PostUpdate,
    user: User = Depends(get_current_active_user)
):
    post_info = post_data.dict(exclude_unset=True)
    post = await update_a_post(db, post_info, post_id, user_id=user.id)
    return post


@post_router.delete("/{post_id}")
async def delete_post(
    *,
    db: AsyncSession = Depends(get_async_session),
    post_id: int,
    user: User = Depends(get_current_active_user)
):
    return await delete_a_post(db, post_id, user.id)
