import pytest
from httpx import ASGITransport, AsyncClient

from application.database import cache
from application.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def clear_redis():
    await cache.redis.flushdb()
    yield


@pytest.mark.asyncio
async def test_post_cache(client):
    # -------------------
    # 1. CREATE
    # -------------------
    post_data = {
        "title": "Test Post",
        "content": "This is a test post.",
    }

    response = await client.post("/api/v1/posts/", json=post_data)
    assert response.status_code == 201

    created = response.json()
    post_id = created["id"]

    assert created["title"] == post_data["title"]
    assert created["content"] == post_data["content"]

    # -------------------
    # 2. GET
    # -------------------
    response = await client.get(f"/api/v1/posts/{post_id}/")
    assert response.status_code == 200

    fetched = response.json()

    cached = await cache.get_item(f"post:{post_id}")
    assert cached is not None

    assert fetched["title"] == cached["title"]
    assert fetched["content"] == cached["content"]

    # -------------------
    # 3. PATCH
    # -------------------
    update_data = {"title": "Updated Title"}

    response = await client.patch(
        f"/api/v1/posts/{post_id}/",
        json=update_data,
    )
    assert response.status_code == 200

    updated = response.json()

    cached = await cache.get_item(f"post:{post_id}")
    assert cached is not None

    assert cached["title"] == "Updated Title"
    assert cached["content"] == post_data["content"]

    assert updated["title"] == "Updated Title"

    # -------------------
    # 4. DELETE (destroy)
    # -------------------
    response = await client.delete(f"/api/v1/posts/{post_id}/")
    assert response.status_code == 204

    cached = await cache.get_item(f"post:{post_id}")
    assert cached is None
