from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from application.database import Post, cache
from application.exceptions import PostNotFoundError


class PostsService:
    POST_KEY = "post:{}"

    @classmethod
    async def _add_item_to_redis(cls, post: Post, key: int | None = None):
        cache_key = None
        if key:
            cache_key = cls.POST_KEY.format(key)
        else:
            cache_key = cls.POST_KEY.format(post.id)

        await cache.add_item(
            cache_key,
            {
                "id": str(post.id),
                "title": post.title,
                "content": post.content,
                "created_at": str(post.created_at),
                "updated_at": str(post.updated_at),
            },
        )

    @classmethod
    async def get_list(cls, db_session: AsyncSession):
        result = await db_session.execute(select(Post))
        posts = result.scalars().all()
        return posts

    @classmethod
    async def get_post(cls, id: int, db_session: AsyncSession):
        cache_key = cls.POST_KEY.format(id)

        cached = await cache.get_item(cache_key)
        if cached:
            return cached

        post = await db_session.get(Post, id)
        if not post:
            raise PostNotFoundError(f"Post with id {id} not found")

        await cls._add_item_to_redis(post)

        return post

    @classmethod
    async def create_post(cls, post_data: dict, db_session: AsyncSession):
        try:
            post = Post(**post_data.model_dump())
            db_session.add(post)
            await db_session.commit()
            await db_session.refresh(post)

            await cls._add_item_to_redis(post)

            return post
        except IntegrityError as e:
            await db_session.rollback()
            raise e

    @classmethod
    async def patch_post(
        cls,
        id: int,
        post_data: dict,
        db_session: AsyncSession,
    ):
        post = await db_session.get(Post, id)

        try:
            update_data = post_data.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                if hasattr(post, key):
                    setattr(post, key, value)

            await db_session.commit()
            await db_session.refresh(post)

            await cls._add_item_to_redis(post)

            return post
        except IntegrityError as e:
            await db_session.rollback()
            raise e

    @classmethod
    async def delete_post(cls, id: int, db_session: AsyncSession):
        try:
            result = await db_session.execute(delete(Post).where(Post.id == id))

            if result.rowcount == 0:
                raise PostNotFoundError(f"Post with id {id} not found")

            await db_session.commit()

            await cache.delete_item(cls.POST_KEY.format(id))

            return True
        except Exception as e:
            await db_session.rollback()
            raise e
