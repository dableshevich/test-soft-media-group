FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock* pytest.ini ./

RUN uv sync --frozen --no-cache

COPY application/ application/

CMD ["uv", "run", "uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "8000"]