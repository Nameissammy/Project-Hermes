FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (optional minimal)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml uv.lock ./
RUN pip install --upgrade pip && pip install uv
RUN uv pip install --system --no-cache --require-hashes --locked

COPY src ./src
COPY run_server.py ./

ENV PYTHONPATH=/app/src
EXPOSE 8001

CMD ["python", "run_server.py"]


