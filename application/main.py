from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from application.config import settings
from application.database import db
from application.exceptions import PostNotFoundError
from application.rest import posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_models()

    yield

    await db.close()


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version="1.0.0",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/documentation",
    redoc_url=None,
    lifespan=lifespan,
)


@app.exception_handler(PostNotFoundError)
async def post_not_found_handler(request: Request, exc: PostNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(posts_router, prefix=settings.API_PREFIX)
