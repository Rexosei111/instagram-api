from typing import Dict
from typing import List
from typing import Union

from auth.models import User
from auth.router import get_current_active_user
from db.database import get_async_session
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from posts.services import get_post
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Comment
from .schemas import CommentCreate
from .schemas import CommentRead
from .services import create_new_comment
from .services import get_a_comment
from .services import get_post_comments

comment_router = APIRouter(prefix="/posts", tags=["Comments"])


@comment_router.get("/{post_id}/comments", response_model=List[CommentRead])
async def get_comments(post_id: int, db: AsyncSession = Depends(get_async_session)):

    comments = await get_post_comments(db, post_id)

    return comments


@comment_router.post(
    "/{post_id}/comments", response_model=Union[CommentRead, Dict[str, str]]
)
async def create_comment(
    post_id: int,
    commentData: CommentCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_session),
):

    post = await get_post(db, post_id)

    comment: Comment = Comment.from_orm(
        commentData, update={"user_id": user.id, "post_id": post.id}
    )
    comment.user = user
    new_comment = await create_new_comment(db, comment)
    return new_comment


@comment_router.delete("/{post_id}/comments/{comment_id}")
async def delete_comment(
    post_id: int,
    comment_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_active_user),
):
    comment = await get_a_comment(db, comment_id, post_id)
    if comment.user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have the permission to delete this comment",
        )
    try:
        await db.delete(comment)
        await db.commit()
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong"
        )
    return True
