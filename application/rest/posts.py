from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.database import db
from application.logic import PostsService
from application.schemas import PostCreate, PostResponse, PostUpdate

db_session_annotate = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostResponse])
async def list_posts(db_session: db_session_annotate):
    posts = await PostsService.get_list(db_session)
    return posts


@router.get("/{post_id}/", response_model=PostResponse)
async def get_post(post_id: int, db_session: db_session_annotate):
    post = await PostsService.get_post(post_id, db_session)
    return post


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: Annotated[PostCreate, Body()], db_session: db_session_annotate
):
    post = await PostsService.create_post(post_data, db_session)
    return post


@router.patch("/{post_id}/", response_model=PostResponse)
async def patch_post(
    post_id: int,
    post_data: Annotated[PostUpdate, Body()],
    db_session: db_session_annotate,
):
    post = await PostsService.patch_post(post_id, post_data, db_session)
    return post


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def destroy_post(post_id: int, db_session: db_session_annotate):
    return await PostsService.delete_post(post_id, db_session)
