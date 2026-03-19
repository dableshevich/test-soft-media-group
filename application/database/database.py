from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from application.config import settings

from .models import Base


class Database:
    def __init__(self, url):
        self.engine = create_async_engine(url)
        self.sessionmaker = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

    async def get_session(self):
        async with self.sessionmaker() as session:
            yield session

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        await self.engine.dispose()


db = Database(settings.DATABASE_URL)
